import pytest

from wordle_solver import solve


def test_load_words():
    words = solve._load_words()
    assert all(len(word) == 5 for word in words)
    assert len(set(words)) == len(words)
    assert all(word.islower() for word in words)
    assert len(words) == 14855


def test_solver_words(solver_):
    assert solver_._words == solve._load_words()


def test_lookups(solver_):
    for lookup in ["_contains_at", "_not_contains", "_contains_not_at"]:
        assert set.union(*(getattr(solver_, lookup).values())) == set(
            solver_._words
        )

    assert "apple" in solver_._contains_at[("a", 0)]
    assert "apple" not in solver_._contains_at[("b", 1)]

    assert "zebra" in solver_._not_contains["q"]
    assert "zebra" not in solver_._not_contains["z"]

    assert "apple" in solver_._contains_not_at[("a", 1)]
    assert "apple" not in solver_._contains_not_at[("a", 0)]
    assert "green" not in solver_._contains_not_at[("a", 0)]

    assert (
        set(letter for letter, _ in solver_._contains_at) == solver_._alphabet
    )
    assert set(letter for letter in solver_._not_contains) == solver_._alphabet
    assert (
        set(letter for letter, _ in solver_._contains_not_at)
        == solver_._alphabet
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
def test_possible_answers(
    test_hint, test_incorrect_positions, expected, solver_
):
    assert (
        solver_.possible_answers(
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
def test_give_hint(test_guess, test_answer, expected, solver_):
    assert solver_.give_hint(test_guess, test_answer) == expected
