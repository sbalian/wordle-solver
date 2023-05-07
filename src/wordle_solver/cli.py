from . import analysis, play


def main():
    """Play all Worldes and print statistics."""

    num_guesses = play.all_games()
    analysis.print_stats(num_guesses)
