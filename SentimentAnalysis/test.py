from SentimentCalculator import SentimentCalculator
import db_helper as db

s = SentimentCalculator()
# s.calcPostSentiment(23)

# text = db.getCommentById(10)
# s.calcSentiment(text)

listOfCom = db.getAllCommentsForPost(347159)
sent = s.calcSummedSentiment(listOfCom)

db.insertSentForPost(347159, sent)