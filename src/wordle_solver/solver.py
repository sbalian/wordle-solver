import pathlib

import pkg_resources


class Solver:
    def __init__(self) -> None:
        # Read possible guesses (from https://gist.github.com/cfreshman)
        words_path = pathlib.Path(
            pkg_resources.resource_filename(
                "wordle_solver", "wordle-nyt-words-14855.txt"
            )
        )
        self.words = words_path.read_text().split()
