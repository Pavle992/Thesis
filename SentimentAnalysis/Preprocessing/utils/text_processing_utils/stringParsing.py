from textblob import TextBlob
from googletrans import Translator

class StringTokenizer(object):

	def __init__(self):
		self.text = None
		self.blob = None

	def __translate(self, text, targetLng = 'en'):
		try:
			gt = Translator()
			translation = gt.translate(text, dest = targetLng)
			return translation.text	
		except Exception as ex:
			return text	

	def setString(self, text):
		if text is not None:
			self.text = self.__translate(text)
			self.blob = TextBlob(self.text)

	def getNounPhrases(self):
		# print(self.blob.noun_phrases)
		shorterNouns = list(filter(lambda x: len(x)<25, self.blob.noun_phrases))
		return shorterNouns
