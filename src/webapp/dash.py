# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# dash.py
# ---------------
# Author: Zhongheng Li
# Start Date: 1-18-19
# Last Modified Date: 1-18-19


"""
This python script will be used for the front-end.

"""

# System modules
import os
from os.path import dirname as up
from datetime import date

# 3rd party modules
import pandas as pd
import configparser


import dash
import dash_table
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc



from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData



# Set up DB configs file path
projectPath = up(os.getcwd())
DB_configs_ini_file_path = "/DB/db_configs.ini"

db_config = configparser.ConfigParser()
db_config.read(projectPath + DB_configs_ini_file_path)


print(projectPath + DB_configs_ini_file_path)

DB_TYPE = db_config['DB_Configs']['DB_TYPE']
DB_DRIVER = db_config['DB_Configs']['DB_DRIVER']
DB_USER = db_config['DB_Configs']['DB_USER']
DB_PASS = db_config['DB_Configs']['DB_PASS']
DB_HOST = db_config['DB_Configs']['DB_HOST']
DB_PORT = db_config['DB_Configs']['DB_PORT']
DB_NAME = db_config['DB_Configs']['DB_NAME']



SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,

                                                      DB_PASS, DB_HOST, DB_PORT, DB_NAME)
db_engine = create_engine(
    SQLALCHEMY_DATABASE_URI, echo=False)



# Setting for sqlalchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


Session = sessionmaker(db_engine)
session = Session()


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


# Read
records = session.query(leetcode_record,fellow).join(fellow, leetcode_record.user_name==fellow.leetcode_user_name).filter(leetcode_record.record_date == str(date.today()))

print(records.statement)

df = pd.read_sql(sql = records.statement, con=records.session.bind, index_col="record_id")




PAGE_SIZE = 25



app = dash.Dash(__name__)

app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                pagination_settings={
                    'current_page': 0,
                    'page_size': 25
                },
                pagination_mode='be',

                filtering='be',
                filtering_settings='',

                sorting='be',
                sorting_type='multi',
                sorting_settings=[]
            ),
            style={'height': 750, 'overflowY': 'scroll'},
            className='six columns'
        ),
        html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        )
    ]
)

@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "pagination_settings"),
     Input('table-paging-with-graph', "sorting_settings"),
     Input('table-paging-with-graph', "filtering_settings")])
def update_table(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = df
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    if len(sorting_settings):
        dff = dff.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["user_name"],
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            for column in ["num_solved","num_accepts","num_submissions","accepted_percentage"]
        ]
    )




if __name__ == '__main__':
    app.run_server(debug=True)