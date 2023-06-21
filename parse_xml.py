import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import os
from sql_queries import *
import logging
from ETL import log_etl
from  datetime import datetime

def get_credentials():
    """read credentials of the database from credentials.txt file:
    host
    user
    password
    """
    try:
        with open('credentials.txt', 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except Exception as e:
        print(e)
        logging.error(e)
        exit()

@log_etl
def create_database_and_table():
    """Create database and table if not exists"""
    connection = None
    try:
        host, user, password = get_credentials()
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(database_create)
            cursor.execute(f"USE {database_name}")
            cursor.execute(table_city_create)
            cursor.execute(table_weather_create)
            print("Database and table created successfully")
            logging.info('Database and table created successfully')
    except Error as e:
        print(f"The error '{e}' occurred")
        logging.error(e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
@log_etl
def insert_city_data():
    """read all files from tmp folder and make a list of the name without extension
    check if city already exists in the table, if not insert it"""
    connection = None
    try:
        host, user, password = get_credentials()
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            city_names = [name.split('.')[0] for name in os.listdir('tmp') if os.path.isfile(os.path.join('tmp', name))]
            print (city_names)
            cursor.execute(f"USE {database_name}")
            for city in city_names:
                cursor.execute(data_city_select, (city,))
                if cursor.fetchone() is not None: #if city already exists in the table ignore it
                    print(f"City {city} already exists")
                    logging.info(f"City {city} already exists")
                    city_names.remove(city)
                    continue
                cursor.execute(data_city_insert, (city,))
                print(f"City {city} inserted successfully")
                logging.info(f"City {city} inserted successfully")
            connection.commit()
            print("Data inserted successfully")
            logging.info('Data inserted successfully')

    except Error as e:
        print(f"The error '{e}' occurred")
        logging.error(e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def find_city_id(city):
    """find city id from the table cities based on city name"""
    connection = None
    try:
        host, user, password = get_credentials()
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"USE {database_name}")
            cursor.execute(data_cityId_select, (city,))
            city_id = cursor.fetchone()[0]
            return city_id
    except Error as e:
        print(f"The error '{e}' occurred")
        logging.error(e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

@log_etl
def xml_parser(file):
    """parse xml file and return a dataframe with the following columns:
    datetime, temperature, city_id, humidity, wind_speed_km, pressure,
    precipitation, solar_radiation, diffuse_solar_radiation"""

    df = pd.read_xml(f'tmp/{file}', xpath="//metData")
    city_name = file.split('.')[0]
    df = df[['tsValid_issued_UTC', 't','rh','ff_val_kmh','p','tp_1h_acc','gSunRad','diffSunRad']]
    #convert datetime so it can be inserted into the database
    df['tsValid_issued_UTC'] = pd.to_datetime(df['tsValid_issued_UTC'], dayfirst=True)
    df['tsValid_issued_UTC'] = df['tsValid_issued_UTC'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['city_id'] = find_city_id(city_name)
    df = df.rename(columns={'tsValid_issued_UTC': 'datetime',
                            't': 'temperature',
                            'city_id': 'city_id',
                            'rh': 'humidity',
                            'ff_val_kmh': 'wind_speed_km',
                            'p': 'pressure',
                            'tp_1h_acc': 'precipitation',
                            'gSunRad': 'solar_radiation',
                            'diffSunRad': 'diffuse_solar_radiation'
                            })
    logging.info(f'{file} parsed successfully')
    return df

@log_etl
def insert_weather_data():
    """read all files from tmp folder and insert data into weather table """
    for file in os.listdir('tmp'):
        if not file.endswith('.xml'):           #check if file is xml
            continue
        df=xml_parser(file)

        host, user, password = get_credentials()
        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database_name}', echo=False)
        try:
            df.to_sql(name='weather', con=engine, if_exists='append', index=False)
            print(f'{file} inserted successfully')
            logging.info(f'{file} inserted successfully')
        except Exception as e:
            if 'Duplicate entry' in str(e):
                print(f'duplicate entry in {file} passed')
                logging.info(f'duplicate entry in {file}')
                continue
            else:
                print(e)
                logging.error(e)
        finally:
            engine.dispose()
    logging.info('weather table updated successfully')

def main():
    if not os.path.exists('tmp'): #check if tmp folder exists
        print('tmp folder does not exist')
        logging.error('tmp folder does not exist')
        exit()
    create_database_and_table()
    insert_city_data()
    insert_weather_data()

if __name__ == '__main__':
    main()