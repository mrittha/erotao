__author__ = 'mrittha'

import math
import random
import codecs

import wikipedia

import clozure
import talker
import chunk_o_learning


def study_questions(questions, rate):
    if len(questions) < 1:
        return 0, 0
    points = 0
    to_use = max(1, math.trunc(len(questions) * rate))
    total_points = to_use
    talker.print_and_talk("I will ask " + str(total_points) + " questions.")
    for question in random.sample(questions, to_use):
        talker.print_and_talk_clozure(question['clozure'])
        answer = talker.ask('Fill in the blank:')
        if answer == "I'm done":
            return (0, 0)
        if answer.lower() == question['word'].lower():
            talker.print_and_talk("You are correct!")
            points += 1
        else:
            talker.print_and_talk("Sorry, I was looking for:", question['word'])
    talker.print_and_talk("You got ", points, "points out of", total_points)
    return points, total_points


def fetch_article(subject):
    talker.print_and_talk("You want to learn about:", subject)
    talker.print_and_talk("I will ask wikipedia for the best suggestion")
    suggestions = wikipedia.search(subject)
    talker.print_and_talk(suggestions[0], "was suggested by wikipedia.")
    article = wikipedia.page(suggestions[0])
    if article:
        talker.print_and_talk("I have loaded the article on", suggestions[0])
    # print article.content
    return article


def study_text(sentences):
    # print text.encode(sys.stdout.encoding, errors='replace')
    # text=unicodedata.normalize('NFKD',text).encode('ascii','replace')
    questions = clozure.make_study_set_sentences(sentences)
    return study_questions(questions, 0.75)


def study_article(article):
    chunk = chunk_o_learning.make_chunk(article)
    for section_title in chunk['section_list']:
        section = chunk['sections'][section_title]
        section['points'] = (0, 0)
        print "************************"
        print
        print
        talker.print_and_talk(section['full_title'])

        for paragraph in section['paragraphs']:
            print
            for line in paragraph:
                talker.print_and_talk(line)
            print
            talker.ask('Hit enter when ready.')
            # for i in range(30):
            #    print '.'
            new_points = study_text(paragraph)
            old_points = section.get('points', (0, 0))
            section['points'] = (old_points[0] + new_points[0], old_points[1] + new_points[1])


def study_file(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        text = f.read()
    study_text(text)


def study_subject(subject):
    article = fetch_article(subject)
    if article:
        study_article(article)
    else:
        talker.print_and_talk("Sorry, I couldn't find an article on", subject)


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
    talker.TALK = False
    # wikipedia.set_lang("simple")
    learn_all_the_things()
