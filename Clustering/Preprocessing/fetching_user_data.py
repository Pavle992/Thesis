from utils.db_utils.base_db import Database

# Global key variables
hostname = 'localhost'
port_num = 3306
username = 'root'
password = ''
db_name = 'sentiment_db'
fb_token = "EAAEvqXBRTZBgBAFdJHhbI9oZAcbaIBuREQRSZA7gPeW38fSiSU3Ol4PhK8kuWpvq5IsCR9BtBJggjEVef715ZCGrRKkmEoofUDxMoUQNyH0psZA4qG3xopD0qjKsd2vIWmH3nbovFQH9aFIT2FZAEZBqZBURT0xUJMkZD"

# Connecting to DB
comment_db = Database(host=hostname, port=port_num, user=username, passwd=password, db=db_name)
comment_db.connect()
results = comment_db.fetch_all(select='id, content, from_id, idpost', from_clause='im_commento',data_as_dataframe=True)
results.set_index('id', inplace=True)

# Taking user ids
user_ids = list(set(results.iloc[:, 1].values)) 
user_ids = sorted(user_ids, reverse=True) 

user_post = dict(results.iloc[:,1:3].values)

# FB API
from utils.api_utils.facebook_api import FacebookAPI 
fb = FacebookAPI(token=fb_token)
fb.connect()

# Inserting users data in db
for counter, uid in enumerate(user_ids[204300:]):
    fu = fb.request(ids=[uid])
    if fu is not None:
        fu['idpost'] = str(user_post[uid])
        comment_db.insert(table='user_social', column_value=fu)
        print('#########', counter)
        print(fu)

print("FB-user data fetching finished")
