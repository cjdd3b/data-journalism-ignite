import nltk
import math
import re
from operator import itemgetter

########## HELPER FUNCTIONS ##########

def word_count(doc):
  return len(doc)

def freq(word, doc):
  return doc.count(word)

def tf(word, doc):
  return (freq(word, doc) / float(word_count(doc)))

def num_docs_containing(word,doclist):
  count = 0
  for doc in doclist:
    if freq(word, doc) > 0:
      count += 1
  return count

def idf(word, doclist):
  return math.log(len(doclist) / num_docs_containing(word, doclist))

def tfidf(word, doc, doclist):
  return (tf(word, doc) * idf(word, doclist))


########## MAIN ##########

dj_text = open('datajournalism.txt', 'r').read().lower()
dj_words = re.findall(r'\w+', dj_text, flags = re.UNICODE | re.LOCALE) 
dj_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), dj_words)

ds_text = open('datascience.txt', 'r').read().lower()
ds_words = re.findall(r'\w+', ds_text, flags = re.UNICODE | re.LOCALE) 
ds_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), ds_words)

doclist = []
doclist.append(dj_important_words)
doclist.append(ds_important_words)

dj_tfidf = {}
for word in doclist[0]:
    dj_tfidf[word] = tfidf(word, doclist[0], doclist)

print '---------- Data journalism terms ----------'
for term in sorted(dj_tfidf.items(), key=itemgetter(1), reverse=True)[:50]:
    print term

ds_tfidf = {}
for word in doclist[1]:
    ds_tfidf[word] = tfidf(word, doclist[1], doclist)

print '---------- Data science terms ----------'
for term in sorted(ds_tfidf.items(), key=itemgetter(1), reverse=True)[:50]:
    print term

