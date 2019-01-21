# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# leetcode_spider.py
# ---------------
# Author: Zhongheng Li
# Start Date: 12-20-18
# Last Modified Date: 1-13-19


"""
This python script will be execute while running the spider script.

"""

# System modules
from datetime import date
import configparser
import os
from os.path import dirname as up
import logging

# 3rd party modules
import scrapy
import pandas as pd
from sqlalchemy import create_engine

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

from sqlalchemy import join, select , Table
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.declarative import declarative_base


"""
Settings

"""

# Setting for logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('leetcode_spider.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Setting for sqlalchemy
Base = declarative_base()




# Set up DB configs file path
projectPath = up(up(os.getcwd()))
DB_configs_ini_file_path = "/DB/db_configs.ini"

# print(projectPath + DB_configs_ini_file_path)
logger.info('Loaded DB configs file from: {}'.format(projectPath + DB_configs_ini_file_path))


# class to model the fellow object
class fellow(Base):
    __tablename__ = "active_fellow"
    leetcode_user_name = sa.Column(sa.VARCHAR(50), primary_key=True)
    first_name = sa.Column(sa.VARCHAR(50))
    last_name = sa.Column(sa.VARCHAR(50))
    email = sa.Column(sa.VARCHAR(50))
    program = sa.Column(sa.VARCHAR(5))
    session_location = sa.Column(sa.VARCHAR(5))
    session_code = sa.Column(sa.VARCHAR(5))
    job_searching = sa.Column(sa.BOOLEAN())


# class to model the leetcode_record object
class leetcode_record(Base):
    __tablename__ = "leetcode_records"
    record_id = sa.Column(sa.VARCHAR(70), primary_key=True)
    user_name = sa.Column(sa.VARCHAR(50))
    num_solved = sa.Column(sa.INTEGER())
    num_accepts = sa.Column(sa.INTEGER())
    num_submissions = sa.Column(sa.INTEGER())
    accepted_percentage = sa.Column(sa.NUMERIC())
    finished_contests = sa.Column(sa.INTEGER())
    record_date = sa.Column(sa.DATE())



# LeetCodeSpider class for web crawling
class LeetCodeSpider(CrawlSpider):

    # Init the domain name of the website to be crawled
    name = 'leetcode'
    allowed_domains = ['leetcode.com']


    def __init__(self, models=None, *args, **kwargs):
        self.endpoints = kwargs.get('user_names').split(',')
        self.start_urls = ["https://leetcode.com/" + x for x in self.endpoints]
        self.records = []
        self.userIndex = 0
        self.lenOfURLs = len(self.start_urls)
        self.rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr/td[2]/a'), callback="parse_table_links", follow= True),
    )

    #
    # def getSQL_DB_Engine(self, filePath = None):
    #
    #     config = configparser.ConfigParser()
    #     config.read(projectPath + DB_configs_ini_file_path)
    #
    #
    #     DB_TYPE = config['DB_Configs']['DB_TYPE']
    #     DB_DRIVER = config['DB_Configs']['DB_DRIVER']
    #     DB_USER = config['DB_Configs']['DB_USER']
    #     DB_PASS = config['DB_Configs']['DB_PASS']
    #     DB_HOST = config['DB_Configs']['DB_HOST']
    #     DB_PORT = config['DB_Configs']['DB_PORT']
    #     DB_NAME = config['DB_Configs']['DB_NAME']
    #     POOL_SIZE = config['DB_Configs']['POOL_SIZE']
    #     TABLENAME = config['DB_Configs']['TABLENAME']
    #     SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
    #                                                           DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    #
    #     ENGINE = create_engine(
    #         SQLALCHEMY_DATABASE_URI, echo=False)
    #
    #     return ENGINE

    def parse(self, response):

        # # Build the sql ULR for SqlAlchemy

        db_config = configparser.ConfigParser()
        db_config.read(projectPath + DB_configs_ini_file_path)

        DB_TYPE = db_config['DB_Configs']['DB_TYPE']
        DB_DRIVER = db_config['DB_Configs']['DB_DRIVER']
        DB_USER = db_config['DB_Configs']['DB_USER']
        DB_PASS = db_config['DB_Configs']['DB_PASS']
        DB_HOST = db_config['DB_Configs']['DB_HOST']
        DB_PORT = db_config['DB_Configs']['DB_PORT']
        DB_NAME = db_config['DB_Configs']['DB_NAME']
        SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,

                                                              DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        engine = create_engine(
            SQLALCHEMY_DATABASE_URI, echo=False)
        #
        # fellow = Table('active_fellows', engine, autoload=True)
        #
        # s = fellow.select(fellow.job_searching == True)
        # rs = s.execute()
        #
        # for row in rs:
        #     print(row)



        user_name = response.url.split('/')[-2]

        badge_onprogress_bar = response.selector.xpath("//span[@class='badge progress-bar-success']/text()").extract()

        has_contest = False if len(badge_onprogress_bar) <= 6 else True
        #
        # columns = ['email', 'user_name', 'first_name', 'last_name', 'num_solved', 'num_accepts','num_submissions', 'accepted_percentage',
        #            'finished_contests', 'record_date']

        columns = ['user_name', 'num_solved', 'num_accepts','num_submissions', 'accepted_percentage',
                   'finished_contests', 'record_date']

        user_model = None

        if has_contest:

            user_model = {

                'record_id': user_name + '_' + str(date.today()),
                'user_name': user_name,

                # 'first_name': product_id,
                # 'last_name': product.title,

                'num_solved': int(badge_onprogress_bar[3].split('\n')[1].strip().split('/')[0].strip()) ,
                'num_accepts' :  int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[0].strip()),
                'num_submissions': int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[1].strip()),

                'accepted_percentage': float(response.xpath("//li[@class='list-group-item'][3]/span[@class='badge progress-bar-info']/text()").extract()[0].split('\n')[1].strip().replace('%','').strip()) ,
                # 'points': int(badge_onprogress_bar[5].split('\n')[1].strip()),

                'finished_contests': int(badge_onprogress_bar[0].split('\n')[1].strip()),
                #
                # 'contest_rating': int(badge_onprogress_bar[1].split('\n')[2].strip()),
                #
                # 'global_ranking' : badge_onprogress_bar[2].split('\n')[1].strip(),
                #

                'record_date': str(date.today())

            }

        else:

            user_model = {

                'record_id': user_name + '_' + str(date.today()),
                'user_name': user_name,

                # 'first_name': product_id,
                # 'last_name': product.title,

                'num_solved': int(badge_onprogress_bar[1].split('\n')[1].strip().split('/')[0].strip()) ,
                'num_accepts' :  int(badge_onprogress_bar[2].split('\n')[1].strip().split('/')[0].strip()),
                'num_submissions': int(badge_onprogress_bar[2].split('\n')[1].strip().split('/')[1].strip()),

                'accepted_percentage': float(response.xpath("//li[@class='list-group-item'][3]/span[@class='badge progress-bar-info']/text()").extract()[0].split('\n')[1].strip().replace('%','').strip()) ,
                # 'points': int(badge_onprogress_bar[3].split('\n')[1].strip()),

                'finished_contests': int(badge_onprogress_bar[0].split('\n')[1].strip()),
                'record_date': str(date.today())

            }

        print('user_model:', user_model)

        self.records.append(user_model)

        self.userIndex += 1

        if self.userIndex == self.lenOfURLs:
            df = pd.DataFrame(self.records, columns=columns)

            print("export fellows_leetcode_records.csv")


            df.to_csv("leetCode_spider/data/" + str(date.today()) + "_fellows_leetcode_records.csv", sep=",", index=False)

            for record in self.records:
                stmt = pg_insert(leetcode_record).values(record)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[leetcode_record.record_id],
                    set_={'num_solved': stmt.excluded.num_solved,
                          'num_accepts': stmt.excluded.num_accepts,
                          'num_submissions': stmt.excluded.num_submissions,
                          'accepted_percentage': stmt.excluded.accepted_percentage,
                          'finished_contests': stmt.excluded.finished_contests,}
                )

                r = engine.execute(stmt)


