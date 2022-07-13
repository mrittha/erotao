#import sys
#sys.path.append(r'C:\code\erotao')

import know_it_all.text_processor.clozure as clo
import know_it_all.text_processor.rake as rake
import know_it_all.text_processor.spacy_client as sc
from know_it_all.study import study_doc as sd,section as sec,paragraph as par
import know_it_all.clients.openai as oai
import yaml
from pprint import pprint
import re
import random
import os


def open_ai_dummy(prompt):
    return "Q:Am I the question?"

def generate_open_ai_questions(example_data,paragraph):
    
    questions=par.get_questions(paragraph)
    questions=[ q for q in questions if q['type']=='complex_clozure']
    prompt=['I am an intelligent program to help you understand text.  If you give me context and an answer from the text, I will create a question for that answer.']
    sentences=par.get_sentences(paragraph)
    new_questions=[]
    if len(questions)>0 and len(sentences)>=2:
        for question in questions:
        #question=random.choice(questions)
            examples=random.sample(example_data,10)
            for example in examples:
                if len('\n'.join(prompt))>2500:
                    break
                prompt.append('')
                prompt.append(f"C:{example['context']}")
                prompt.append(f"A:{example['answer']}")
                prompt.append(f"Q:{example['question']}")
                
            
            sentence_string=' '.join(sentences)
            prompt.append('          ')            
            prompt.append(f"C:{sentence_string}")
            prompt.append(f"A:{question['answer']}")
            string_prompt='\n'.join(prompt)
            #print(string_prompt)
            #print("Contacting Open AI")
            #print(f"C:{sentence_string}")
            response=oai.generate_question(string_prompt)
            #response=open_ai_dummy(string_prompt)
            #pull the possible question from the response
            matches=re.findall("Q\:[\S ]+?\?",response,re.MULTILINE)
            if len(matches)>0:
                oai_question={'question':matches[0][2:],
                'answer':question['answer'],
                'original':question['original'],
                'score':question['score'],
                'type':'open_ai_question'
                }
                new_questions.append(oai_question)
    return new_questions
            

def add_open_ai_questions(document):
    """
    Be aware that this causes cost!
    The document also needs to have had the complex clozure questions added
    
    """
    example_data_file=os.getenv("QUESTION_ANSWER_DATA")
    with open(example_data_file) as f:
        example_data=yaml.safe_load(f.read())




    sections=sd.section_names(document)
    for s in sections:
        section=sd.get_section(document,s)
        for paragraph in sec.get_paragraphs(section).values():
            questions=generate_open_ai_questions(example_data,paragraph)
            for question in questions:
                paragraph=par.add_question(paragraph,question)
            section=sec.update_paragraph(section,paragraph)
        document=sd.update_section(document,section)            
    return document



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
    Given we have a certain clozure, we'll want to find the 
   
    """
    section_names=sd.section_names(document)
    for name in section_names:
        section=sd.get_section(document,name)
        sentence=find_sentence_sec(section,search_string)
        if sentence:
            return sentence
    return None

def make_clozure_question_answer(sentence:str,c_string:str,score:float):
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
             'score':score,
             'type':'complex_clozure'
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
            question=make_clozure_question_answer(sentence,text,score)
            section=sd.get_section(document,section_name)
            paragraph=sec.get_paragraph(section,paragraph_name)
            paragraph=par.add_question(paragraph,question)
            section=sec.update_paragraph(section,paragraph)
            document=sd.update_section(document,section)
    return document
            
            
    
if __name__=="__main__":
    
    
    study_doc=sd.read('C:\code\erotao\study_docs\A Quick Guide to Cloud Types (2022.07.05-21.56.17Z).epub.json')
    study_doc=add_open_ai_questions(study_doc)
    pprint(study_doc)




            
