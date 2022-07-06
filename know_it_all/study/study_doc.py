"""
study_doc represents the base of the erotoa system.   Erotoa generates questions bout study_doc, and measures
performance on them, study docs are created from sources.
A study doc is broken into sections, paragraphs and sentences.
"""
import json
import know_it_all.study.section as sec
from toolz import merge,get_in

VERSION="0.1"

def write(data,path):
    with open(path,'w') as f:
        f.write(json.dumps(data,indent=4))


def read(path):
    with open(path) as f:
        data=json.reads(f.read())
    return data

def create(title=""):
    return {
        'title':title,
        'version':VERSION,
        'toc':[],
        'sections':{},
        'last_studied':"",
        'score':""
    }

def section_names(data):
    return data.get('toc',[])

def add_section(data,section):
    section_title=sec.get_title(section)
    if section_title in section_names(data):
        raise ValueError(f'Section title {section_title} already exists. Unable to add.')
    else:
        data['toc']=section_names(data)+[section_title]
        data['sections']=merge(data.get('sections',{}),{section_title:section})
    return data

def update_section(data,section):
    section_title=sec.get_title(section)
    if section_title not in section_names(data):
        raise ValueError(f'Section title {section_title} does not exist. Unable to update.')
    else:
        data['sections']=merge(data.get('sections',{}),{section_title:section})
    return data

def get_section(data,section_title):
    return get_in(['sections',section_title],data,{})

def to_text(data):
    text=[]
    for section_title in section_names(data):
        text.append(sec.to_text(get_section(data,section_title)))
    return "\n\n".join(text)

