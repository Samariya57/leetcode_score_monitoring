#!/bin/bash

source $LEETCODE_PROJECT_ENV
echo "Scrapy_Start!!"
cd $LEETCODE_PROJECT_SCRAPER_PATH
scrapy crawl leetcode -a user_names="zl1761,hideaki,oreki47"
