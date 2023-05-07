import pathlib

import pkg_resources


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


class Solver:
    def __init__(self) -> None:
        self.words = set(load_words())
