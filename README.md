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
Average number of guesses to a correct solution: 4.97
Number of guesses distribution (%):
1: 0.01
2: 1.43
3: 14.29
4: 31.20
5: 24.25
6: 13.29
7: 7.28
8: 3.81
9: 2.05
10: 1.16
11: 0.65
12: 0.32
13: 0.15
14: 0.07
15: 0.03
Games won (up to 6 guesses): 84.47 %
wordle-solver  50.02s user 1.83s system 738% cpu 7.020 total
```

To run the tests locally:

```bash
pip install -U tox
tox -r
```
