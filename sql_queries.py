
#Create database
database_name = "WeatherData180"
database_create =f"CREATE DATABASE IF NOT EXISTS {database_name};"""

#Create table
table_city_create = """CREATE TABLE IF NOT EXISTS cities (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    city_name VARCHAR(255) NOT NULL unique);"""

table_weather_create = """CREATE TABLE weather (
    id INT AUTO_INCREMENT,
    datetime DATETIME,
    city_id INT,
    temperature DECIMAL(5,2),
    humidity smallint,
    pressure smallint,
    wind_speed_km smallint,
    precipitation DECIMAL(5,2),
    solar_radiation smallint,
    diffuse_solar_radiation smallint,
    PRIMARY KEY (id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    UNIQUE KEY (city_id, datetime)
    );"""

#Insert data
data_city_insert = """INSERT INTO cities (city_name) VALUES (%s);"""
data_weather_insert = """INSERT INTO weather (city_id, datetime,  temperature)
    VALUES (%s, %s, %s);"""

#Select data
data_city_select = """SELECT * FROM cities WHERE city_name = %s;"""
data_cityId_select = """SELECT id FROM cities WHERE city_name = %s;"""

