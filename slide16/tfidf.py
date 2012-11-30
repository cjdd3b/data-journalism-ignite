import nltk
import math
import re
from operator import itemgetter

########## HELPER FUNCTIONS ##########

def word_count(doc):
  '''
  Returns the number of words in a document. Expects the document to be
  presented as a list of words.
  '''
  return len(doc)

def freq(word, doc):
  '''
  Returns the frequency of a word in a document.
  '''
  return doc.count(word)

def tf(word, doc):
  '''
  Returns the term frequency of the word in the document, which is to
  say the percent of the document that is made up by that word.
  '''
  return (freq(word, doc) / float(word_count(doc)))

def num_docs_containing(word, doclist):
  '''
  Returns the number of documents containing the input word.
  '''
  count = 0
  for doc in doclist:
    if freq(word, doc) > 0:
      count += 1
  return count

def idf(word, doclist):
  '''
  Returns the inverse document frequency of the word across the corpus.
  '''
  return math.log(len(doclist) / num_docs_containing(word, doclist))

def tfidf(word, doc, doclist):
  '''
  Calculates TF-IDF, which is just tf * idf.
  '''
  return (tf(word, doc) * idf(word, doclist))


########## MAIN ##########

# Clean up the input text as we have in several previous scripts. Open the document, convert
# to lowercase, ignore punctuation and cut out stopwords.
dj_text = open('datajournalism.txt', 'r').read().lower()
dj_words = re.findall(r'\w+', dj_text, flags = re.UNICODE | re.LOCALE) 
dj_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), dj_words)

# Do the same for the data science text
ds_text = open('datascience.txt', 'r').read().lower()
ds_words = re.findall(r'\w+', ds_text, flags = re.UNICODE | re.LOCALE) 
ds_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), ds_words)

# Create the "corpus" of all documents, which in this case is just two documents: the data journalism
# handbook and the data science article.
doclist = []
doclist.append(dj_important_words)
doclist.append(ds_important_words)

# Calculate and print out TF-IDF weights for the data journalism text.
# The higher the weight, the more significant that term is to this particular
# text.
dj_tfidf = {}
for word in doclist[0]:
    dj_tfidf[word] = tfidf(word, doclist[0], doclist)

print '---------- Data journalism terms ----------'
for term in sorted(dj_tfidf.items(), key=itemgetter(1), reverse=True)[:50]:
    print term

# Do the same for the data science text
ds_tfidf = {}
for word in doclist[1]:
    ds_tfidf[word] = tfidf(word, doclist[1], doclist)

print '---------- Data science terms ----------'
for term in sorted(ds_tfidf.items(), key=itemgetter(1), reverse=True)[:50]:
    print term

