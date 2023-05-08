# Wordle solver

This is work in progress (it is by no means an efficient implementation!).

Clone this repo, navigate to it and use `pip` to install in a virtual
environment:

```bash
git clone https://github.com/sbalian/wordle-solver.git

cd wordle-solver

virtualenv .venv --python=3.10
source .venv/bin/activate

python -m pip install -U pip
pip install .
```

To solve all Wordles:

```bash
time wordle-solver
```

You should see something like this:

```text
Number of games played: 14855
Average number of guesses to a correct solution: 5.30
Number of guesses distribution (%):
1: 0.01
2: 0.96
3: 8.63
4: 23.63
5: 27.87
6: 20.19
7: 10.18
8: 4.55
9: 2.11
10: 1.01
11: 0.50
12: 0.24
13: 0.10
14: 0.02
Games won (up to 6 guesses): 81.29 %
wordle-solver  67.62s user 0.64s system 1220% cpu 5.592 total
```

To run the tests locally:

```bash
pip install -U tox
tox
```
