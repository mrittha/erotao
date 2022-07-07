import know_it_all.study.paragraph as para
from toolz import merge

def create(title):
    return {
        'title':title,
        'paragraphs_titles':[],
        'paragraphs':{},
        'last_studied':"",
        'score':"",
    }

def get_title(section):
    return section.get('title',"")

def get_paragraphs(section):
    return section.get('paragraphs',{})

def get_paragraph_titles(section):
    return section.get('paragraph_titles',[])

def add_paragraph(section,paragraph):
    p_title=paragraph['title']
    if paragraph['title'] in get_paragraph_titles(section):
        raise ValueError(f"Already have a paragraph with designation {p_title} in section")
    section['paragraph_titles']=get_paragraph_titles(section)+[p_title]
    section['paragraphs']=merge(get_paragraphs(section),{'p_title':paragraph})
    return section

def update_paragraph(section,paragraph):
    p_title=paragraph['title']
    if paragraph['title'] not in get_paragraph_titles(section):
        raise ValueError(f"No paragraph with designation {p_title} in section")
    section['paragraphs']=merge(get_paragraphs(section),{'p_title':paragraph})
    return section


def to_text(section):
    text=[]
    for paragraph in get_paragraphs(section):
        text.append(para.to_text(paragraph))
    return '\n\n'.join(text)

