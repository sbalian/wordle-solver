from wordle_solver import solver


def test_load_words():
    words = solver.load_words()
    assert all(len(word) == 5 for word in words)
    assert len(set(words)) == len(words)
    assert all(word.islower() for word in words)
    assert len(words) == 14855
