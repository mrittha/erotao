__author__ = 'mrittha'

import nltk

for d in nltk.corpus.brown.tagged_words()[:100]:
    print d