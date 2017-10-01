from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union
from nltk.stem import PorterStemmer
import nltk
sentence = "Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike."

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

# print(sent_tokenize(sentence))
# print(word_tokenize(sentence))

# for w in word_tokenize(sentence):
# 	print(w)

# filtered = []
# stop_words = stopwords.words("english")

# for w in word_tokenize(sentence):
# 	if w not in stop_words:
# 		filtered.append(w)

# print(filtered)

# ps = PorterStemmer()

# example_words = ["python", "pythoner", "pythoning", "pythoned"]

# for w in example_words:
# 	print(ps.stem(w))

# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# tokenized = custom_sent_tokenizer(sample_text)

tokenized = sent_tokenize(sample_text)

def pos_content():
	try:
		for s in tokenized:
			words = word_tokenize(s)
			tagged = nltk.pos_tag(words)
			
			#named entity recognition

			namedEnt = nltk.ne_chunk(tagged)
			namedEnt.draw()

	except Exception as e:
		print(str(e))

pos_content()


