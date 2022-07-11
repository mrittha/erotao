import know_it_all.text_processor.clozure as clo
import know_it_all.text_processor.rake as rake
import know_it_all.text_processor.spacy_client as sc
from know_it_all.study import study_doc as sd,section as sec,paragraph as par
from pprint import pprint
import re

def add_simple_clozures(document):
    sections=sd.section_names(document)
    for s in sections:
        section=sd.get_section(document,s)
        for paragraph in sec.get_paragraphs(section).values():
            sentences=par.get_sentences(paragraph)
            questions=clo.make_study_set_sentences(sentences)
            for question in questions:
                paragraph=par.add_question(paragraph,question)
            section=sec.update_paragraph(section,paragraph)
        document=sd.update_section(document,section)            
    return document


def find_sentence_par(search_string:str,paragraph):
    print(paragraph)
    print(search_string)
    sentences=par.get_sentences(paragraph)
    for s in sentences:
        if search_string.lower() in s.lower():
            return [paragraph['title'],s]
    return None

def find_sentence_sec(section,search_string):
    paragraphs=sec.get_paragraphs(section).values()
    for p in paragraphs:
        result=find_sentence_par(search_string,p)
        if result:
            return [section['title']]+result
    return None
    

def find_sentence_doc(document,search_string):
    """
    Given we have a certain clojure, we'll want to find the 
   
    """
    section_names=sd.section_names(document)
    for name in section_names:
        section=sd.get_section(document,name)
        sentence=find_sentence_sec(section,search_string)
        if sentence:
            return sentence
    return None

def make_clojure_question_answer(sentence:str,c_string:str,score:float):
    #we could make this a case insensitive replace
    blanks='_'*len(c_string)
    
    # The following allows for case insensitive substitution
    # It may run into problems if there are things which need to be
    # escaped for the regular expression
    clozure=re.sub(c_string,blanks,sentence,flags=re.I)
    #clozure=sentence.replace(c_string,blanks)
    
    return { 'question':clozure,
             'answer':c_string,
             'original':sentence,
             'score':score
            }
    


def add_raked_clozures(document):
    text=sd.to_text(document)
    noun_phrases=sc.get_noun_phrases(text)
    scored_phrases=rake.rake_phrases(noun_phrases)
    scored_phrases.sort(reverse=True)
    
    #sort them so we start with the most 'important' phrases
    
    #only pick the top 10
    for phrase in scored_phrases[:10]:
        score,span=phrase[:2]
        text=str(span)
        section_name,paragraph_name,sentence=find_sentence_doc(document,text)
        if sentence:
            question=make_clojure_question_answer(sentence,text,score)
            section=sd.get_section(document,section_name)
            paragraph=sec.get_paragraph(section,paragraph_name)
            paragraph=par.add_question(paragraph,question)
            section=sec.update_paragraph(section,paragraph)
            document=sd.update_section(document,section)
    return document
            
            
    




            
