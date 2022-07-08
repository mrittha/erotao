import know_it_all.study.paragraph as para


def test_create():
    paragraph=para.create('p1')
    assert paragraph=={
        'title':'p1',
        'sentences':[],
        'last_studied':"",
        'score':"",
        'questions':[]
    }

def test_add_sentence():
    base=para.create('p1')
    base=para.add_sentence(base,"Test sentence")
    s=para.get_sentences(base)
    assert s==["Test sentence"]

def test_add_question():
    base=para.create('p1')
    question={
        "question":"What is the airspeed of a laden swallow?",
        "answer":"A european or a asian swallow?"
    }
    base=para.add_question(base,question)
    q=para.get_questions(base)
    assert q==[{
        "question":"What is the airspeed of a laden swallow?",
        "answer":"A european or a asian swallow?"
    }]

def test_to_text():
    base=para.create('p1')
    base=para.add_sentence(base,"Test sentence")
    base=para.add_sentence(base,"Test sentence2")
    t=para.to_text(base)
    assert t=="Test sentence Test sentence2"