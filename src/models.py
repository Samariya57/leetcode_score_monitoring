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
from datetime import datetime
# from config import db, ma


# 3rd party modules
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# Setting for sqlalchemy
Base = declarative_base()


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



#
# class Word(db.Model):
#     __tablename__ = "words"
#     word_id = db.Column(db.Integer, primary_key=True)
#     word = db.Column(db.String(32))
#     pronunciation = db.Column(db.String(32))
#     phoneme = db.Column(db.String(32))
#     timestamp = db.Column(
#         db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
#     )
#
#
# class WordSchema(ma.ModelSchema):
#     class Meta:
#         model = Word
#         sqla_session = db.session
#
#
# class Song(db.Model):
#     __tablename__ = "songs"
#     song_id = db.Column(db.Integer, primary_key=True)
#     song = db.Column(db.String(32))
#     year = db.Column(db.Integer)
#     artist = db.Column(db.String(128))
#     genre = db.Column(db.String(32))
#     lyrics = db.Column(db.Text()) # text
#     timestamp = db.Column(
#         db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
#     )
#

# class SongSchema(ma.ModelSchema):
#     class Meta:
#         model = Song
#         sqla_session = db.session