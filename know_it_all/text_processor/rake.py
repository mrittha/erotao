from toolz import frequencies, concat
import spacy
import numpy as np
import networkx as nx
from pprint import pprint
import yaml
import os
import random
#import pydot
#from networkx.drawing.nx_pydot import write_dot

nlp = spacy.load('en_core_web_lg')

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def phrase_vector(phrase):
    output = phrase[0].vector
    for tok in phrase[1:]:
        output += tok.vector
    return normalize(output)


def word_score(token, degree, counts):
    return degree.get(token, 0) / counts.get(token, 1)


def phrase_string(phrase):
    return " ".join([tok.lemma_.lower() for tok in phrase])




EXTRA_STOP=["et","al"]



def rake(text, section_id):
    """
    The rake algorithm builds a graph of words, 
    
    
    """
    doc = nlp(text)
    phrases = []
    g=nx.Graph()
    for chunk in doc.noun_chunks:
        current_phrase = []
        for tok in chunk:
            if not tok.is_punct and not tok.is_space and not tok.is_stop and not tok.is_oov and len(
                    tok) > 1 and not tok.like_num and tok.text not in EXTRA_STOP:
                current_phrase.append(tok)
            elif tok.is_punct or tok.is_stop or tok.is_oov or len(tok.text) <= 1 or tok.like_num or tok.text in EXTRA_STOP:
                if current_phrase != []:
                    span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
                    if span.text != '':
                        phrases.append(span)
                    current_phrase = []
            else:
                pass
        
        #process the final phrase since we are no longer in the for loop
        if current_phrase != []:
            span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
            if span.text != '':
                phrases.append(span)
            current_phrase = []


    #we just want to the total frequency across all of our tokens
    counts = frequencies([p.lemma_.lower() for p in concat(phrases)])
    
    #add the unique tokens to the graph
    for k,v in counts.items():
        g.add_node(k,size=v)
    
    degree = {}
    for phrase in phrases:
        d = len(phrase)
        for tok in phrase:
            degree[tok.lemma_.lower()] = degree.get(tok.lemma_.lower(), 0) + d
        for i in range(len(phrase)):
            for j in range(i,len(phrase)):
                if j!=i:
                    t1=phrase[i].lemma_.lower()
                    t2=phrase[j].lemma_.lower()
                    g.add_edge(t1, t2, weight=1)
    phrase_scores = []
    seen_phrase = set()
    text_object = {"text": text,
                   "section": section_id,
                   "word count": len(doc),
                   "doc":doc
                   }
    
    
    nx.write_graphml(g,"rake.graphml")
    #write_dot(g,"rake.dot")
    tagged_phrases = []
    for phrase in phrases:

        score = sum([word_score(tok.lemma_.lower(), degree, counts) for tok in phrase])
        p_string = phrase_string(phrase)
        t_phrase = {"start": phrase.start,
                    "end": phrase.end,
                    # "vector":phrase.vector.tolist(),
                    "score": score,
                    "text": phrase.text,
                    "p_string": p_string
                    }
        if p_string not in seen_phrase:
            tagged_phrases.append(t_phrase)
            phrase_scores.append((score, phrase,phrase.start,phrase.end))
            seen_phrase.add(p_string)
    text_object["tagged phrases"] = tagged_phrases
    text_object["phrase scores"] = phrase_scores

    # I a doc, the list of spans, and their scores
    phrase_scores.sort(reverse=True)
    p_vects = []

    for score, phrase,start,end in phrase_scores[:10]:
        p_vects += [score * phrase_vector(phrase)]
    p_vects = normalize(np.sum(np.array(p_vects), axis=0))
    text_object['phrase vector'] = p_vects

    return text_object

def find_sentences(text):
    doc = nlp(text)
    sentences=[]
    for s in doc.sents:
        txt=str(s)
        txt=txt.replace("\n"," ")
        txt=txt.replace("\r"," ")
        txt=txt.strip()
        sentences.append(txt)
    return sentences
    
    #pprint(doc.sents)


def complex_clozures(text):
    results = rake(text, 1)
    
    #find the sentences
    sentences=[]
    for s in results['doc'].sents:
        s=str(s).replace("\n"," ").strip()
        sentences.append(s)

    questions=[]

    top_one_hundred=list(results["phrase scores"][:100])
    
    top_one_hundred.sort(key=lambda x: x[2])
    
    for result in top_one_hundred:
        score,phrase,start,end=result
        phrase=str(phrase)  

        for i,s in enumerate(sentences):
            if phrase.lower() in s.lower():

                question=s.replace(phrase,"_"*len(phrase))
                answer=phrase
                #print(f"S:  {s}")
                #print(f"Q:  {question}")
                #print(f"A:  {answer}")
                t={"sentence":s,
                   "question":question,
                   "answer":answer,
                   "score":score,
                   "sentence_number":i
                   }
                questions.append(t)

    return questions        




def rake_test(file_path):
    with open(file_path,encoding="utf-8") as f:
        text=f.read()

    questions=complex_clozures(text)

    directory,file_name=os.path.split(file_path)
    with open(f"data/{file_name}.yaml","w")  as f:
        f.write(yaml.dump(questions))        
    
 

if __name__ == "__main__":
    file=r"C:\code\memory_palace\data\Even beyond Physics_ Introducing Multicomputation as a Fourth General Paradigm for Theoretical Science—Stephen Wolfram Writings.txt"
    questions=rake_test(r"C:\code\memory_palace\data\Even beyond Physics_ Introducing Multicomputation as a Fourth General Paradigm for Theoretical Science—Stephen Wolfram Writings.txt")
    text=[]
    with open(file+".yaml") as f:
        questions=yaml.load(f.read(),Loader=yaml.SafeLoader)
    #print(questions)
    text.append("STUDY GUIDE")
    text.append(os.path.split(file)[1])
    text.append("---------------------------")
    for i,q in enumerate(questions):
        question=q["question"]
        score=q["score"]
        text.append(f"({i}) {question} ({score})")
        answers=[q['answer']]
        while len(answers)<5:
            random_answer=random.choice(questions)['answer']
            if random_answer not in answers:
                answers.append(random_answer)

        random.shuffle(answers)
        for j,a in enumerate(['A','B','C','D']):
            text.append(f"   ({a})  {answers[j]}")
        text.append("   ")
    with open("data/study.txt",'w',encoding='utf-8') as f:
        f.write("\n".join(text))

        
        
