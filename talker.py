__author__ = 'mrittha'

import re
import textwrap
import pyttsx


def make_speech_engine():
    engine = pyttsx.init()
    engine.setProperty('rate', 150)
    return engine


SPEAKER = make_speech_engine()
TALK = True


def speak(engine, text):
    if TALK:
        engine.say(text)
        engine.runAndWait()


def t_from_args(args):
    text = [str(a) for a in args]
    text = ' '.join(text)
    return text


def ask(*args):
    text = t_from_args(args)
    print textwrap.fill(text,80),
    speak(SPEAKER, text)
    answer = raw_input(":")
    return answer


def print_and_talk(*args):
    text = t_from_args(args)
    print textwrap.fill(text,80)
    speak(SPEAKER, text)


def print_and_talk_clozure(*args):
    text = t_from_args(args)
    talk_text = re.sub('_+', 'blank', text)
    print textwrap.fill(text,80)
    speak(SPEAKER, talk_text)


if __name__ == "__main__":
    print_and_talk("testing.")
    response = ask("How are you?")
    print_and_talk(response)
