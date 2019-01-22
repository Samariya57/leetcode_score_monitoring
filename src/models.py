#!/usr/bin/env python3
# models.py
# ---------------
# Author: Zhongheng Li
# Start Date: 1-19-19
# Last Modified Date: 1-21-19


"""
This is the models module that store the schema for the objects that we are using in this project


"""


# System modules


# 3rd party modules
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# Setting for sqlalchemy
Base = declarative_base()


# class to model the fellow object
class fellow(Base):
    __tablename__ = "active_fellows"
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