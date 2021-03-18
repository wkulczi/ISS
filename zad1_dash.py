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
                        dbc.Col(dbc.Input(id='h0-input', type="number", min=0, max=10, step=0.5, value=0, bs_size='sm'),
                                width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("A:"), width=1),
                        dbc.Col(dbc.Input(id='a-input', type="number", min=0, max=10, step=0.5, value=0, bs_size='sm'),
                                width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("Tp"), width=1),
                        dbc.Col(dbc.Input(id='tp-input', type="number", min=0, max=10, step=0.5, value=0, bs_size='sm'),
                                width=4,
                                className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("β:"), width=1),
                        dbc.Col(
                            dbc.Input(id='beta-input', type="number", min=0, max=10, step=0.5, value=0, bs_size='sm'),
                            width=4,
                            className='pl-1'),
                        dbc.Col(html.Div("jednostka"), width=4, className='px-0')
                    ], align="center", className='my-2'),
                    dbc.Row([
                        dbc.Col(html.Div("Qd:"), width=1),
                        dbc.Col(dbc.Input(id='qd-input', type="number", min=0, max=10, step=0.2, value=0, bs_size='sm'),
                                width=4,
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
              Output('h0-input', 'disabled'),
              Output('a-input', 'disabled'),
              Output('beta-input', 'disabled'),
              Output('tp-input', 'disabled'),
              Input('start-button', 'n_clicks'),
              Input('stop-button', 'n_clicks'))
def start_loop(start_nclicks, stop_nclicks):
    ctx = dash.callback_context
    if ctx.triggered is not None:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'start-button':
            return False, True, 0.25 * 1000, False, True, True, True, True
        else:
            #            wyłącz timer
            return True, False, 0, True, False, False, False, False


@app.callback(
    Output('table', 'data'),
    Input('tick-component', 'n_intervals'),
    Input('h0-input', 'value'),
    Input('a-input', 'value'),
    Input('beta-input', 'value'),
    Input('tp-input', 'value'),
    Input('qd-input', 'value'),
    State('table', 'data')
)
def interval_tick(n_intervals, rows, h0, a, beta, tp, qd):
    print("{}, {}, {}, {}, {}".format(h0, a, beta, tp,qd))
    if n_intervals > 0:
        if n_intervals == 1:
            #     policz pierwszy krok
            hn = count_step(h0, tp, qd, beta, a)
        else:
            #     policz reszte krokow
            hn_1 = rows[-1]['value']
            hn = count_step(hn_1, tp, qd, beta, a)
        rows.append({'step': n_intervals, 'value': hn})
    return rows


def count_step(hn, Tp, Qdn, beta, A):
    import math
    return (((-beta * math.sqrt(hn) + Qdn) * Tp) / A) + hn


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
