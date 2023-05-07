from . import analysis, solve


def main():
    """Play all Worldes and print statistics."""

    num_guesses = solve.Solver().play()
    analysis.print_stats(num_guesses)
