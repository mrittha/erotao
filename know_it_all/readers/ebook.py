import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

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
            output += '{} '.format(t)
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


def to_text(path):
    return epub2text(path)


if __name__=="__main__":
    out=epub2text(r"C:\Shared area\Calibre Library\Calibre Library\Rui Xu, Don Wunsch\9780470276808-Chapter-1-Cluster-Anal (3)\9780470276808-Chapter-1-Cluster - Rui Xu, Don Wunsch.epub")
    text="\n".join(out)
    with open("C:\code\memory_palace\data\9780470276808-Chapter-1-Cluster-analysis_epub.txt",'w',encoding="utf-8") as f:
        f.write(text)

