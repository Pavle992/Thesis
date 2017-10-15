# -*- coding: utf-8 -*-
import db_helper as db
import re
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


class SentimentCalculator:
	
	
	def __init__(self):
		with open('./res/emoji-sentiment.json', 'r') as fp:
			self.emojiSentData = json.load(fp)
		
	def __translate(self, text, targetLng = 'en'):
		gt = Translator()
		translation = gt.translate(text, dest = targetLng)
		
		return translation.text

	def __getSentiment(self, text):
		analyzer = SentimentIntensityAnalyzer()
		result = analyzer.polarity_scores(text)

		return result

	def __getEmojiSentiment(self, emojis):

		if len(emojis) == 0:
			return 0

		result = 0
		sameEmojiCount = 1
		prevEmUnicode = ""
		i = 0
		increas = False

		for em in emojis:

			emUnicode = hex(ord(em))[2:].upper()
			if (i != 0):
				
				if (emUnicode == prevEmUnicode):

					sameEmojiCount += 1
	
					if (sameEmojiCount % 3 == 0):
						increas = True
				else:
					sameEmojiCount = 1


			prevEmUnicode = emUnicode
			i += 1

			try:
				result += self.emojiSentData[emUnicode]

				if (increas):
					if (result > 0):
						result+=0.5
					else:
						result-=0.5

					increas = False
			except Exception:
				return 0
			
		
		result /= len(emojis)

		if (result > 1):
			return 1

		return result

	def __getCombinedSentiment(self, textSent, emojiSent):
		emojiRegularization = 1 #1 if very important

		if textSent != 0 and emojiSent != 0:
			comb = (textSent + emojiRegularization * emojiSent)/2
		elif textSent == 0 and emojiSent != 0:
			comb = emojiSent
		elif textSent != 0 and emojiSent == 0:
			comb = textSent
		else:
			comb = textSent

		return comb

	def __sanitize(self, text):
		return text.replace(',', '')

	def __calcSentiment(self, text):

		print('################################################')

		emoji_pattern = re.compile(u'['
			u'\U0001F300-\U0001F64F'
    		u'\U0001F680-\U0001F6FF'
    		u'\u2600-\u26FF\u2700-\u27BF]', 
    		re.UNICODE)
		
		postContent = {}
		 
		m = emoji_pattern.findall(text)
		postContent['emojis'] = m
		postContent['text'] = re.sub(emoji_pattern, '',text)
		postContent['text'] = self.__sanitize(postContent['text'])

		if (postContent['emojis']):
			print('emojis found: %s' %postContent['emojis'])
		print('text found: %s' %postContent['text'])

		postContent['text'] = self.__translate(postContent['text'])
		
		print('translated text: %s' %postContent['text'])

		sent = {}

		sent['text'] = self.__getSentiment(postContent['text'])
		print('sentiment for text: %s' %sent['text']['compound'])
		sent['emojis'] = self.__getEmojiSentiment(postContent['emojis'])
		print('sentiment for emojis: %s' %sent['emojis'])
		sent['combined'] = self.__getCombinedSentiment(sent['text']['compound'], sent['emojis'])
		print('sentiment combined: %s' %sent['combined'])
		print('################################################')

		return sent
	
	def calcSummedSentiment(self, listOfComments):
		numOfRows = len(listOfComments)

		summedSent = {'text' : 0.0, 'emojis': 0.0, 'combined': 0.0}

		for comment in listOfComments:
			print(comment)
			if (self.checkSpam(comment)):
				numOfRows = numOfRows - 1;
				continue

			sentScore = self.__calcSentiment(comment)
			summedSent['text'] += sentScore['text']['compound']
			summedSent['emojis'] += sentScore['emojis']
			summedSent['combined'] += sentScore['combined']

		if (numOfRows != 0):
			summedSent['text'] /= numOfRows
			summedSent['emojis'] /= numOfRows
			summedSent['combined'] /= numOfRows

		print(summedSent)
		return summedSent

	def checkSpam(self, commentText):
	    spam_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
	    result = re.findall(spam_pattern, commentText)
	    if len(result) == 0:
	        return False
	    else:
	        return True
	

