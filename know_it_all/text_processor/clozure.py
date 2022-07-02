__author__ = 'mrittha'
"""Given a set of sentences, finds the a noun in each sentence and creates a clozure based on a target word tag.
Should return a list of clozure, word, sentence dictionaries"""

import know_it_all.text_processor.sentence_tagger as sentence_tagger
import random
import edn_format
from edn_format import Keyword


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
    answer = {}
    answer['original'] = sentence
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

spider_text="""Spiders (order Araneae) are air-breathing arthropods that
have eight legs and chelicerae with fangs that inject venom. They are the largest
order of arachnids and rank seventh in total species diversity among all other
orders of organisms.[2] Spiders are found worldwide on every continent except for Antarctica,
and have become established in nearly every habitat with the exceptions of air and sea colonization.
As of November 2015, at least 45,700 spider species,[3] and 114 families have been recorded by
taxonomists.[1] However, there has been dissension within the scientific community as to how
all these families should be classified, as evidenced by the over 20 different classifications that have been proposed since 1900.[4]"""

def turn_text_to_edn_notes(text,title,author,urls,section_title):
    study_set=make_study_set_text(text)
    doc={}
    doc[Keyword("author")]=author
    doc[Keyword("title")]=title
    doc[Keyword("urls")]=urls
    section={}
    doc[Keyword("sections")]=[section]
    section[Keyword("title")]=section_title
    questions=[]
    for a_clozure in study_set:
        question_pair={}
        question_pair[Keyword("q")]=a_clozure['clozure']
        question_pair[Keyword("a")]=a_clozure['word']
        questions.append(question_pair)
    section[Keyword("questions")]=questions
    return doc




data=turn_text_to_edn_notes(spider_text,"Spider","Wikipedia",["https://en.wikipedia.org/wiki/Spider"],"introduction")
with open(r"c:\code\sophist\spider_notes.edn",'w') as f:
    f.write(edn_format.dumps(data)+"\n")




