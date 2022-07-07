import know_it_all.text_processor.clozure as clo
from know_it_all.study import study_doc as sd,section as sec,paragraph as par
from pprint import pprint

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



            
