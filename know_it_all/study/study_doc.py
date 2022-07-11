"""
study_doc represents the base of the erotoa system.   Erotoa generates questions bout study_doc, and measures
performance on them, study docs are created from sources.
A study doc is broken into sections, paragraphs and sentences.
"""
import json
import know_it_all.study.section as sec
from toolz import merge,get_in
from pprint import pprint

VERSION="0.1"

def write(doc,path):
    with open(path,'w') as f:
        f.write(json.dumps(doc,indent=4))


def read(path):
    with open(path) as f:
        doc=json.loads(f.read())
    return doc

def create(title=""):
    return {
        'title':title,
        'version':VERSION,
        'toc':[],
        'sections':{},
        'last_studied':"",
        'score':""
    }

def section_names(doc):
    return doc.get('toc',[])

def add_section(doc,section):
    section_name=sec.get_title(section)
    if section_name in section_names(doc):
        raise ValueError(f'Section title {section_name} already exists. Unable to add.')
    else:
        doc['toc']=section_names(doc)+[section_name]
        doc['sections']=merge(doc.get('sections',{}),{section_name:section})
    return doc

def update_section(doc,section):
    section_name=sec.get_title(section)
    if section_name not in section_names(doc):
        raise ValueError(f'Section title {section_name} does not exist. Unable to update.')
    else:
        #pprint({section_name:section})
        doc['sections']=merge(doc.get('sections',{}),{section_name:section})
    return doc

def get_section(doc,section_name):
    return get_in(['sections',section_name],doc,{})

def to_text(doc):
    text=[]
    for section_name in section_names(doc):
        text.append(sec.to_text(get_section(doc,section_name)))
    return "\n\n".join(text)

