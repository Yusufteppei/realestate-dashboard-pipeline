import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlalchemy

user = os.environ.get('POSTGRES_USER')
db = os.environ.get('POSTGRES_DB')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')

engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:5432/db")

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1("Dashboard", style={'textAlign': 'center'}),

    dcc.Graph()
])

if __name__=="__main__":
    app.run_server(debug=True)
