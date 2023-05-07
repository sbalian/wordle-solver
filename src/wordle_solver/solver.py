import collections
import pathlib
import string
from typing import TypedDict

import pkg_resources

ALPHABET = set(string.ascii_lowercase)


def load_words() -> list[str]:
    """Read possible guesses (source: https://gist.github.com/cfreshman)."""

    return (
        pathlib.Path(
            pkg_resources.resource_filename(
                "wordle_solver", "wordle-nyt-words-14855.txt"
            )
        )
        .read_text()
        .split()
    )


class Lookups(TypedDict):
    contains_at: dict[tuple[str, int], set[str]]
    does_not_contain: dict[str, set[str]]
    contains_not_at: dict[tuple[str, int], set[str]]


class Solver:
    def __init__(self) -> None:
        self.words = set(load_words())
        self.lookups = self.build_lookups()

    def build_lookups(self) -> Lookups:
        """Iterate over the words and populate lookups."""

        contains: dict[str, set[str]] = collections.defaultdict(lambda: set())
        does_not_contain: dict[str, set[str]] = collections.defaultdict(
            lambda: set()
        )
        contains_at: dict[tuple[str, int], set[str]] = collections.defaultdict(
            lambda: set()
        )

        for word in self.words:
            for position, letter in enumerate(word):
                contains[letter].add(word)
                contains_at[(letter, position)].add(word)
            for letter in ALPHABET - set(word):
                does_not_contain[letter].add(word)

        contains_not_at: dict[tuple[str, int], set[str]] = {}

        for letter in string.ascii_lowercase:
            for position in range(5):
                contains_not_at[(letter, position)] = (
                    contains[letter] - contains_at[(letter, position)]
                )

        return {
            "contains_at": dict(contains_at),
            "does_not_contain": dict(does_not_contain),
            "contains_not_at": dict(contains_not_at),
        }
