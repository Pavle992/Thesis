import pandas as pd 
import numpy as np 

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select

engine = create_engine('mysql+pymysql://root:@localhost:3306/sentiment_db')

connection = engine.connect()

metadata = MetaData()

comments = Table('im_commento', metadata, autoload=True, autoload_with=engine)

stmt = select([comments])

results = connection.execute(stmt).fetchall()

df = pd.DataFrame(results, columns=comments.columns)

print(df.head())
print(df.info())

# print(engine.table_names())