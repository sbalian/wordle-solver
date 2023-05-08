import collections
import concurrent.futures
import functools
import random
import string
from importlib import resources
from typing import DefaultDict


def _load_words() -> list[str]:
    """Read possible guesses (5-letter words) from file.

    Source: https://gist.github.com/cfreshman.

    Returns
    -------
    list of str:
        A list of allowed Wordle words.
    """

    return resources.read_text(
        "wordle_solver", "wordle-nyt-words-14855.txt"
    ).splitlines()


class Solver:
    _alphabet = set(string.ascii_lowercase)

    def __init__(self) -> None:
        """Solve Wordles using lookup tables from a list of 5-letter words."""

        self._words: list[str] = _load_words()

        # Iterate over the words and build lookups

        # Contains a letter
        self._contains: DefaultDict[str, set[str]] = collections.defaultdict(
            set
        )
        # Does not contain a letter
        self._not_contains: DefaultDict[
            str, set[str]
        ] = collections.defaultdict(set)
        # Contains a letter at a position
        self._contains_at: DefaultDict[
            tuple[str, int], set[str]
        ] = collections.defaultdict(set)
        for word in self._words:
            for position, letter in enumerate(word):
                self._contains[letter].add(word)
                self._contains_at[(letter, position)].add(word)
            for letter in self._alphabet - set(word):
                self._not_contains[letter].add(word)
        # Contains a letter but not at the given position
        self._contains_not_at: DefaultDict[
            tuple[str, int], set[str]
        ] = collections.defaultdict(set)
        for letter in string.ascii_lowercase:
            for position in range(5):
                self._contains_not_at[(letter, position)] = (
                    self._contains[letter]
                    - self._contains_at[(letter, position)]
                )

    def possible_answers(
        self,
        hint: str,
        incorrect_positions: set[int] | None = None,
    ) -> set[str]:
        """Returns possible answers given a hint and wrong letter positions.

        For example, `hint` = 'Tseta' and `incorrect_positions` = set([1, 3]),
        specify that the word starts with a T, contains s and another t
        in incorrect positions and does not contain an a.

        Parameters
        ----------
        hint : str
            A 5-character string in which uppercase letters indicate letters
            in the correct position (green in the UI) and lowercase letters
            indicate letters that are either in the incorrect positions
            (orange) or do not exist in the word (grey in the UI).
        incorrect_positions: set of int or None, optional
            The indices in `hint` for letters that exist in the word but
            in the incorrect positions (orange in the UI). Set this to None
            for an empty set (the default).

        Returns
        -------
        set of str:
            Possible answers.

        Raises
        ------
        ValueError
            If `hint` is not of length 5.
        ValueError
            If `incorrect_positions` is not a subset of {0, 1, 2, 3, 4}.
        ValueError
            If an index in `incorrect_positions` matches the position of an
            uppercase letter in `hint`.
        """

        if incorrect_positions is None:
            incorrect_positions = set()

        if len(hint) != 5:
            raise ValueError(f"hint '{hint}' must be of length 5")
        if not incorrect_positions.issubset(set(range(5))):
            raise ValueError(
                f"incorrect positions '{incorrect_positions}' is not a "
                f"subset of {set(range(5))}"
            )

        for incorrect_position in incorrect_positions:
            if hint[incorrect_position].isupper():
                raise ValueError(
                    f"incorrect position '{incorrect_position}' cannot point "
                    "to an uppercase letter"
                )

        # The output will be the intersection of these sets
        word_sets: list[set[str]] = []

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
            if upper_letter:
                word_sets.append(self._contains_at[(letter.lower(), position)])
            elif position_in_incorrect_positions:
                word_sets.append(self._contains_not_at[(letter, position)])
            elif letter not in letters_in_incorrect_positions.union(
                letters_in_correct_positions
            ):
                word_sets.append(self._not_contains[letter])

        if len(incorrect_positions) == 5:
            for letter in self._alphabet - set(hint.lower()):
                word_sets.append(self._not_contains[letter])
        return set.intersection(*word_sets)

    def give_hint(
        self, guess: str, answer: str, word_check: bool = False
    ) -> tuple[str, set[int]]:
        """Get a hint and incorrect letter positions for a guess and answer.

        Parameters
        ----------
        guess : str
        answer : str
        word_check : bool, optional
            Check if `guess` and `answer` are in the allowed list of words.
            Defaults to False.

        Returns
        -------
        tuple of a str and a set of int
            The hint string and the indicies of incorrectly positioned letters
            (see also: Solver.possible_answers docstring).

        Raises
        ------
        ValueError
            If `guess` or `answer` are not in the list of allowed words and
            if `word_check` is True.
        ValueError
            If the guess or the answer are not of length 5 and are not
            alphabetic.
        """

        if word_check:
            if guess not in self._words:
                raise ValueError(f"guess '{guess}' is not an allowed word")
            if answer not in self._words:
                raise ValueError(f"answer '{answer}' is not an allowed word")

        correct_guess_positions: set[int] = set()
        guess_letters_not_in_answer: set[str] = set()
        guess_positions_not_in_answer: set[int] = set()
        possible_incorrect_guess_positions_by_letter: DefaultDict[
            str, list[int]
        ] = collections.defaultdict(list)

        for guess_position, guess_letter in enumerate(guess):
            if answer[guess_position] == guess_letter:
                correct_guess_positions.add(guess_position)
            elif guess_letter not in answer:
                guess_letters_not_in_answer.add(guess_letter)
                guess_positions_not_in_answer.add(guess_position)
            else:
                possible_incorrect_guess_positions_by_letter[
                    guess_letter
                ].append(guess_position)

        answer_without_matched_letters: list[str] = []
        for position, letter in enumerate(answer):
            if position not in correct_guess_positions:
                answer_without_matched_letters.append(letter)

        answer_without_matched_letters_counts = collections.Counter(
            answer_without_matched_letters
        )

        for letter in possible_incorrect_guess_positions_by_letter.keys():
            while (
                len(possible_incorrect_guess_positions_by_letter[letter])
                > answer_without_matched_letters_counts[letter]
            ):
                possible_incorrect_guess_positions_by_letter[letter].pop(-1)

        hint = ""
        for guess_position, guess_letter in enumerate(guess):
            if guess_position in correct_guess_positions:
                hint += guess_letter.upper()
            else:
                hint += guess_letter

        incorrect_positions: set[int] = set()
        for positions in possible_incorrect_guess_positions_by_letter.values():
            for position in positions:
                incorrect_positions.add(position)

        return hint, incorrect_positions

    def play(
        self,
        answer: str,
        seed: int | None = 42,
    ) -> int:
        """Play a game and return the number of guesses to the solution.

        Always finds the answer.

        Parameters
        ----------
        answer : str
            The answer.
        seed : int or None, optional
            The seed passed to random.seed (used for randomly choosing
            from possible candidates). Defaults to 42.

        Returns
        -------
        int
            Number of guesses to the solution.
        """

        random.seed(seed)
        num_guesses = 0
        candidates = set(self._words)
        hint = ""
        while hint.lower() != answer:
            if seed is not None:
                # This sorting is inefficient but guarantees reproducibility
                # (roughly doubles Solver.play running time)
                guess = random.choice(sorted(list(candidates)))
            else:
                guess = random.choice(list(candidates))

            num_guesses += 1
            hint, incorrect_positions = self.give_hint(guess, answer)
            candidates.remove(guess)
            candidates.intersection_update(
                self.possible_answers(hint, incorrect_positions)
            )
        return num_guesses

    def play_all(
        self, seed: int | None = 42, chunksize: int = 1000
    ) -> list[int]:
        """Play all Wordles and return the number of guesses to the solutions.

        Calls Solver.play on all words and runs in parallel using
        multiprocessing.

        Parameters
        ----------
        seed : int or None, optional
            The seed passed to random.seed (used for randomly choosing
            from possible candidates). Defaults to 42.
        chunksize : int
            Passed to concurrent.futures.ProcessPoolExecutor.map (default
            1000). Change this if the function runs for too long.
            On Intel Core i7-12700H with 20 cores and 32 GB of RAM, it takes
            about 10 seconds to play all Wordles.

        Returns
        -------
        list of int
            Number of guesses to the solution for all Wordles.
        """

        words = list(self._words)
        num_guesses = []

        game = functools.partial(self.play, seed=seed)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            num_guesses = list(executor.map(game, words, chunksize=chunksize))
        return num_guesses
