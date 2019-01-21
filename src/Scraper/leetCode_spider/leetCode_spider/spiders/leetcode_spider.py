from __future__ import absolute_import

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
from sqlalchemy.orm import sessionmaker

# Internal Modules
from .record_model import  fellow, leetcode_record


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




# LeetCodeSpider class for web crawling
class LeetCodeSpider(CrawlSpider):

    # Init the domain name of the website to be crawled
    name = 'leetcode'
    allowed_domains = ['leetcode.com']


    def __init__(self, models=None, *args, **kwargs):
        self.records = []
        self.userIndex = 0
        self.rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr/td[2]/a'), callback="parse_table_links", follow= True),
    )
        self.DB_engine = self.getSQL_DB_Engine()


        Session = sessionmaker(self.DB_engine)
        session = Session()

        # Read fellows
        fellows = session.query(fellow).filter(fellow.job_searching == True)
        fellows_leetcode_user_names = [this_fellow.leetcode_user_name for this_fellow in fellows ] #kwargs.get('user_names').split(',')

        self.start_urls = ["https://leetcode.com/" + username for username in fellows_leetcode_user_names]
        self.lenOfURLs = len(self.start_urls)

    def getSQL_DB_Engine(self, filePath = None):

        config = configparser.ConfigParser()
        config.read(projectPath + DB_configs_ini_file_path)


        DB_TYPE = config['DB_Configs']['DB_TYPE']
        DB_DRIVER = config['DB_Configs']['DB_DRIVER']
        DB_USER = config['DB_Configs']['DB_USER']
        DB_PASS = config['DB_Configs']['DB_PASS']
        DB_HOST = config['DB_Configs']['DB_HOST']
        DB_PORT = config['DB_Configs']['DB_PORT']
        DB_NAME = config['DB_Configs']['DB_NAME']
        POOL_SIZE = config['DB_Configs']['POOL_SIZE']
        TABLENAME = config['DB_Configs']['TABLENAME']
        SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
                                                              DB_PASS, DB_HOST, DB_PORT, DB_NAME)

        ENGINE = create_engine(
            SQLALCHEMY_DATABASE_URI, echo=False)

        return ENGINE

    def parse(self, response):

        user_name = response.url.split('/')[-2]

        badge_onprogress_bar = response.selector.xpath("//span[@class='badge progress-bar-success']/text()").extract()

        has_contest = False if len(badge_onprogress_bar) <= 6 else True

        # columns = ['email', 'user_name', 'first_name', 'last_name', 'num_solved', 'num_accepts','num_submissions', 'accepted_percentage',
        #            'finished_contests', 'record_date']

        columns = ['user_name', 'num_solved', 'num_accepts','num_submissions', 'accepted_percentage',
                   'finished_contests', 'record_date']

        user_model = None

        if has_contest:

            user_model = {

                'record_id': user_name + '_' + str(date.today()),
                'user_name': user_name,
                'num_solved': int(badge_onprogress_bar[3].split('\n')[1].strip().split('/')[0].strip()) ,
                'num_accepts' :  int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[0].strip()),
                'num_submissions': int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[1].strip()),
                'accepted_percentage': float(response.xpath("//li[@class='list-group-item'][3]/span[@class='badge progress-bar-info']/text()").extract()[0].split('\n')[1].strip().replace('%','').strip()) ,
                # 'points': int(badge_onprogress_bar[5].split('\n')[1].strip()),
                'finished_contests': int(badge_onprogress_bar[0].split('\n')[1].strip()),
                # 'contest_rating': int(badge_onprogress_bar[1].split('\n')[2].strip()),
                # 'global_ranking' : badge_onprogress_bar[2].split('\n')[1].strip(),
                'record_date': str(date.today())

            }

        else:

            user_model = {

                'record_id': user_name + '_' + str(date.today()),
                'user_name': user_name,
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

                r = self.DB_engine.execute(stmt)


