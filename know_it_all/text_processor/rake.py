from toolz import frequencies, concat
from pprint import pprint

def word_score(token, degree, counts):
    """
    Each word has score which effectively is lowered for words
    which are more common in the text and raised for words that 
    appear in longer phrases.   So the highest score will be for words
    that appear one time in a long phrase.
    """
    return degree.get(token, 0) / counts.get(token, 1)


def rake_phrases(phrases):
    """
    we expect phrases to be a list of lists of strings, all lowercase
    """
    counts = frequencies([p for p in concat(phrases)])
    #pprint(counts)
    
    degree = {}
    for phrase in phrases:
        d = len(phrase)
        # the degree of each word is the sum of all the lengths
        # of phrases it appears in
        for word in phrase:
            degree[word] = degree.get(word, 0.0) + d
    
    #pprint(degree)
    phrase_scores = []
    seen_phrase = set()
    
    
    for phrase in phrases:

        #the phrase score is the sum of all the word scores in the phrase
        score = sum([word_score(word, degree, counts) for word in phrase])
        
        #need to create immutable object for use in set
        phrase_string=' '.join(phrase)

        if phrase_string not in seen_phrase:
            
            phrase_scores.append([score, phrase_string])
            seen_phrase.add(phrase_string)

    return phrase_scores

        
        
