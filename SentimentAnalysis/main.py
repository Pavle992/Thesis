# -*- coding: utf-8 -*-
from SentimentCalculator import SentimentCalculator
import db_helper as db
import json

s = SentimentCalculator()


text = db.getCommentById(8)
s.calcSentiment(text)

# listOfCom = db.getAllCommentsForPost(335758)
# sent = s.calcSummedSentiment(listOfCom)

# db.insertSentForPost(335758, sent)

# with open('./res/emoji-sentiment.json', 'r') as fp:
#     emojiSentiment = json.load(fp)

# print(s.emojiSentData['1f602'])

