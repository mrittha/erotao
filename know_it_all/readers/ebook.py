import sys
sys.path.append('c:\\code\\erotao')

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import json
from pprint import pprint


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
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext    

def build_chapter(chapter, enumeration):
    title=f"Section_{enumeration}"
    paragraphs=col.get_paragraphs([chapter])
    chapter_section={ "full_title":title,
              "title":title,
              "paragraphs":paragraphs}
    
    return title,chapter_section


def to_paragraphs(text):
    return text.split('  ')

def to_sections(path):
    chapters=epub2text(path)
    document={'section_list':[],
              'sections':{}
    }
    for i,chapter in enumerate(chapters):
        title,section_chapter=build_chapter(chapter,i)
        document['section_list'].append(title)
        document['sections'][title]=section_chapter
    filename=os.path.basename(path)+".json"
    filepath=f"C:\\code\\erotao\\know_it_all\\subjects\\{filename}"
    if not os.path.exists(filepath):
        with open(filepath,'w') as f:
            f.write(json.dumps(document,indent=4))
    return filepath




def to_text(path):
    out=epub2text(path)
    text="\n".join(out)
    return text





if __name__=="__main__":
    #to_sections(r"C:\attic\docs\A Quick Guide to Cloud Types (2022.07.05-21.56.17Z).epub")
    path=r"C:\attic\docs\A Quick Guide to Cloud Types (2022.07.05-21.56.17Z).epub"
    text=to_text(path)
    pprint(to_paragraphs(text))
    #with open("C:\code\memory_palace\data\9780470276808-Chapter-1-Cluster-analysis_epub.txt",'w',encoding="utf-8") as f:
    #    f.write(text)

