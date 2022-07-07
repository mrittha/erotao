import know_it_all.study.paragraph as para
import know_it_all.study.section as sec

def test_create():
    title="test"
    section=sec.create(title)
    assert section=={
        'title':title,
        'paragraphs':[],
        'last_studied':"",
        'score':"",
    }

def test_to_text():
    p1=para.create()
    p1=para.add_sentence(p1,"Test sentence")
    p1=para.add_sentence(p1,"Test sentence2")

    p2=para.create()
    p2=para.add_sentence(p2,"Test sentence3")
    p2=para.add_sentence(p2,"Test sentence4")

    s=sec.create("section 1")
    s=sec.add_paragraph(s,p1)
    print(s)
    s=sec.add_paragraph(s,p2)

    t=sec.to_text(s)
    assert t=="Test sentence Test sentence2\n\nTest sentence3 Test sentence4"