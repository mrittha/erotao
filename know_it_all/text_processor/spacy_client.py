import spacy
from pprint import pprint
nlp = spacy.load('en_core_web_lg')

EXTRA_STOP=["et","al"]

def include_token(token):
    return (not token.is_punct 
            and not token.is_space 
            and not token.is_stop 
            and not token.is_oov 
            and len(token) > 1 
            and not token.like_num 
            and token.text not in EXTRA_STOP)

def end_phrase(token):
    #don't end a phrase on a space.
    return (token.is_punct 
            or token.is_stop 
            or token.is_oov 
            or len(token.text) <= 1  
            or token.like_num 
            or token.text in EXTRA_STOP)

def add_phrase(phrases,doc,current_phrase):
    if current_phrase != []:
        span = doc[current_phrase[0].i:current_phrase[-1].i + 1]
        if span.text != '':
            phrases.append([tok.lower_ for tok in span])
    return phrases


def get_noun_phrases(text):
    """
    Process the text look for noun phrases (noun chunks in spacy terms)
    filters out spaces, stops and numbers etc.  returns a list of phrases
    
    """
    doc = nlp(text)
    phrases = []
    for chunk in doc.noun_chunks:
        current_phrase = []
        for tok in chunk:
            if include_token(tok):
                current_phrase.append(tok)
            elif end_phrase(tok) and current_phrase != []:
                phrases=add_phrase(phrases,doc,current_phrase)
                current_phrase = []
            else:
                pass
        
        #process the final phrase since we are no longer in the for loop
        if current_phrase != []:
             phrases=add_phrase(phrases,doc,current_phrase)
    return phrases


if __name__=='__main__':
    text="""
    Deep learning algorithms involve optimization in many contexts. 
    For example,performing inference in models such as PCA involves solving an optimization problem.
    We often use analytical optimization to write proofs or design algorithms.
    Of all the many optimization problems involved in deep learning, 
    the most diﬃcultis neural network training. 
    It is quite common to invest days to months of time on hundreds 
    of machines to solve even a single instance of the neural network training problem. 
    Because this problem is so important and so expensive, 
    a specialized set of optimization techniques have been developed for solving it. 
    This chapter presents these optimization techniques for neural network training.
    """
    pprint(get_noun_phrases(text))