def test_words(solver_class):
    words = solver_class.words
    assert all(len(word) == 5 for word in words)
    assert len(set(words)) == len(words)
    assert all(word.islower() for word in words)
