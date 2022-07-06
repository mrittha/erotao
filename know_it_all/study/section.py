import know_it_all.study.paragraph as para

def create(title=""):
    return {
        'title':title,
        'paragraphs':[],
        'last_studied':"",
        'score':"",
    }

def get_title(data):
    return data.get('title',"")

def get_paragraphs(data):
    return data.get('paragraphs',[])

def add_paragraph(data,paragraph):
    data['paragraphs']=get_paragraphs(data)+[paragraph]
    return data

def to_text(data):
    text=[]
    for paragraph in get_paragraphs(data):
        text.append(para.to_text(paragraph))
    return '\n\n'.join(text)

