__author__ = 'mrittha'
"""Given a list of sentences, finds the  noun in each sentence and creates a clozure based on a target word tag.
Should return a list of clozure, word, sentence dictionaries"""

import know_it_all.text_processor.sentence_tagger as sentence_tagger
#from know_it_all.study import paragraph as par,section as sec,study_doc as doc
import random
#import edn_format
#from edn_format import Keyword


def first_noun(tags):
    """find the first noun, create a closure from that"""
    for i, v in enumerate(tags):
        if v[1] in ['NNP', 'NN']:
            return i, v


def any_noun(tags):
    """choose a random, create a closure from that"""
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
    
    words = [w[0] for w in tags]
    words[location] = ''.join(['_'] * len(tag[0]))

    answer = {'answer':tag[0],
              'original':sentence,
              'question':' '.join(words),
              'score':1.0,
              'type':'simple_clozure'}

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



