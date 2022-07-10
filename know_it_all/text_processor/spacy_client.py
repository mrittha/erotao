from toolz import frequencies, concat
import spacy
import numpy as np
import networkx as nx
from pprint import pprint
import yaml
import os
import random
#import pydot
#from networkx.drawing.nx_pydot import write_dot

nlp = spacy.load('en_core_web_lg')

EXTRA_STOP=["et","al"]

def get_noun_phrases(text,section_id):
    """
    Process the text look for noun phrases (noun chunks in spacy terms)
    filters out spaces, stops and numbers etc.  returns a list of phrases
    
    """
    doc = nlp(text)
    phrases = []
    for chunk in doc.noun_chunks:
        current_phrase = []
        for tok in chunk:
            if not tok.is_punct and not tok.is_space and not tok.is_stop and not tok.is_oov and len(
                    tok) > 1 and not tok.like_num and tok.text not in EXTRA_STOP:
                current_phrase.append(tok)
            elif tok.is_punct or tok.is_stop or tok.is_oov or len(tok.text) <= 1 or tok.like_num or tok.text in EXTRA_STOP:
                if current_phrase != []:
                    span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
                    if span.text != '':
                        phrases.append([tok.lower_ for tok in span])
                    current_phrase = []
            else:
                pass
        
        #process the final phrase since we are no longer in the for loop
        if current_phrase != []:
            span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
            if span.text != '':
                phrases.append([tok.lower_ for tok in span])
    
    

    print(phrases)


def rake(text, section_id):
    """
    The rake algorithm builds a graph of words, 
    
    
    """
    doc = nlp(text)
    phrases = []
    g=nx.Graph()
    for chunk in doc.noun_chunks:
        current_phrase = []
        for tok in chunk:
            if not tok.is_punct and not tok.is_space and not tok.is_stop and not tok.is_oov and len(
                    tok) > 1 and not tok.like_num and tok.text not in EXTRA_STOP:
                current_phrase.append(tok)
            elif tok.is_punct or tok.is_stop or tok.is_oov or len(tok.text) <= 1 or tok.like_num or tok.text in EXTRA_STOP:
                if current_phrase != []:
                    span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
                    if span.text != '':
                        phrases.append(span)
                    current_phrase = []
            else:
                pass
        
        #process the final phrase since we are no longer in the for loop
        if current_phrase != []:
            span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
            if span.text != '':
                phrases.append(span)
            current_phrase = []


    #we just want to the total frequency across all of our tokens
    counts = frequencies([p.lemma_.lower() for p in concat(phrases)])
    
    #add the unique tokens to the graph
    for k,v in counts.items():
        g.add_node(k,size=v)
    
    degree = {}
    for phrase in phrases:
        d = len(phrase)
        for tok in phrase:
            degree[tok.lemma_.lower()] = degree.get(tok.lemma_.lower(), 0) + d
        for i in range(len(phrase)):
            for j in range(i,len(phrase)):
                if j!=i:
                    t1=phrase[i].lemma_.lower()
                    t2=phrase[j].lemma_.lower()
                    g.add_edge(t1, t2, weight=1)
    phrase_scores = []
    seen_phrase = set()
    text_object = {"text": text,
                   "section": section_id,
                   "word count": len(doc),
                   "doc":doc
                   }
    
    
    nx.write_graphml(g,"rake.graphml")
    #write_dot(g,"rake.dot")
    tagged_phrases = []
    for phrase in phrases:

        score = sum([word_score(tok.lemma_.lower(), degree, counts) for tok in phrase])
        p_string = phrase_string(phrase)
        t_phrase = {"start": phrase.start,
                    "end": phrase.end,
                    # "vector":phrase.vector.tolist(),
                    "score": score,
                    "text": phrase.text,
                    "p_string": p_string
                    }
        if p_string not in seen_phrase:
            tagged_phrases.append(t_phrase)
            phrase_scores.append((score, phrase,phrase.start,phrase.end))
            seen_phrase.add(p_string)
    text_object["tagged phrases"] = tagged_phrases
    text_object["phrase scores"] = phrase_scores

    # I a doc, the list of spans, and their scores
    phrase_scores.sort(reverse=True)
    p_vects = []

    for score, phrase,start,end in phrase_scores[:10]:
        p_vects += [score * phrase_vector(phrase)]
    p_vects = normalize(np.sum(np.array(p_vects), axis=0))
    text_object['phrase vector'] = p_vects

    return text_object

def find_sentences(text):
    doc = nlp(text)
    sentences=[]
    for s in doc.sents:
        txt=str(s)
        txt=txt.replace("\n"," ")
        txt=txt.replace("\r"," ")
        txt=txt.strip()
        sentences.append(txt)
    return sentences
    
    #pprint(doc.sents)



if __name__=='__main__':
    text="""
    Deep learning algorithms involve optimization in many contexts. 
    For example,performing inference in models such as PCA involves solving an optimization problem.
    We often use analytical optimization to write proofs or design algorithms.
    Of all the many optimization problems involved in deep learning, 
    the most diﬃcultis neural network training. 
    It is quite common to invest days to months of time on hundreds 
    of machines to solve even a single instance of the neural network training problem. 
    Because this problem is so important and so expensive, 
    a specialized set of optimization techniques have been developed for solving it. 
    This chapter presents these optimization techniques for neural network training.
    
    """

    get_noun_phrases(text,"test")