import collections
import statistics

from . import solve


def print_stats(num_guesses: list[int]) -> None:
    """Print statistics given number of guesses to solutions.

    Parameters
    ----------
    num_guesses : list of int
        Number of guesses to solutions (e.g., from solver.Solver.play_all).
    """

    num_games = len(num_guesses)
    print(f"Number of games played: {num_games}")

    avg_guesses = statistics.mean(num_guesses)
    print(
        f"Average number of guesses to a correct solution: {avg_guesses:.2f}"
    )

    counts = collections.Counter(num_guesses)
    ordered_counts = {
        guess: counts.get(guess, 0.0) for guess in range(1, max(counts) + 1)
    }
    print("Number of guesses distribution (%):")
    for guess, count in ordered_counts.items():
        print(f"{guess}: {count/num_games*100.0:.2f}")

    perc_games_won = sum([ng < 7 for ng in num_guesses]) / num_games * 100
    print(f"Games won (up to 6 guesses): {perc_games_won:.2f} %")


def print_top_scores(limit: int = 10) -> None:
    """Print the top scores.

    Parameters
    ----------
    limit : int
        Print the top `limit` (default top 10).
    """

    scores = solve.load_sorted_scores()
    printed = 0
    for word, score in scores.items():
        if printed == limit:
            break
        print(word, score)
        printed += 1
