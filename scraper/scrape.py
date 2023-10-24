import psycopg2
import pandas as pd
from bs4 import BeautifulSoup
import requests
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

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
MYSQL_HOST = os.environ.get('MYSQL_HOST')

ENGINE = create_engine(f'postgresql+psycopg2://postgres:unhackable@{POSTGRES_HOST}:5432/postgres')

BATHS = []
BEDS = []
PRICE = []
TOILETS = []
TITLE = []
CONTACT = []
PID = []
LOCATION = []

CITIES = [ "Maitama", "Lugbe", "Apo", "Jahi", "Garki 1", "Garki 2", "Mabushi", 
          "Guzape", "Katampe Main", "Katampe Ext", "Lokogoma", "Wuye", "Jabi", "Life Camp", "Asokoro",
          "Kado", "Dakwo", "Idu", "Wuse 1", "Wuse 2", "Utako", "Kubwa", "Mpape", ]


df = pd.DataFrame()

def get_city(location, cities):
    for city in cities:
        if city in location:
            return city
    return None

def fetch_page(output_df, url, page=None):
    if page != None and page > 0:
        url += f'?page={page}'
        
    text = requests.get(url).content
    soup = BeautifulSoup(text, 'lxml')
    props = soup.select('.listings-property')
    
    for i in props:
        
        try:
            title = i.select('.listings-property-title2')[0].get_text()
        except IndexError:
            title = None
            #title = i.select('.listings-property-title')[0].get_text()
        #print("\ntitle\n, ", title)
        TITLE.append(title)
        
        try:
            price = i.select('.n50')[0].get_text()
        except IndexError:
            try:
                price = i.select('.listings-price')[0].get_text()
                print("price", price)
            except IndexError:
                price = i.select('h3')[0].get_text()
        #print("\nprice\n, ", price)
        PRICE.append(price)
        
        try:
            contact = i.select('.phone-icon')[0].get_text().split()[0]
        except IndexError:
            contact = None
        #print("\ncontact\n, ", contact)
        CONTACT.append(str(contact))

        try:
            location = i.select('h4')[1].get_text()
        except IndexError:
            location = None
            
        #print("\nlocation\n, ", location)
        LOCATION.append(location)
        
        try:
            pid = i.select('h2')[0].get_text().split()[1]
        except IndexError:
            pid = None
       # print("\nPID\n, ", pid)
        PID.append(pid)
        
        try:
            features = i.select('.fur-areea span')
            if features == []:
                features = [None, None, None]
        except:
            features = [None, None, None]
        #print("Features : ", features)
        
        if features != [None, None, None]:
            features = [ i.get_text() for i in features]
        
        beds = features[0]
        BEDS.append(beds)
        
        baths = features[1]
        BATHS.append(baths)
        
        toilets = features[2]
        TOILETS.append(toilets)
    return soup
        
        
def fetch_all_pages(output_df, url):
    page = 0
    while True:
        print("Fetching for page ", page)
        
        print( "url : ", url + f'?page={page}' )
        soup = fetch_page(output_df, url, page)
        #print(soup)
        try:
            next_page = soup.find_all(attrs={'alt': 'view next property page'})
            page += 1 
        except AttributeError:
            raise AttributeError
        if page == 3:# 355:
            break

def count_(s):
    if s != None:
        return s.split()[0]
    return None


def clean_data(state):
    print("Cleaning data")
    DF = {
        'price': PRICE,
        'title': TITLE,
        'contact': CONTACT,
        'toilets': TOILETS,
        'beds': BEDS,
        'baths': BATHS,
        'PID': PID,
        'location': LOCATION
    }
    
    x = pd.DataFrame(DF)
    x['beds'] = x['beds'].apply(lambda x: count_(x))
    x['baths'] = x['baths'].apply(lambda x: count_(x))
    x['toilets'] = x['toilets'].apply(lambda x: count_(x))
    
    #non_rent = x[x['price'].str.contains('year') == False]
    try:
        rent = x[x['price'].str.contains('year') == True]
    except:
        rent = x

    rent['rent'] = rent['price'].apply(lambda x: x.split()[1][:-5].replace(',',''))
    
    rent = rent[rent['beds'] != 'beds']
    rent = rent[rent['baths'] != 'baths']
    rent = rent[rent['toilets'] != 'Toilets']
    
    rent = rent.drop('price', axis=1)
    
    rent['city'] = rent['location'].apply(lambda x : get_city(x, CITIES))
    
    rent = rent[["toilets", "beds", "baths", "rent", "city"]]
    
    rent[['baths', 'beds', 'toilets', 'rent']] = rent[['baths', 'beds', 'toilets', 'rent']].astype(int)
    
    rent['room_index'] = rent['beds'] + rent['baths'] + rent['toilets']

    rent['state'] = state.lower()
    
    print(rent.head())
    rent.to_csv(f'properties_{state.lower()}_rent.csv')
    rent.to_sql(f'properties_{state.lower()}_rent.sql', con=ENGINE)
    
    return rent
   
    


def city_data(city):
    return rent[rent['city'] == city]


def get_state_data(state):
    print("Fetching state data...")
    url = f'https://www.propertypro.ng/property-for-rent/in/{state.lower()}/'
    
    fetch_all_pages(df, url)
    
    return clean_data(state)



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

    df.to_sql('properties', con=engine)

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



#print( fetch_page(df, 'https://www.propertypro.ng/property-for-rent/in/abuja/', 2) )
rent = get_state_data('abuja')

push_to_postgres_db()
