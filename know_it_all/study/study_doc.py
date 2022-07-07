"""
study_doc represents the base of the erotoa system.   Erotoa generates questions bout study_doc, and measures
performance on them, study docs are created from sources.
A study doc is broken into sections, paragraphs and sentences.
"""
import json
import know_it_all.study.section as sec
from toolz import merge,get_in

VERSION="0.1"

def write(doc,path):
    with open(path,'w') as f:
        f.write(json.dumps(doc,indent=4))


def read(path):
    with open(path) as f:
        doc=json.reads(f.read())
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
    section_title=sec.get_title(section)
    if section_title in section_names(doc):
        raise ValueError(f'Section title {section_title} already exists. Unable to add.')
    else:
        doc['toc']=section_names(doc)+[section_title]
        doc['sections']=merge(doc.get('sections',{}),{section_title:section})
    return doc

def update_section(doc,section):
    section_title=sec.get_title(section)
    if section_title not in section_names(doc):
        raise ValueError(f'Section title {section_title} does not exist. Unable to update.')
    else:
        doc['sections']=merge(doc.get('sections',{}),{section_title:section})
    return doc

def get_section(doc,section_title):
    return get_in(['sections',section_title],doc,{})

def to_text(doc):
    text=[]
    for section_title in section_names(doc):
        text.append(sec.to_text(get_section(doc,section_title)))
    return "\n\n".join(text)

