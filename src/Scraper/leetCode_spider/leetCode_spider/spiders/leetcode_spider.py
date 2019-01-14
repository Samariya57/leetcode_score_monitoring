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

# 3rd party modules
import scrapy
import pandas as pd
from sqlalchemy import create_engine


# Set up DB configs file path
projectPath = os.getcwd()
DB_configs_ini_file_path = "/leetCode_spider/spiders/db_configs.ini"

print(projectPath + DB_configs_ini_file_path)


class LeetCodeSpider(scrapy.Spider):
    name = 'leetcode'
    allowed_domains = ['leetcode.com']

    def __init__(self, models=None, *args, **kwargs):
        self.endpoints = kwargs.get('user_names').split(',')
        self.start_urls = ["https://leetcode.com/" + x for x in self.endpoints]
        self.users = []
        self.userIndex = 0
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

                # 'email': product_id,
                'user_name': self.start_urls[self.userIndex].split('/')[-1],

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

                # 'email': product_id,
                'user_name': self.start_urls[self.userIndex].split('/')[-1],

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

        self.users.append(user_model)

        self.userIndex += 1

        if self.userIndex == self.lenOfURLs:
            df = pd.DataFrame(self.users, columns=columns)

            print("export fellows.csv")

            # Build the sql ULR for SqlAlchemy
            # sql_url = "sqlite:////" + os.path.join(basedir, "story_writer.db")

            df.to_csv("leetCode_spider/data/" + str(date.today()) + "_fellows.csv", sep=",", index=False)

            engine = self.getSQL_DB_Engine()


            df.to_sql(name='leetcode_records', con=engine, if_exists='append', index=False)




