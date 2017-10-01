import db_helper as db
from googletrans import Translator
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def translate(text, targetLng = 'en'):
	gt = Translator()
	translation = gt.translate(text, dest = targetLng)
		
	return translation.text

def checkSpam(text):
	spam_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
	result = re.findall(spam_pattern, text)
	if len(result) == 0:
		return False
	else:
		return True

def sanitize(text):
	return text.replace(',', ' ')

conn = db.db_connect()

query = 'select about from user_social'

cur = db.doQuery(conn, query)

result = cur.fetchall()


db.db_close(conn)



about_whole = []
about = ""
# gt = Translator()
# row = 724
# for i in result:
# 	#about_whole.append(translate(i[0]))
# 	if (i[0] != None) and (not checkSpam(i[0])):
# 		print(row)
# 		about+=translate(sanitize(i[0]))
# 		about += " "
# 	row+=1




# f = open('about_output.txt', 'wt', encoding='utf-8')
# f.write(about)

f = open('about_output.txt', 'r', encoding='utf-8')
about = f.read()

about = about.lower()
words_about = []

stopw = set(stopwords.words('english'))
stopw.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
stopw.update(['<', '>', '?', '/s', '/', '&', '|', '-', '_', 'æ', '»', '@'])

for w in word_tokenize(about):
	if w not in stopw:
		words_about.append(w)

freq = nltk.FreqDist(words_about)
print(freq.most_common(100))
