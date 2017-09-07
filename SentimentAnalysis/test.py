# -*- coding: utf-8 -*-
from SentimentCalculator import SentimentCalculator
import db_helper as db
import json
import sys

s = SentimentCalculator()

text = db.getCommentById(716)
sent = s.calcSentiment(text)

# db.insertSentForPost(postID, sent)

# sisi diffic sporcar , vosevo dervila così in questa Modo,,,
# Virgoline virgoline cccccc
