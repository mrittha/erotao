from cmath import e
import sys
sys.path.append('c:\\code\\erotao')

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import json
from pprint import pprint


from know_it_all.study import study_doc as sd,section as sec,paragraph as par,questions as q
import know_it_all.text_processor.chunk_o_learning as col



# from https://github.com/ZA3karia/PDF2TEXT/blob/master/ebook_to_text.ipynb

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]
def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += f'{t} '
    return output

def thtml2ttext(thtml):
    output = []
    for html in thtml:
        text =  chap2text(html)
        output.append(text)
    return output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext    



def to_paragraphs(text):
    return text.split('  ')


def build_section(epub_section, enumeration):
    title=f"Section_{enumeration}"
    section=sec.create(title=title)
    lists_of_sentences=col.get_paragraphs(epub_section)
    for i,p in enumerate(lists_of_sentences):
        paragraph=par.create(f"Paragraph_{i}")
        for sentence in p:
            paragraph=par.add_sentence(paragraph,sentence)
        section=sec.add_paragraph(section,paragraph)
    return section

def to_study_doc(path):
    base_filename=os.path.basename(path)
    epub_sections=epub2text(path)
    epub_sections=[ to_paragraphs(text) for text in epub_sections] 
    document=sd.create(title=base_filename)
    for i,epub_section in enumerate(epub_sections):
        section=build_section(epub_section,i)
        document=sd.add_section(document,section)
    return document



def to_text(path):
    out=epub2text(path)
    text="\n".join(out)
    return text

def create_study_doc_path(path):
    study_doc_dir="C:\\code\\erotao\\study_docs\\"
    base_filename=os.path.basename(path)
    filename=base_filename+".json"
    sd_path=f"{study_doc_dir}{filename}"
    return sd_path


def create_full_doc(path,sd_path):
    document=to_study_doc(path)
    document=q.add_simple_clozures(document)
    document=q.add_raked_clozures(document)
    sd.write(document,sd_path)
    return document





if __name__=="__main__":
    #to_sections(r"C:\attic\docs\A Quick Guide to Cloud Types (2022.07.05-21.56.17Z).epub")
    path=r"C:\attic\docs\A Quick Guide to Cloud Types (2022.07.05-21.56.17Z).epub"
    to_study_doc(path)
    #pprint(to_paragraphs(text))
    #with open("C:\code\memory_palace\data\9780470276808-Chapter-1-Cluster-analysis_epub.txt",'w',encoding="utf-8") as f:
    #    f.write(text)

