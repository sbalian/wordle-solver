import collections
import statistics


def print_stats(num_guesses: list[int]) -> None:
    avg_guesses = statistics.mean(num_guesses)
    print(f"Average number of guesses to a correct solution: {avg_guesses}")
    counts = collections.Counter(num_guesses)
    print("Number of guesses distribution")
    for guess, count in counts.items():
        print(f"{guess}: {count/len(num_guesses)*100}%")
    perc_games_won = sum([g < 7 for g in num_guesses]) / len(num_guesses) * 100
    print(f"Percentage of games won (up to 6 guesses): {perc_games_won}")
