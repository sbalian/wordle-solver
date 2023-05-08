import pytest

import wordle_solver


@pytest.fixture
def solver_():
    return wordle_solver.Solver()
