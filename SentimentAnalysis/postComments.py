# -*- coding: utf-8 -*-

import db_helper as db 
import pandas as pd
import binascii
import re

conn = db.db_connect()

query = 'select content from im_commento where id=22'

cur = db.doQuery(conn, query)

results = cur.fetchone()
print(results[0])

for w in results[0]:
	print( "0x%x"%ord(w))

emoji_pattern = re.compile(u'['
    u'\U0001F300-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\u2600-\u26FF\u2700-\u27BF]+', 
    re.UNICODE)
p = re.compile(emoji_pattern)
m = p.search(results[0])
print(m.group())

db.db_close(conn)