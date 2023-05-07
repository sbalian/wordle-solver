import pytest

from wordle_solver import solver


def test_load_words():
    words = solver.load_words()
    assert all(len(word) == 5 for word in words)
    assert len(set(words)) == len(words)
    assert all(word.islower() for word in words)
    assert len(words) == 14855


def test_solver_words(solver_class):
    assert solver_class.words == solver.load_words()


def test_lookups(solver_class):
    for lookup in solver_class.lookups.values():
        assert set.union(*(lookup.values())) == set(solver_class.words)

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


@pytest.mark.parametrize(
    "test_hint,test_incorrect_positions,expected",
    [
        ("HELPS", None, set(["helps"])),
        ("AWAek", set([3, 4]), set(["awake"])),
        ("HEplS", set([2, 3]), set(["helps"])),
        ("Gohts", set([1, 2, 3, 4]), set(["ghost"])),
        ("pPael", set([0, 2, 3, 4]), set(["apple"])),
        (
            "elapp",
            set([0, 1, 2, 3, 4]),
            set(["appel", "apple", "lapel", "palea", "pepla"]),
        ),
        ("praps", set([0, 1, 2, 3, 4]), set([])),
        ("hsARE", set([0, 1]), set(["share"])),
        ("APPLc", None, set(["apple", "apply"])),
        (
            "AddLE",
            None,
            set(
                [
                    "abele",
                    "agile",
                    "ahole",
                    "aisle",
                    "aizle",
                    "amble",
                    "amole",
                    "ample",
                    "ancle",
                    "anele",
                    "angle",
                    "anile",
                    "ankle",
                    "anole",
                    "apple",
                    "argle",
                    "avale",
                    "axile",
                    "azole",
                ]
            ),
        ),
        ("ApsiS", set([1]), set(["aapas", "alaps", "arpas", "ataps"])),
    ],
)
def test_find_candidates(
    test_hint, test_incorrect_positions, expected, solver_class
):
    assert (
        solver_class.find_candidates(
            test_hint, incorrect_positions=test_incorrect_positions
        )
        == expected
    )


@pytest.mark.parametrize(
    "test_guess,test_answer,expected",
    [
        ("speak", "stays", ("Speak", set([3]))),
        ("speak", "speak", ("SPEAK", set([]))),
        ("leapp", "apple", ("leapp", set([0, 1, 2, 3, 4]))),
        ("eplap", "apple", ("ePlap", set([0, 2, 3, 4]))),
    ],
)
def test_give_hint(test_guess, test_answer, expected, solver_class):
    assert solver_class.give_hint(test_guess, test_answer) == expected
