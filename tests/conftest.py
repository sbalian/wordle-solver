import pytest

from wordle_solver import solver


@pytest.fixture
def solver_class():
    return solver.Solver()
