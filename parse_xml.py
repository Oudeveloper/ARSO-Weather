import pandas as pd
from sqlalchemy import create_engine

df = pd.read_xml('tmp/BABNO-POL.xml', xpath="//metData")

#convert df to sqllite table even it does not exist
# engine = create_engine('sqlite:///tmp/BABNO-POL.db', echo=False)
# sqlite_connection = engine.connect()
# sqlite_table = "BABNO-POL"
# df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')
# sqlite_connection.close()


print(df['tsValid_issued_UTC'].head())

