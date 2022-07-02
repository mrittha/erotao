__author__ = 'mrittha'
"""Based on the code from http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
"""

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from spacy import English

from heapq import nlargest

nlp = English()


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        """
          Compute the frequency of each of word.
          Input:
           word_sent, a list of sentences already tokenized.
          Output:
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in freq.keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def summarize(self, text, n):
        """
          Return a list of n sentences
          which represent the summary of text.
        """
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]


def summarize_spacy(self, text, n):
    """
      Return a list of n sentences
      which represent the summary of text.
    """
    doc = nlp(text)
    sents = [sent.string.strip() for sent in doc]
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i, sent in enumerate(word_sent):
        for w in sent:
            if w in self._freq:
                ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)
    return [sents[j] for j in sents_idx]


def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)


if __name__ == "__main__":
    text = """
 Many researchers have investigated and speculated about the link between information technology and organizational structure with very mixed results. This paper suggests that part of the reason for these mixed results is the coarseness of previous analyses of both technology and structure The paper describes a new and much more detailed perspective for investigating this link. Using concepts of object-oriented programming from artificial intelligence, the information processing that occurs in organizations is characterized in terms of the kinds of messages people exchange and the ways they process those messages The utility of this approach is demonstrated through the analysis of a case in which a reduction in levels of management is coupled with the introduction of a computer conferencing system The detailed model developed for this case helps explain both macro-level data about the changes in the organizational structure, and micro-level data about individuals' use of the svstem.

Introduction

Since soon after the invention of computers, researchers have attempted to investigate the relationship between information technology (IT) and organizational structure. For instance, as long ago as in 1958, Leavitt and Whisler predicted that IT would lead to a dramatic reduction in numbers of middle managers. Recently there has been a flood of articles in the popular business press describing individual organizations where the introduction of IT seems to be associated with large organizational changes (Business Week, 1984, 1985). We are thus apparently beginning to see the effects of IT, but as yet we understand them only vaguely.

Our research involves a new perspective to investigate this link. The technique analyzes information processing in organizations in a much more detailed way than most previous work. Using concepts of object-oriented programming from artificial intelligence, we characterize the information processing that occurs in organizations in terms of the kinds of messages people exchange and the ways they process those messages The models that can be developed using these object-oriented concepts have more of the precision and flavour of cognitive science theories than most previous models based on the information processing view of organizations.

We begin with a review of the literature on the impact of IT on organizations, from which we develop a new information processing approach to the problem. The utility of this technique is demonstrated through the analysis of a case, one in which a reduction in levels of management is coupled with the introduction of a computer conferencing system. The model developed in this case agrees with data about the changes in the organizational structure, qualitative comments about changes in job roles and detailed analyses of message contents We conclude by sketching possible future directions for research using our perspective.
    """
    fs = FrequencySummarizer()
    sentences = fs.summarize(text, 3)
    print("nltk sentences")
    for s in sentences:
        print(s)
    print()

    print ("spacy sentences")
    sentences = fs.summarize_spacy(text, 3)
    for s in sentences:
        print s
