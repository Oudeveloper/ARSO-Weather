import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import os
from sql_queries import *
import logging
from ETL import log_etl


def get_credentials():
    try:
        with open('credentials.txt', 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except Exception as e:
        print(e)
        logging.error(e)
        exit()

#Create database and table
@log_etl
def create_database_and_table():
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
    #read all files from tmp folder and make a list of the name without extension
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

def main():
    if not os.path.exists('tmp'): #check if tmp folder exists
        print('tmp folder does not exist')
        exit()
    df = pd.read_xml('tmp/BABNO-POL.xml', xpath="//metData")
    print(df['tsValid_issued_UTC'].head())
    create_database_and_table()
    insert_city_data()

if __name__ == '__main__':
    main()


#convert df to sqllite table even it does not exist
# engine = create_engine('sqlite:///tmp/BABNO-POL.db', echo=False)
# sqlite_connection = engine.connect()
# sqlite_table = "BABNO-POL"
# df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')
# sqlite_connection.close()

