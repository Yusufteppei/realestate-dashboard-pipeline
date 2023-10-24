import os
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 

user = os.environ.get('POSTGRES_USER')
db = os.environ.get('POSTGRES_DB')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')

conn = psycopg2.connect(
        database=db,
        user=user,
        password=password,
        host=host,
        port=5432
    )

engine = create_engine(f'postgresql+psycopg2://postgres:unhackable@{host}:5432/postgres')

#cursor = conn.cursor()
#cursor.execute("SELECT * FROM properties")

df = pd.read_sql_table("properties", con=engine)

MEAN_PRICE = df['price'].mean()
MEDIAN_PRICE = df['price'].median()



conn.close()
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
