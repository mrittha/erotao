__author__ = 'mritthaler'

from gensim import models
import numpy as np
import nltk
from pattern.en import parse,tag,tokenize,pprint


def find_relation_tags(a_parse):
    tags=set([ p.split('/')[-1] for p in a_parse.split(' ')])
    return tags


def gather_bits(a_parse):
    #tags= find_relation_tags(a_parse)
    gathered={}
    all_bits=a_parse.split(' ')
    for p in all_bits:
        t=p.split('/')[-1]
        gathered[t]=gathered.get(t,[])+[p]
    return gathered




def gather_bits_by_role(all_bits):
    gathered={}
    for p in all_bits:
        t=p.split('/')[-1]
        t=t.split('-')
        if len(t)>1:
            gathered[t[-2]]=gathered.get(t[-2],[])+[p]
    return gathered

def gather_bits_by_id(all_bits):
    #tags= find_relation_tags(a_parse)
    gathered={}
    for p in all_bits:
        t=p.split('/')[-1].split('-')[-1]
        gathered[t]=gathered.get(t,[])+[p]
    return gathered

def gather_question_bits(sentence):
    question_bits=[]
    a_parse=parse(sentence,relations=True)
    print a_parse
    pprint(a_parse)
    all_bits=a_parse.split(' ')
    ids=gather_bits_by_id(all_bits)
    for id in ids:
        roles=gather_bits_by_role(ids[id])
        if 'SBJ' in roles and 'VP' in roles and 'OBJ' in roles:
            question_bits.append(roles)
    return question_bits

def is_pronoun(bit_list):
    if len(bit_list)==1 and bit_list[0].split('/')[1]=="PRP":
        return True
    return False



def convert_pp(basic_sentences):
    current_subject=None
    for sentence in basic_sentences:
        if not is_pronoun(sentence['SBJ']):
            current_subject=sentence['SBJ']
        else:
            if current_subject:
                sentence['SBJ']=current_subject
    return basic_sentences

def bit_to_word(bit):
    return bit.split('/')[0]

def bits_to_words(bits):
    return [bit_to_word(bit) for bit in bits]

def basic_sentence_to_question(basic_sentence):
    sbj=basic_sentence['SBJ']
    obj=basic_sentence['OBJ']
    verb=basic_sentence['VP']





text="""
A star is a massive ball of plasma (very hot gas) held together by gravity. It radiates energy because of the nuclear reactions inside it

It radiates heat and light, and every other part of the electromagnetic spectrum, such as radio waves, micro-waves, X-rays, gamma-rays and ultra-violet radiation. The proportions vary according to the mass and age of the star.

The energy of stars comes from nuclear fusion. This is a process that turns a light chemical element into another heavier element. Stars are mostly made of hydrogen and helium. They turn the hydrogen into helium by fusion. When a star is near the end of its life, it begins to change the helium into other heavier chemical elements, like carbon and oxygen. Fusion produces a lot of energy. The energy makes the star very hot. The energy produced by stars radiates away from them. The energy leaves as electromagnetic radiation.
"""
sentences=tokenize(text)
basic_sentences=[]
for sentence in sentences:
    print sentence
    basic_sentences=basic_sentences+gather_question_bits(sentence)

#basic_sentences=convert_pp(basic_sentences)
for sentence in basic_sentences:
    print sentence

