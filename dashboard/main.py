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

print(df.head())
MEAN_PRICE = df['rent'].mean()
MEDIAN_PRICE = df['rent'].median()
PROPERTY_COUNT = df.shape[0]



conn.close()
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(

    children=[

        html.H1("Dashboard", style={'textAlign': 'center'}),

        dbc.Row(
            dbc.Col(
                dbc.Row(
                    dbc.Col(
                        html.Div("Mean Price"),
                        html.Div(MEAN_PRICE)
                    )
                )
            ),
            
            dbc.Col(
                dbc.Row(
                    dbc.Col(
                        html.Div("Median Price"),
                        html.Div(MEDIAN_PRICE)
                    )
                )
            ),

            dbc.Col(
                dbc.Row(
                    dbc.Col(
                        html.Div("Properties"),
                        html.Div(PROPERTY_COUNT)
                    )
                )
            ),
        ),
        
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
                dbc.Col(
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': [1,2,3], 'y': [1,2,3], 'type': 'bar', 'name':'Graph'}
                            ]
                        }
                    )
                ),
                
            ]
        ),    

        

    ]
)

if __name__=="__main__":
    app.run_server(host="0.0.0.0", debug=True)
