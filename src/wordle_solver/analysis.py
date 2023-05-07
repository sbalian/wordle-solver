import collections
import statistics


def print_stats(num_guesses: list[int]) -> None:
    num_games = len(num_guesses)
    print(f"Number of games played: {num_games}")
    avg_guesses = statistics.mean(num_guesses)
    print(
        f"Average number of guesses to a correct solution: {avg_guesses:.2f}"
    )
    counts = collections.Counter(num_guesses)
    ordered_counts = {
        guess: counts.get(guess, 0) for guess in range(1, max(counts) + 1)
    }
    print("Number of guesses distribution (%):")
    for guess, count in ordered_counts.items():
        print(f"{guess}: {count/len(num_guesses)*100:.2f}")
    perc_games_won = sum([g < 7 for g in num_guesses]) / len(num_guesses) * 100
    print(f"Games won (up to 6 guesses): {perc_games_won:.2f} %")
