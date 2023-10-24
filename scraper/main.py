import psycopg2
import pandas as pd
import os
import mysql.connector
from sqlalchemy import create_engine
   

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
MYSQL_HOST = os.environ.get('MYSQL_HOST')

COPY_CSV_QUERY = """
    COPY properties( toilets, beds, baths, rent, city)
    FROM 'properties_abuja_rent.csv'
    DELIMITER ','
    CSV HEADER;
"""

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS properties ( toilets SMALLINT, beds SMALLINT, baths SMALLINT, rent INT, city VARCHAR(128));

"""

def push_to_postgres_db():

    df = pd.read_csv('properties_abuja_rent.csv')
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="unhackable",
        host=POSTGRES_HOST,
        port=5432
    )
    engine = create_engine(f'postgresql+psycopg2://postgres:unhackable@{POSTGRES_HOST}:5432/postgres')

    
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS properties")
    conn.commit()

    x = df.to_sql('properties', con=engine)

    print("to sql", x)
    conn.close()


def push_to_mysql_db():
    conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user="mysql",
            password="unhackable"
    )

    cursor = conn.cursor()

    #   CREATE TABLE IF NOT EXISTS
    cursor.execute(CREATE_TABLE_QUERY)

    #   PUSH DATA
    cursor.execute(COPY_CSV_QUERY)


push_to_postgres_db()
