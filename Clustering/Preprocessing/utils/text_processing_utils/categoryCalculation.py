from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from googletrans import Translator

class CategorySimilarity(object):

    def __init__(self, categories=['fashion', 'beauty', 'accessories', 'lifestyle', 'car', 'blog', 'food', 'luxury', 'hair', 'design']):

        self.categories = categories
        self.similarity = {}
        self.count = {}

    def __translate(self, text, targetLng = 'en'):
        try:
            gt = Translator()
            translation = gt.translate(text, dest = targetLng)
            return translation.text 
        except Exception as ex:
            return text

    def __resetSimilarities(self):
        for c in self.categories:
            self.similarity[c] = 0
            self.count[c] = 0        
        return

    def getStringCategory(self, stringParam):

        if stringParam is None:
            return ""

        translatedString = self.__translate(stringParam.lower())

        tokens = word_tokenize(translatedString)

        self.__resetSimilarities()

        for word1 in self.categories:
            for word2 in tokens:
                wordFromList1 = wordnet.synsets(word1)
                wordFromList2 = wordnet.synsets(word2)
                if wordFromList1 and wordFromList2:
                    s = wordFromList1[0].wup_similarity(wordFromList2[0])
                    if (s != None):
                    	self.similarity[word1] += s
                    	self.count[word1] += 1
        
        # print(tokens)
        # print(self.similarity)
        # print(self.count)
        for c in self.categories:        	
            if self.count[c] == 0:
                self.similarity[c] = 0
            else:        
                self.similarity[c] /= self.count[c]

        #category to assign
        category = max(self.similarity.items(), key=lambda x: x[1])[0]
        
        return category

    def getTokensCategory(self, tokensParam):

        if len(tokensParam) == 0:
            return ""

        self.__resetSimilarities()

        for word1 in self.categories:
            for word2 in tokensParam:
                wordFromList1 = wordnet.synsets(word1)
                wordFromList2 = wordnet.synsets(word2)
                if wordFromList1 and wordFromList2:
                    s = wordFromList1[0].wup_similarity(wordFromList2[0])
                    if (s != None):
                        self.similarity[word1] += s
                        self.count[word1] += 1
        
        for c in self.categories:   
            if self.count[c] == 0:
                self.similarity[c] = 0
            else:         
                self.similarity[c] /= self.count[c]

        #category to assign
        category = max(self.similarity.items(), key=lambda x: x[1])[0]
        
        return category 