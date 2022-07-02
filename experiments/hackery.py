__author__ = 'mrittha'

import gensim
import numpy as np
import nltk.chunk
import text_processor.sentence_tagger as st
import chunk_parser

text = 'A star is a massive ball of plasma  held together by gravity.  It radiates energy because of the nuclear reactions inside it'
print chunk_parser.treebank[0]

sentences = st.get_sentences(text)
print sentences

tags = st.tag_sentence(sentences[0])
print tags
pattern = "NP: {<DT>?<JJ>*<NN>}"
NPChunker = nltk.RegexpParser(pattern)
result = NPChunker.parse(tags)
print result
LNPChunker=chunk_parser.get_NP_chunker()
result=LNPChunker.parse(tags)
print result
result.draw()
print result.chomsky_normal_form()






# model = gensim.models.Word2Vec.load_word2vec_format("C:/temp/GoogleNews-vectors-negative300.bin", binary=True)

# for i in range(300):
#    probe = np.zeros((300,))
#    probe[i] = 1.0
#    print i, model.most_similar(positive=[probe], negative=[], topn=10)
#    probe[i] = -1.0
#    print i, model.most_similar(positive=[probe], negative=[], topn=10)
