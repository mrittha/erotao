import math
import codecs
__author__ = 'mrittha'
"""Given a set of sentences, finds the a noun in each sentence and creates a clozure based on a target word tag.
Should return a list of clozure, word, sentence dictionaries"""

import sentence_tagger
import random
import unicodedata


def first_noun(tags):
    """find the first noun, create a closure from that"""
    for i, v in enumerate(tags):
        if v[1] in ['NNP', 'NN']:
            return i, v


def any_noun(tags):
    """find the first noun, create a closure from that"""
    nouns = []
    for i, v in enumerate(tags):
        if v[1] in ['NNP', 'NN']:
            nouns.append((i, v))
    if len(nouns) > 1:
        return random.sample(nouns, 1)[0]
    elif len(nouns)==1:
        return nouns[0]
    return None,None


def create_clozure(sentence):
    tags = sentence_tagger.tag_sentence(sentence)
    location, tag = any_noun(tags)
    if not location:
        return None
    answer = {}
    answer['orginal'] = sentence
    answer['word'] = tag[0]

    words = [w[0] for w in tags]
    words[location] = ''.join(['_'] * len(tag[0]))
    answer['clozure'] = ' '.join(words)

    return answer


def create_questions(sentences):
    clozures= [create_clozure(s) for s in sentences]
    return [ c for c in clozures if c]


def find_sentences(text):
    return sentence_tagger.get_sentences(text)

def make_study_set_sentences(sentences):
    sentences = [s.strip() for s in sentences]
    sentences = [s for s in sentences if len(s) > 5]
    questions = create_questions(sentences)
    return questions

def make_study_set_text(text):
    sentences = find_sentences(text)
    return make_study_set_sentences(sentences)




    # answer=create_clozure("Saturn is the sixth planet from the Sun in the Solar System.")
    # print answer
