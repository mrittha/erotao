__author__ = 'mrittha'


import nltk
from nltk.tag.perceptron import PerceptronTagger
tagger=PerceptronTagger()

"""We assume a sentence is string brought out by the sentence tokenizer"""
def tag_sentence(sentence):
    tokens=nltk.word_tokenize(sentence)
    tags=nltk.tag._pos_tag(tokens,None,tagger)

    return tags


def get_sentences(text):
    return nltk.sent_tokenize(text)


if __name__=="__main__":
    print tag_sentence("How do you do?")

