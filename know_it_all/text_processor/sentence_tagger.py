__author__ = 'mrittha'


import nltk
from nltk.tag.perceptron import PerceptronTagger

toker=nltk.PunktSentenceTokenizer()
tagger=PerceptronTagger()

"""We assume a sentence is string brought out by the sentence tokenizer"""
def tag_sentence(sentence):
    tokens=nltk.word_tokenize(sentence,language='english')
    tags=nltk.tag._pos_tag(tokens,None,tagger,lang='eng')

    return tags


def get_sentences(text):
    return toker.tokenize(text)


if __name__=="__main__":
    print(tag_sentence("The dog is red."))
    print(tag_sentence("What is red?"))


