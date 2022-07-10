import know_it_all.text_processor.rake as rake


def test_1_word_rake():
    result=rake.rake_phrases([['one']])
    assert result==[[1.0,'one']]

def test_1_word_2_rake():
    result=rake.rake_phrases([['one'],['one']])
    assert result==[[1.0,'one']]

def test_2_word_1_rake():
    result=rake.rake_phrases([['one', 'two']])
    assert result==[[4.0,'one two']]


def test_3_word_2_rake():
    result=rake.rake_phrases([['one'],['one', 'two']])
    assert result==[[1.5, 'one'],
                    [3.5,'one two']]
