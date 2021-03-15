from jupyter_dash import JupyterDash
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import pandas as pd
import plotly.express as px
import plotly
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import random
from random_word import RandomWords

random_words = RandomWords()

JupyterDash.infer_jupyter_proxy_config()

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Interval(
            id='tick-component',
            n_intervals=0,
            disabled=True),
        dbc.Row(
            [
                dbc.Col([

                    ######################## obwiń w card
                    dbc.Row([
                        dbc.Col(html.Div("h0:"), width=1),
                        dbc.Col(dbc.Input(type="number", min=0, max=10, step=0.5, bs_size='sm'), width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("A:"), width=1),
                        dbc.Col(dbc.Input(type="number", min=0, max=10, step=0.5, bs_size='sm'), width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("Qd"), width=1),
                        dbc.Col(dbc.Input(type="number", min=0, max=10, step=0.5, bs_size='sm'), width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("β:"), width=1),
                        dbc.Col(dbc.Input(type="number", min=0, max=10, step=0.5, bs_size='sm'), width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("Tp:"), width=1),
                        dbc.Col(dbc.Input(type="number", min=0, max=10, step=0.5, bs_size='sm'), width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=2, className='px-0'),
                        dbc.Col(dbc.Button("Send", className='ml-2', size='sm'))
                    ], align="center", className='my-2'),
                    #############################
                    html.Div([
                        dbc.Row([
                            dbc.Col([dbc.Button("START", size='sm', block=True, n_clicks=0, id='start-button')],
                                    className='mx-1', width={"size": 4, "offset": 1}),
                            dbc.Col([dbc.Button("STEP", size='sm', block=True)], className='mx-1', width=4)
                        ], no_gutters=True, className='my-1'),
                        dbc.Row([
                            dbc.Col([dbc.Button("STOP", size='sm', block=True, id='stop-button', n_clicks=0)],
                                    className='mx-1', width={"size": 4, "offset": 1}),
                            dbc.Col([dbc.Button("CLEAR", size='sm', block=True)], className='mx-1', width=4)
                        ], no_gutters=True, className='my-1'),
                    ]),
                    html.Div('', id='placeholder-div')
                    ###############################
                    # tutaj jakiś card z markdownem z opisem zadania czy coś
                    ###############################
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='graph-window', figure={}),
                    dbc.Row([
                        dbc.Col([
                            dash_table.DataTable(
                                id='table',
                                columns=[{'id': 'step', 'name': 'step'}, {'id': 'value', 'name': 'value'}],
                                data=[],
                                page_size=10,
                                style_table={'height': '350px', 'overflowY': 'auto'},
                                style_cell_conditional=[
                                    {
                                        'if': {
                                            'column_id': 'step',
                                        },
                                        'width': '10%'
                                    }
                                ],
                                editable=True)
                        ], width={"size": 5, "offset": 3})
                    ])
                ], width=6),
            ])
    ])


@app.callback(Output('stop-button', 'disabled'),
              Output('start-button', 'disabled'),
              Output('tick-component', 'interval'),
              Output('tick-component', 'disabled'),
              Input('start-button', 'n_clicks'),
              Input('stop-button', 'n_clicks'))
def start_loop(start_nclicks, stop_nclicks):
    ctx = dash.callback_context
    if ctx.triggered is not None:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'start-button':
            #             ustaw period do timera i go odpal
            #             po'tem callback timera musi zmieniać ten numerek
            #             inny callback łapie ten numerek, robi krok, wstawia dane do tabeli i do grafu
            return False, True, 0.25 * 1000, False
        else:
            #            wyłącz timer
            return True, False, 0, True


@app.callback(
    Output('table', 'data'),
    Input('tick-component', 'n_intervals'),
    State('table', 'data'))
def interval_tick(n_intervals, rows):
    if n_intervals > 0:
        rows.append({'step': n_intervals, 'value': random.randint(0, 22)})
    return rows


@app.callback(Output('table', 'page_current'),
              Input('table', 'data'),
              Input('table', 'page_size'))
def auto_scroll(data, page_size):
    return int((len(data) - 1) / page_size)


@app.callback(Output('graph-window', 'figure'),
              Input('table', 'data'),
              State('table', 'data'))
def update_graph(tableData, allData):
    if allData:
        fig = go.Figure(go.Scatter(
            x=[i['step'] for i in allData],
            y=[i['value'] for i in allData]
        ))

        return fig
    else:
        raise PreventUpdate


app.run_server(debug=True)
