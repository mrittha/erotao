
def create(title):
    return {
        'title':title,
        'sentences':[],
        'last_studied':"",
        'score':"",
        'questions':[]
    }

def get_sentences(paragraph):
    return paragraph.get('sentences',[])

def get_questions(paragraph):
    return paragraph.get('questions',[])

def add_thing(paragraph,key,thing):
    paragraph[key]=paragraph.get(key,[])+[thing]
    return paragraph

def add_sentence(paragraph,sentence):
    """A sentence is our semantic bedrock"""
    return add_thing(paragraph,'sentences',sentence)

def add_question(paragraph,question):
    """A question is our understanding bedrock"""
    return add_thing(paragraph,'questions',question)

def to_text(paragraph):
    return ' '.join(get_sentences(paragraph))
