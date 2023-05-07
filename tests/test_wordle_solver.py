from wordle_solver import solver


def test_load_words():
    words = solver.load_words()
    assert all(len(word) == 5 for word in words)
    assert len(set(words)) == len(words)
    assert all(word.islower() for word in words)
    assert len(words) == 14855


def test_solver_words(solver_class):
    assert solver_class.words == set(solver.load_words())


def test_lookups(solver_class):
    for lookup in solver_class.lookups.values():
        assert set.union(*(lookup.values())) == solver_class.words

    assert "apple" in solver_class.lookups["contains_at"][("a", 0)]
    assert "apple" not in solver_class.lookups["contains_at"][("b", 1)]

    assert "zebra" in solver_class.lookups["does_not_contain"]["q"]
    assert "zebra" not in solver_class.lookups["does_not_contain"]["z"]

    assert "apple" in solver_class.lookups["contains_not_at"][("a", 1)]
    assert "apple" not in solver_class.lookups["contains_not_at"][("a", 0)]
    assert "green" not in solver_class.lookups["contains_not_at"][("a", 0)]

    assert (
        set(letter for letter, _ in solver_class.lookups["contains_at"])
        == solver.ALPHABET
    )
    assert (
        set(letter for letter in solver_class.lookups["does_not_contain"])
        == solver.ALPHABET
    )
    assert (
        set(letter for letter, _ in solver_class.lookups["contains_not_at"])
        == solver.ALPHABET
    )
