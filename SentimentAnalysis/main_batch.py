# -*- coding: utf-8 -*-
from SentimentCalculator import SentimentCalculator
import db_helper as db

conn = db.db_connect()

query = "select distinct idpost from im_commento"
cur = db.doQuery(conn, query)

results = cur.fetchall()

s = SentimentCalculator()

for r in results[:10]:
    listOfCom = db.getAllCommentsForPost(r[0])
    sent = s.calcSummedSentiment(listOfCom)
    db.insertSentForPost(r[0], sent)
