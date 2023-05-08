import argparse

from . import analysis, solve


def main():
    parser = argparse.ArgumentParser(
        description="Play all Worldes and print statistics."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed for random module (default: None)",
    )

    args = parser.parse_args()
    num_guesses = solve.Solver().play_all(seed=args.seed)
    analysis.print_stats(num_guesses)
