import os

from apps.check_residual_tool import CheckResidual, TIME_PATTERN, SOLVER_PATTERN
from pytest import fixture

@fixture
def testing_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data_for_tests', 'check_residual_test_data.run')
    return file_path

def test_find_time_step_and_residual(testing_data):
    t = CheckResidual(time_pattern=TIME_PATTERN, solver_pattern=SOLVER_PATTERN)
    t.find_time_step_and_residuals(testing_data)
    r = t.get_result()
    assert r == [('0.300024', '111', '222', '333'), ('0.300048', '2.0084695e-11', '2.6502596e-09', '1.4049786e-08')]
