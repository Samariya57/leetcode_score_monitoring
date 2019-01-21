#!/bin/bash

source $LEETCODE_PROJECT_ENV
echo "Scrapy_Start!!"
cd $LEETCODE_PROJECT_SCRAPER_PATH
scrapy crawl leetcode -a user_names="oreki47,zl1761,hideaki,rogerfederer,euijun0109,inctrl,strenghten,kmgowda,jacot,coastd54703,lanrengufeng,hackersplendid,danny1718,zitaowang,cslzy,shaw3257"
