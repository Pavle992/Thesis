import db_helper as db 

conn = db.db_connect()

query = 'select content from im_commento where idpost=346036'

cur = db.doQuery(conn, query)

for cnt in cur.fetchall():
    byte_array = str.encode(cnt[0])
    # print(str(byte_array, 'utf-8'))
    print(byte_array.decode('utf-8'))

db.db_close(conn)