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
Average number of guesses to a correct solution: 5.18
Number of guesses distribution (%):
1: 0.01
2: 0.98
3: 10.22
4: 25.37
5: 28.70
6: 18.01
7: 8.62
8: 4.13
9: 2.14
10: 1.02
11: 0.51
12: 0.24
13: 0.05
Games won (up to 6 guesses): 83.29 %
wordle-solver  104.57s user 0.36s system 1300% cpu 8.067 total
```

To run the tests locally:

```bash
pip install -U tox
tox
```
