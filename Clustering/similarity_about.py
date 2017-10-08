import db_helper as db
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

categories = ['fashion', 'beauty', 'accessories', 'lifestyle', 'car', 'blog', 'food', 'luxury', 'hair', 'design']


conn = db.db_connect()
query = 'select about from user_social where id=%d' %780
cur = db.doQuery(conn, query)
result = cur.fetchone()
db.db_close(conn)


tokens = word_tokenize(result[0].lower())
print(tokens)
similarity = {}
count = {}

for c in categories:
	similarity[c] = 0
	count[c] = 0

for word1 in categories:
    for word2 in tokens:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
            if (s != None):
            	similarity[word1] += s
            	count[word1] += 1

print(count)           	
for c in categories:
	
	similarity[c] /= count[c]

#category to assign
category = max(similarity, key=lambda i: similarity[i])
print(category)
