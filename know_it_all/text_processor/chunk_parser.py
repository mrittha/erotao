import nltk

from nltk.corpus import conll2000
import nltk.corpus as nc
test_sents = conll2000.chunked_sents('test.txt') #chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt') #chunk_types=['NP'])
treebank=nltk.corpus.treebank_chunk.chunked_sents()
train_sents=treebank+train_sents



class ChunkParser(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]

        self.unigram_tagger = nltk.UnigramTagger(train_data)
        self.bigram_tagger = nltk.BigramTagger(train_data,backoff=self.unigram_tagger)
        self.tagger = nltk.TrigramTagger(train_data,backoff=self.bigram_tagger)

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


def get_NP_chunker():
    return ChunkParser(train_sents)
