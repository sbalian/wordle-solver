import random

from .solve import Solver


def game(
    answer: str,
    solver_: Solver,
    seed: int | None = 42,
) -> int:
    """Play a game and return the number of guesses to a solution."""

    random.seed(seed)
    num_guesses = 0
    candidates = set(solver_.words)
    hint = ""
    while hint.lower() != answer:
        guess = random.choice(list(candidates))
        num_guesses += 1
        hint, incorrect_positions = solver_.give_hint(guess, answer)
        candidates.remove(guess)
        candidates.intersection_update(
            solver_.find_candidates(hint, incorrect_positions)
        )
    return num_guesses


def all_games() -> list[int]:
    """Play all Worldes and return the number of guesses."""

    # Not reproducible even with seed, possibly because
    # of the ordering in the sets changing between runs

    solver_ = Solver()
    words = list(solver_.words)
    num_guesses = []
    for word in words:
        num_guesses.append(game(word, solver_))
    return num_guesses
