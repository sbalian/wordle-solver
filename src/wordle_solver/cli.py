import argparse
import json

from . import analysis, solve


def play_all() -> None:
    parser = argparse.ArgumentParser(
        description="Play all Worldes and print statistics."
    )
    parser.parse_args()
    num_guesses = solve.Solver().play_all()  # uses multiprocessing
    analysis.print_stats(num_guesses)


def average_scores() -> None:
    parser = argparse.ArgumentParser(description="Print average word scores.")
    parser.parse_args()

    print("Calculating scores ...")
    scores = solve.Solver().average_hint_scores()
    with open("scores.json", "w") as f:
        json.dump(scores, f)
    print("Wrote to scores.json")
