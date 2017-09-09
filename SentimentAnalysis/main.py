# -*- coding: utf-8 -*-
from SentimentCalculator import SentimentCalculator
import db_helper as db
import json
import sys

s = SentimentCalculator()

postID = int(sys.argv[1])

listOfCom = db.getAllCommentsForPost(postID)
sent = s.calcSummedSentiment(listOfCom)

db.insertSentForPost(postID, sent)



