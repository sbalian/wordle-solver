import pytest

from wordle_solver import solve


@pytest.fixture
def solver_():
    return solve.Solver()
