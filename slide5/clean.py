import nltk
import re

text = open('precision_journalism.txt', 'r').read().lower()
out = open('clean_pj.txt', 'a')

words = re.findall(r'\w+', text, flags = re.UNICODE | re.LOCALE) 
important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), words)

out.write(' '.join(important_words))
