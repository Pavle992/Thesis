import db_helper as db 
import pandas as pd
conn = db.db_connect()

query = 'select * from im_commento'

cur = db.doQuery(conn, query)

results = cur.fetchall()

df = pd.DataFrame(results)

print(df.head())

# for cnt in cur.fetchall()[:10]:
#     print(cnt[0].encode('utf-8'))

db.db_close(conn)