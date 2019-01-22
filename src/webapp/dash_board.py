# -*- coding: utf-8 -*-

# !/usr/bin/env python3
# dash_board.py
# ---------------
# Author: Zhongheng Li
# Start Date: 1-18-19
# Last Modified Date: 1-18-19


"""
This python script runs with dash and is used for the front-end.

"""


# System modules
import os
from datetime import date
from os.path import dirname as up
import sys
import configparser
projectPath = up(os.getcwd())
sys.path.append(projectPath)

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
# 3rd party modules
import pandas as pd
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Internal modules
from models import fellow, leetcode_record

# Set up DB configs file path
DB_configs_ini_file_path = projectPath + "/DB/db_configs.ini"




def getSQL_DB_Engine(filePath):
    """

    :param filePath: DB configs ini file path
    :return: SQLalchemy database engine
    """

    config = configparser.ConfigParser()
    config.read(filePath)

    DB_TYPE = config['DB_Configs']['DB_TYPE']
    DB_DRIVER = config['DB_Configs']['DB_DRIVER']
    DB_USER = config['DB_Configs']['DB_USER']
    DB_PASS = config['DB_Configs']['DB_PASS']
    DB_HOST = config['DB_Configs']['DB_HOST']
    DB_PORT = config['DB_Configs']['DB_PORT']
    DB_NAME = config['DB_Configs']['DB_NAME']
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
                                                          DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI, echo=False)


    return engine


db_engine = getSQL_DB_Engine(DB_configs_ini_file_path)

Session = sessionmaker(db_engine)
session = Session()

# Get the latest updated fellows' leetcode records from database
records = session.query(leetcode_record, fellow).join(fellow,
                                                      leetcode_record.user_name == fellow.leetcode_user_name).filter(
    leetcode_record.record_date == str(date.today()))

df = pd.read_sql(sql=records.statement, con=records.session.bind, index_col="record_id")

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
           pagination_settings['current_page'] * pagination_settings['page_size']:
           (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
           ].to_dict('rows')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column_info[0],
                figure={
                    "data": [
                        {
                            "x": dff["user_name"],
                            "y": dff[column_info[0]] if column_info[0] in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "title": column_info[1],
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 35, "l": 10, "r": 10},
                    },
                },
            )
            for column_info in
            [("num_solved", "Number of Solved Questions"), ("num_submissions", "Number of Submissions"),
             ("accepted_percentage", "Acceptance Rate")]
        ]
    )


if __name__ == '__main__':
    # change host from the default to '0.0.0.0' to make it publicly available
    app.server.run(port=8050, host='0.0.0.0')
    app.run_server(debug=True)
