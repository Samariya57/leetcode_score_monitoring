#!/bin/bash

source $LeetCode_Project_env
echo "Scrapy_Start!!"
cd /Users/zhonghengli/Documents/Insight/leetCodeProject/leetcode_score_monitoring/src/Scraper/leetCode_spider
scrapy crawl leetcode -a user_names="zl1761,hideaki,oreki47"
