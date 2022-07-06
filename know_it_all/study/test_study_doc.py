import know_it_all.study.study_doc as sd
import know_it_all.study.section as sec
from pprint import pprint

def create_section_1():
    return {'last_studied': '',
                'paragraphs': [{'last_studied': '',
                 'questions': [],
                 'score': '',
                 'sentences': ['Test sentence', 'Test sentence2']},
                {'last_studied': '',
                 'questions': [],
                 'score': '',
                 'sentences': ['Test sentence3', 'Test sentence4']}],
                 'score': '',
                 'title': 'section 1'}


def create_section_2():
    return {'last_studied': '',
                'paragraphs': [{'last_studied': '',
                 'questions': [],
                 'score': '',
                 'sentences': ['Test sentence5', 'Test sentence6']},
                {'last_studied': '',
                 'questions': [],
                 'score': '',
                 'sentences': ['Test sentence7', 'Test sentence8']}],
                 'score': '',
                 'title': 'section 2'}     


def test_create():
    title="test"
    section=sd.create(title)
    assert section=={
        'title':title,
        'version':sd.VERSION,
        'toc':[],
        'sections':{},
        'last_studied':"",
        'score':""
    }

def test_bad_add_section():
    section_1=create_section_1()
    doc=sd.create("to study")
    doc=sd.add_section(doc,section_1)
   
    try:
        doc=sd.add_section(doc,section_1)
        assert False=="Shouldn't have been able to add section."
    except ValueError as ve:
        assert str(ve)=="Section title section 1 already exists. Unable to add."
    
def test_update_section():    
    section_1=create_section_1()
    doc=sd.create("to study")
    doc=sd.add_section(doc,section_1)
    section_1_delta=create_section_1()

    p1={'last_studied': '',
        'questions': [],
        'score': '',
        'sentences': ['Test sentence10']}

    section_1_delta=sec.add_paragraph(section_1_delta,p1)
    doc=sd.update_section(doc,section_1_delta)
    assert sd.get_section(doc,'section 1')==section_1_delta

def test_update_bad_section():    
    section_1=create_section_1()
    doc=sd.create("to study")
    doc=sd.add_section(doc,section_1)
    section_2=create_section_2()
    
    try:
        doc=sd.update_section(doc,section_2)
        assert False=="Shouldn't have been able to add section."
    except ValueError as ve:
        assert str(ve)=="Section title section 2 does not exist. Unable to update."

def test_to_text():
    section_1=create_section_1()
    section_2=create_section_2()
               
    doc=sd.create("to study")
    doc=sd.add_section(doc,section_1)
    doc=sd.add_section(doc,section_2)
    text=sd.to_text(doc)
    assert text=="Test sentence Test sentence2\n\nTest sentence3 Test sentence4\n\nTest sentence5 Test sentence6\n\nTest sentence7 Test sentence8"