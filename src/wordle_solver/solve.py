import collections
import concurrent.futures
import functools
import random
import string
from importlib import resources
from typing import TypedDict

ALPHABET = set(string.ascii_lowercase)


def load_words() -> list[str]:
    """Read possible guesses (source: https://gist.github.com/cfreshman)."""

    return resources.read_text(
        "wordle_solver", "wordle-nyt-words-14855.txt"
    ).splitlines()


class Lookups(TypedDict):
    contains_at: dict[tuple[str, int], set[str]]
    does_not_contain: dict[str, set[str]]
    contains_not_at: dict[tuple[str, int], set[str]]


class Solver:
    def __init__(self) -> None:
        self.words = load_words()
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

    def find_candidates(
        self,
        hint: str,
        incorrect_positions: set[int] | None = None,
    ) -> set[str]:
        """Return possible Wordle solutions given a hint.

        hint is a 5-letter word specification. Use uppercase letters
        to indicate letters in the correct position (green) and
        lowercase letters to indicate letters that are either in the
        incorrect position (orange) or do not exist in the word
        (dark grey). Use incorrect_positions to indicate the indices
        in the hint for the letters that exist in the word but are
        incorrectly positioned (i.e., color letters orange using
        these indices).

        For example, hint = 'Tseta' and incorrect_positions = set([1, 3])
        specify that the word starts with a T, contains s and another
        t but in incorrect positions and does not contain an a.
        """

        if incorrect_positions is None:
            incorrect_positions = set()

        if len(hint) != 5:
            raise ValueError(f"hint: {hint} must be of length 5")
        if len(incorrect_positions) > 5:
            raise ValueError("length of incorrect_positions must be at most 5")
        for incorrect_position in incorrect_positions:
            if not (0 <= incorrect_position < 5):
                raise ValueError(
                    f"incorrect position {incorrect_position} out of bounds"
                )

        word_sets = []
        letters_in_incorrect_positions = set(
            [hint[position] for position in incorrect_positions]
        )
        letters_in_correct_positions = set(
            [
                hint[position].lower()
                for position, letter in enumerate(hint)
                if letter.isupper()
            ]
        )
        for position, letter in enumerate(hint):
            upper_letter = letter.isupper()
            position_in_incorrect_positions = position in incorrect_positions
            if upper_letter and position_in_incorrect_positions:
                raise ValueError(
                    "correct letter (upper) position cannot be in "
                    "incorrect_positions"
                )
            elif upper_letter:
                word_sets.append(
                    self.lookups["contains_at"][(letter.lower(), position)]
                )
            elif position_in_incorrect_positions:
                word_sets.append(
                    self.lookups["contains_not_at"][(letter, position)]
                )
            elif letter not in letters_in_incorrect_positions.union(
                letters_in_correct_positions
            ):
                word_sets.append(self.lookups["does_not_contain"][letter])

        if len(incorrect_positions) == 5:
            for letter in ALPHABET - set(hint.lower()):
                word_sets.append(self.lookups["does_not_contain"][letter])
        return set.intersection(*word_sets)

    @staticmethod
    def give_hint(guess: str, answer: str) -> tuple[str, set[int]]:
        """Get a hint and incorrect letter positions for a guess and answer."""

        guess = guess.lower()
        answer = answer.lower()

        if len(guess) != 5:
            raise ValueError("guess must be of length 5")
        if len(answer) != 5:
            raise ValueError("answer must be of length 5")
        if not guess.isalpha():
            raise ValueError("guess must be alphabetic")
        if not answer.isalpha():
            raise ValueError("answer must be alphabetic")

        answer_positions = list(range(5))
        correct_positions = set([])
        incorrect_positions = set([])

        for guess_position, guess_letter in enumerate(guess):
            if answer[guess_position] == guess_letter:
                answer_positions.remove(guess_position)
                correct_positions.add(guess_position)

        for guess_position, guess_letter in enumerate(guess):
            if guess_position in correct_positions:
                continue
            found_orange = False
            for answer_position in answer_positions:
                if answer[answer_position] == guess_letter:
                    found_orange = True
                    break
            if found_orange:
                incorrect_positions.add(guess_position)
                answer_positions.remove(answer_position)

        hint = ""
        for i in range(5):
            if i in correct_positions:
                hint += guess[i].upper()
            else:
                hint += guess[i]
        return hint, incorrect_positions

    def game(
        self,
        answer: str,
        seed: int | None = 42,
    ) -> int:
        """Play a game and return the number of guesses to a solution."""

        random.seed(seed)
        num_guesses = 0
        candidates = set(self.words)
        hint = ""
        while hint.lower() != answer:
            # This sorting is inefficient but guarantees reproducibility
            # (roughly doubles Solver.play running time)
            guess = random.choice(sorted(list(candidates)))
            num_guesses += 1
            hint, incorrect_positions = self.give_hint(guess, answer)
            candidates.remove(guess)
            candidates.intersection_update(
                self.find_candidates(hint, incorrect_positions)
            )
        return num_guesses

    def play(self) -> list[int]:
        """Play all Worldes and return the number of guesses."""

        words = list(self.words)
        num_guesses = []

        game_ = functools.partial(self.game, seed=42)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            num_guesses = list(executor.map(game_, words, chunksize=1000))
        return num_guesses
