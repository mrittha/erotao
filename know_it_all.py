__author__ = 'mrittha'
"""
the know-it-all is a method for studying subjects.    It allows the student to study subjects based on
wikipedia or text files.  It reads the information to the learner, then asks questions about the information
just read.   It keeps track of the answers, so determine how well the student knows each subject.
It allows for reviews, and also text clustering to fit new subjects into its knowledge base.
In general the idea is that the student keeps using the software, and it keeps getting smarter about what the
student knows.

track and break out questions.


"""
import math
import random
import codecs
import json
import wikipedia
import os
import know_it_all.text_processor.clozure as clozure
import know_it_all.cli.talker as talker
import know_it_all.text_processor.chunk_o_learning as col
import know_it_all.cli.simple_menu as simple_menu
import know_it_all.evaluation.multi_choice as mc
import know_it_all.readers.ebook as ebook
import know_it_all.readers.pdf as rpdf
import know_it_all.text_processor.rake as rake
from know_it_all.study import study_doc as sd,section as sec,paragraph as par,questions as q
from pprint import pprint


def study_questions(questions, rate):
    if len(questions) < 1:
        return 0, 0
    points = 0
    to_use = max(1, math.trunc(len(questions) * rate))
    possible_points = 0.0
    talker.print_and_talk(f"I will ask {str(to_use)} questions.")

    for question in random.sample(questions, to_use):
        possible_points+=question['score']
        talker.print_and_talk(question['question'])
        answer = talker.ask('Fill in the blank:')
        if answer == "I'm done":
            return points, possible_points
        if answer.lower() == question['answer'].lower():
            talker.print_and_talk("You are correct!")
            points += question['score']
        else:
            talker.print_and_talk("Sorry, I was looking for:", question['answer'])
    talker.print_and_talk("You got ", points, "points out of", possible_points)
    return points, possible_points


def fetch_subject_file(subject):
    subject = subject.replace(' ', '_').lower()
    subject_file = 'subjects/' + subject + '.json'
    try:
        with open(subject_file) as f:
            data = f.read()
            return json.loads(data)
    except IOError as e:
        return None


def study_text(sentences):
    # print text.encode(sys.stdout.encoding, errors='replace')
    # text=unicodedata.normalize('NFKD',text).encode('ascii','replace')
    questions = clozure.make_study_set_sentences(sentences)
    return study_questions(questions, 0.75)

def study_text_complex_clozures(text):
    questions=rake.complex_clozures(text)
    mc.ask_questions(questions)
    
def study_paragraph(paragraph:dict,q_type='fill_in_the_blank'):
    questions=par.get_questions(paragraph)
    #fill in the blank
    if q_type=='fill_in_the_blank':
        score=study_questions(questions,0.3)
    elif q_type=='multiple_choice':
        score=mc.ask_questions(questions)
    paragraph['score']=score
    return paragraph

def study_section(document,selection):
    section = sd.get_section(document,selection)
    p_count=len(sec.get_paragraph_titles(section))
    section['points'] = (0, 0)
    if 'studied' not in section:
        section['studied']=(0,p_count)
    print("************************")
    print()
    print()
    talker.print_and_talk(section['title'])
    talker.print_and_talk("You have studied",section['studied'][0],"paragraphs out of",section['studied'][1])

    for i,paragraph in enumerate(sec.get_paragraphs(section).values()):
        print()
        for line in par.get_sentences(paragraph):
            talker.print_and_talk(line)
        print()
        talker.ask('Hit enter when ready.')
        # for i in range(30):
        #    print '.'
        paragraph = study_paragraph(paragraph)
        section=sec.update_paragraph(section,paragraph)

        if i+1>section['studied'][0]:
            section['studied']=(i+1,p_count)

        document=sd.update_section(document,section)

#def study_chunk(chunk):
#    while True:
#        talker.print_and_talk("What section would you like to study?")
#        selection=simple_menu.ask_list(chunk['section_list'])
#        if not selection:
#            return
#        study_section(chunk,selection)


def get_suggestion(subject):
    suggestions = wikipedia.search(subject)
    return suggestions[0]


def study_subject(subject):
    talker.print_and_talk("You want to learn about:", subject)
    chunk = fetch_subject_file(subject)
    if not chunk:
        talker.print_and_talk("I will ask wikipedia for the best suggestion")
        suggestion = get_suggestion(subject)
        talker.print_and_talk('"'+suggestion+'"', "was suggested by wikipedia.")
        chunk = fetch_subject_file(suggestion)
        if not chunk:
            article = wikipedia.page(suggestion)
            if not article:
                talker.print_and_talk("Sorry, I couldn't find an article on", suggestion)
                return
            chunk = col.make_chunk(article,suggestion)
            talker.print_and_talk("I have loaded the article on", suggestion)
        else:
            talker.print_and_talk("I found a local file for", suggestion)
    else:
        talker.print_and_talk("I found a local file for", subject)
    #study_chunk(chunk)


def study_text_file(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        text = f.read()
    study_text(text)

def study_section_file(filename):
    """Expects files in the section json format.
    uses that format to convert the file into a set of questions."""
    chunk=col.section_file_to_chunk(filename)
    talker.print_and_talk("I have loaded the file")
    study_chunk(chunk)

def study_study_doc(filepath:str):
    document=sd.read(filepath)
    while True:
        talker.print_and_talk("What section would you like to study?")
        selection,_=simple_menu.ask_list(sd.section_names(document))
        if not selection:
            return
        document=study_section(document,selection)
        sd.write(document,filepath)


def study_file(filename:str):
    text=''
    if filename.endswith("epub"):
        study_document_path=ebook.create_study_doc_path(filename)
        if os.path.exists(study_document_path):
            study_study_doc(study_document_path)
        document=ebook.create_full_doc(filename)
        study_study_doc(study_document_path)

    elif filename.endswith("pdf"):
        text=rpdf.to_text(filename)
    elif filename.endswith("txt"):
        with open(filename,encoding='utf-8') as f:
            text=f.read()
    else:
        raise ValueError(f'filename {filename} is of an unknown type based on file ending.')
    study_text_complex_clozures(text)

def learn_wikipedia_subjects():
    done = False
    while not done:
        answer = talker.ask('What wikipedia subject do you want to learn about?:')
        if answer == "I'm done" or answer.strip()=="":
            done = True
        else:
            study_subject(answer.lower())



def learn_all_the_things():
    done = False
    while not done:
        print("I understand: 'wikipedia' or 'a file' or 'I'm done'")
        answer = talker.ask('What do you want to learn about?:')
        if answer == "I'm done" or answer.strip()=="":
            done = True
        elif answer.lower() == "a file":
            file_name=talker.ask('Please enter the file you wish to learn')
            study_file(file_name)
        else:
            learn_wikipedia_subjects()



if __name__ == "__main__":
    # print wikipedia.search("harry potter")
    # study_file("text/saturn.txt")
    # talker.TALK = False
    # wikipedia.set_lang("simple")
    learn_all_the_things()
