
def create(title=""):
    return {
        'sentences':[],
        'last_studied':"",
        'score':"",
        'questions':[]
    }

def get_sentences(data):
    return data.get('sentences',[])

def get_questions(data):
    return data.get('questions',[])

def add_thing(data,key,thing):
    data[key]=data.get(key,[])+[thing]
    return data

def add_sentence(data,sentence):
    """A sentence is our semantic bedrock"""
    return add_thing(data,'sentences',sentence)

def add_question(data,question):
    """A question is our understanding bedrock"""
    return add_thing(data,'questions',question)

def to_text(data):
    return ' '.join(get_sentences(data))
