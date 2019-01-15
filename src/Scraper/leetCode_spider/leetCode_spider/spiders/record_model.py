# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# record_model.py
# ---------------
# Author: Zhongheng Li
# Start Date: 1-14-19
# Last Modified Date: 1-14-19


"""
This python script will be execute while running the spider script.

"""


# 3rd party modules
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



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




