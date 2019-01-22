#!/usr/bin/env python3
# scraping_scheduler_dag.py
# ---------------
# Author: Zhongheng Li
# Start Date: 12-20-18
# Last Modified Date: 1-13-19


"""
This is a dag to schedule the scraping script to run daily at 7:00am EST

"""

# System modules
import datetime as dt

# 3rd party modules
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 12, 20, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('leetCoode_scrapying_dag',
         catchup=False,
         default_args=default_args,
         # Set for testing purpose to run in every 5 seconds
         # schedule_interval='*/5 * * * *',
         # Should run daily at 7:00 am
         schedule_interval='00 7 * * *',
         ) as dag:



    opr_init_msg = BashOperator(task_id='init_msg',
                             bash_command='echo "Scrapy_Start!!"')

    opr_run_daily_scraper = BashOperator(task_id='run_daily_scraper',
                             bash_command='cd $LEETCODE_PROJECT_SCRAPER_PATH && sh run.sh ')



opr_init_msg >> opr_run_daily_scraper

