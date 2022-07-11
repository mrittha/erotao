"""
Contains utilities to present and evaluate a set of questions using multi_choice algorithm

"""
import random
import know_it_all.cli.simple_menu as sm
import know_it_all.cli.talker as talker

def random_answers(questions,selected):
    sample_questions=random.sample(questions,min(len(questions),10))
    answers=[]
    for question in sample_questions:
        if question['answer']!=selected['answer']:
            answers.append(question['answer'])
    all_answers=answers[:4]+[selected['answer']]
    random.shuffle(all_answers)
    return all_answers

def ask_questions(questions:'list[dict]',count:int):
    """
    questions are expected to be a list of dictionaries
    with a entries for 'question', 'answer'
    """

    #first randomly pick count questions:
    to_ask=random.sample(questions,count)
    score=0.0
    available_score=sum([ q['score'] for q in to_ask])
    for question in to_ask:
        answers=random_answers(questions,question)
        talker.print_and_talk(question['question'])
        answer,_=sm.ask_list(answers)
        if answer.lower()==question['answer'].lower():
            score=score+question['score']
            talker.print_and_talk(f'{answer} is correct!')
        else:
            talker.print_and_talk(f'{answer} is incorrect!')
            talker.print_and_talk(f"The correct answer is: {question['answer']}")
    talker.print_and_talk(f"You got {score} out of {available_score}")
    return score


