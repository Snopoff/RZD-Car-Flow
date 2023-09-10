#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash import Dash, dcc, html, Input, Output, State, callback
from iterational_solution import IterationalProblem

data = pd.read_json("dataset.json")
data_to_see = data.iloc[10]

problem = IterationalProblem("dataset.json")
problem.solve()

hat = [item[:-4] for item in data_to_see['stations'].keys()]

app = dash.Dash(__name__)
app.layout = html.Div(
    style={'background-image': 'url("https://catherineasquithgallery.com/uploads/posts/2021-02/thumbs/1613682224_1-p-fon-dlya-prezentatsii-zheleznaya-doroga-1.jpg")',
           'background-size': 'cover',
           'width': '100%',
           'height': '110vh'},
    children=[
        html.Br(),
        html.H1(children='Координация пропуска вагонопотока',
                style={'fontSize':'36px', 'textAlign':'center'}),
        html.Div([
        html.Div([
            html.Label('Выберете экземпляр вагонопотока ', style={'fontSize':'20px', 'textAlign':'center'}),
            dcc.Input(
                id='input1',
                type='number',
                min=1,
                max=100000,
                step='1',
                style={'margin-left': '10px'}
            ),
            html.Br(),
            html.Br(),
            html.Label('Выберите станцию', style={'fontSize':'20px', 'textAlign':'center'}),
            dcc.Dropdown(hat,
                id='drop1',
                multi=False,
                style={'width': '500px'}
            ),
            html.Div(id='output1'),
            html.Br(),
            html.Button('Посмотреть вагонопоток', id='button', n_clicks=0,
                        style={'fontSize':'14px', 'width': '200px',
                               'fontWeight': 'bold', 'height': '30px'}),
        ],
                style={'width': '50%', 'float': 'left', 'height': '30vh'}
        ),
        html.Img(
        src="https://digital-natt.ru/upload/iblock/b2b/bobsqm4xuyyaf2uaqox36ly79egwvg79.png",
        style={'width': '50%', 'float': 'right'}
        )
        ]),
        html.Div([
            html.Br(),
            html.Div(
                children=[
                    html.H1(children='Выполненные расчеты',
                            style={'fontSize': '32px', 'textAlign': 'center'}),
                    dash_table.DataTable(
                        id='table',
                        data=[],
                        style_cell={'textAlign': 'left', 'minWidth': '150px',
                                    'whiteSpace': 'normal', 'height': 'auto',
                                    'fontSize': '12px'},
                        style_header={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '14px'}
                    )

                ],
                style={'width': '100%', 'margin': '0 auto'}
            )
        ]
        )
    ]
)

@app.callback(
    Output('output1', 'children'),
    Input('drop1', 'value')
)
def update_drop(station):
    if station:
        return f'Вы сотрудник станции {station}'
    else:
        return 'Выберите станцию для расписания вагонопотока'

@app.callback(
    Output('table','data'),
    Output('table','columns'),
    State('input1', 'value'),
    State('drop1', 'value'),
    Input('button', 'n_clicks')
)

def update_table(ecz, city, click):
    if click>0:
        df = problem.get_solution_for_city((ecz-1),city)
        df = df.rename(columns={'trains':'Поезд', 'number of cars':'Количество вагонов для сцепки',
                          'arrival time':'Время прибытия', 'departure time':'Время отбытия'}, inplace=False)
        
        df1 = df.to_dict('records')
        columns = df.columns
        columns=[{"name": i, "id": i} for i in columns]
        
        return df1, columns
    else:
        return [], []

if __name__ == '__main__':
    app.run_server(mode='inline', debug=True)


# In[ ]:




