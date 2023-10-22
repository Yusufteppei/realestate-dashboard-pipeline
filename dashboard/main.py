import os
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import sqlalchemy

user = os.environ.get('POSTGRES_USER')
db = os.environ.get('POSTGRES_DB')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')

engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:5432/db")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = html.Div(

    children=[

        html.H1("Dashboard", style={'textAlign': 'center'}),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1,2,3], 'y': [1,2,3], 'type': 'bar', 'name':'Graph'}
                        ]
                    }
                ),
                ),
                dbc.Col(
                    dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1,2,3], 'y': [1,2,3], 'type': 'bar', 'name':'Graph'}
                        ]
                    }
                )
                ),
                dbc.Col(),
                
                   
            ]
        ),    

        

    ]
)

if __name__=="__main__":
    app.run_server(host="0.0.0.0", debug=True)
