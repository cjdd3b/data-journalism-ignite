import nltk
import re
import operator
import math

dj_text = open('datajournalism.txt', 'r').read().lower()
dj_words = re.findall(r'\w+', dj_text, flags = re.UNICODE | re.LOCALE) 
dj_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), dj_words)

ds_text = open('datascience.txt', 'r').read().lower()
ds_words = re.findall(r'\w+', ds_text, flags = re.UNICODE | re.LOCALE) 
ds_important_words = filter(lambda x: x not in nltk.corpus.stopwords.words('english'), ds_words)

bothdocs = {}
for word in dj_important_words:
    if word in ds_important_words:
        # Janky back-of-the-napkin metric designed to heavily weight terms that occur often in
        # both documents in relatively even proportions. I have no doubt there is a better and
        # more established way of doing this, but part of data journalism is playing around with
        # your data to see what works. And for these purposes, it works just fine.
        bothdocs[word] = (dj_important_words.count(word) + ds_important_words.count(word)) \
            / (abs((dj_important_words.count(word) - ds_important_words.count(word))) + 1.0) \
                * math.log((dj_important_words.count(word) + ds_important_words.count(word)))

terms = sorted(bothdocs.iteritems(), key=operator.itemgetter(1))
terms.reverse()

for term in terms[:25]:
    print term