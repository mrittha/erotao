__author__ = 'mrittha'

import math
import random
import codecs
import json
import wikipedia
import os
import clozure
import talker
import chunk_o_learning
import simple_menu


def study_questions(questions, rate):
    if len(questions) < 1:
        return 0, 0
    points = 0
    to_use = max(1, math.trunc(len(questions) * rate))
    total_points = to_use
    if total_points > 1:
        talker.print_and_talk("I will ask " + str(total_points) + " questions.")
    else:
        talker.print_and_talk("I will ask " + str(total_points) + " question.")
    for question in random.sample(questions, to_use):
        talker.print_and_talk_clozure(question['clozure'])
        answer = talker.ask('Fill in the blank:')
        if answer == "I'm done":
            return None
        if answer.lower() == question['word'].lower():
            talker.print_and_talk("You are correct!")
            points += 1
        else:
            talker.print_and_talk("Sorry, I was looking for:", question['word'])
    talker.print_and_talk("You got ", points, "points out of", total_points)
    return points, total_points


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







def study_section(chunk,selection):
    section = chunk['sections'][selection[0]]
    p_count=len(section['paragraphs'])
    section['points'] = (0, 0)
    if 'studied' not in section:
        section['studied']=(0,p_count)
    print "************************"
    print
    print
    talker.print_and_talk(section['full_title'])
    talker.print_and_talk("You have studied",section['studied'][0],"paragraphs out of",section['studied'][1])

    for i,paragraph in enumerate(section['paragraphs']):
        print
        for line in paragraph:
            talker.print_and_talk(line)
        print
        talker.ask('Hit enter when ready.')
        # for i in range(30):
        #    print '.'
        new_points = study_text(paragraph)
        if new_points is None:
            return
        if i+1>section['studied'][0]:
            section['studied']=(i+1,p_count)
        old_points = section.get('points', (0, 0))
        section['points'] = (old_points[0] + new_points[0], old_points[1] + new_points[1])
        chunk_o_learning.update_chunk(chunk)

def study_chunk(chunk):
    while True:
        talker.print_and_talk("What section would you like to study?")
        selection=simple_menu.ask_list(chunk['section_list'])
        if not selection:
            return
        study_section(chunk,selection)


def study_file(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        text = f.read()
    study_text(text)


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
            chunk = chunk_o_learning.make_chunk(article,suggestion)
            talker.print_and_talk("I have loaded the article on", suggestion)
        else:
            talker.print_and_talk("I found a local file for", suggestion)
    else:
        talker.print_and_talk("I found a local file for", subject)
    study_chunk(chunk)


def learn_all_the_things():
    done = False
    while not done:
        answer = talker.ask('What subject do you want to learn about?:')
        if answer == "I'm done":
            done = True
        else:
            study_subject(answer.lower())


if __name__ == "__main__":
    # print wikipedia.search("harry potter")
    # study_file("text/saturn.txt")
    # talker.TALK = False
    # wikipedia.set_lang("simple")
    learn_all_the_things()
