# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from datetime import date



class LeetCodeSpider(scrapy.Spider):
    name = 'leetcode'
    allowed_domains = ['leetcode.com']

    def __init__(self, models=None, *args, **kwargs):
        self.endpoints = kwargs.get('user_names').split(',')
        self.start_urls = ["https://leetcode.com/" + x for x in self.endpoints]
        self.users = []
        self.userIndex = 0
        self.lenOfURLs = len(self.start_urls)



    def parse(self, response):

        badge_onprogress_bar = response.selector.xpath("//span[@class='badge progress-bar-success']/text()").extract()

        has_contest = False if len(badge_onprogress_bar) <= 6 else True

        columns = ['email', 'user_id', 'first_name', 'last_name', 'num_solved', 'num_accepts','num_submissions', 'solved_percentage',
                   'points', 'finished_contests', 'contest_rating' , 'global_ranking', 'date']

        user_model = None

        if has_contest:

            user_model = {

                # 'email': product_id,
                # 'user_id': product.title,

                # 'first_name': product_id,
                # 'last_name': product.title,

                'num_solved': int(badge_onprogress_bar[3].split('\n')[1].strip().split('/')[0].strip()) ,
                'num_accepts' :  int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[0].strip()),
                'num_submissions': int(badge_onprogress_bar[4].split('\n')[1].strip().split('/')[1].strip()),

                'solved_percentage': float(response.xpath("//li[@class='list-group-item'][3]/span[@class='badge progress-bar-info']/text()").extract()[0].split('\n')[1].strip().replace('%','').strip()) ,
                'points': int(badge_onprogress_bar[5].split('\n')[1].strip()),

                'finished_contests': int(badge_onprogress_bar[0].split('\n')[1].strip()),

                'contest_rating': int(badge_onprogress_bar[1].split('\n')[2].strip()),

                'global_ranking' : badge_onprogress_bar[2].split('\n')[1].strip(),


                'date': str(date.today())

            }

        else:

            user_model = {

                # 'email': product_id,
                # 'user_id': product.title,

                # 'first_name': product_id,
                # 'last_name': product.title,

                'num_solved': int(badge_onprogress_bar[1].split('\n')[1].strip().split('/')[0].strip()) ,
                'num_accepts' :  int(badge_onprogress_bar[2].split('\n')[1].strip().split('/')[0].strip()),
                'num_submissions': int(badge_onprogress_bar[2].split('\n')[1].strip().split('/')[1].strip()),

                'solved_percentage': float(response.xpath("//li[@class='list-group-item'][3]/span[@class='badge progress-bar-info']/text()").extract()[0].split('\n')[1].strip().replace('%','').strip()) ,
                'points': int(badge_onprogress_bar[3].split('\n')[1].strip()),

                'finished_contests': int(badge_onprogress_bar[0].split('\n')[1].strip()),
                'date': str(date.today())

            }

        print('user_model:', user_model)

        self.users.append(user_model)

        self.userIndex += 1

        if self.userIndex == self.lenOfURLs:
            df = pd.DataFrame(self.users, columns=columns)

            print("export fellows.csv")

            df.to_csv("leetCode_spider/data/fellows.csv", sep=",")




