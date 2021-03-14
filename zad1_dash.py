from jupyter_dash import JupyterDash
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

JupyterDash.infer_jupyter_proxy_config()

data = pd.read_csv("untitled.csv")

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Interval(
            id='interval-component',
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
                    ])
                    ###############################
                    # tutaj jakiś card z markdownem z opisem zadania czy coś
                    ###############################
                ], width=6),
                dbc.Col([
                    dcc.Graph(),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'))
                ], width=6),
            ])
    ])


@app.callback(Output('stop-button', 'disabled'),
              Output('start-button', 'disabled'),
              Input('start-button', 'n_clicks'),
              Input('stop-button', 'n_clicks'))
def start_loop(start_nclicks, stop_nclicks):
    ctx = dash.callback_context
    if ctx.triggered is not None:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'start-button':
            #             ustaw period do timera i go odpal
            #             potem callback timera musi zmieniać ten numerek
            #             inny callback łapie ten numerek, robi krok, wstawia dane do tabeli i do grafu
            return False, True
        else:
            #            wyłącz timer
            return True, False


app.run_server(debug=True)