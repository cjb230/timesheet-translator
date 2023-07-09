# from ..timesheet_translator import utils as u

import timesheet_translator.utils as u


def test_hours_to_string():
    assert u.hours_to_string(2.75) == "2:45"
    assert u.hours_to_string(0.083) == "0:05"
    assert u.hours_to_string(0.5) == "0:30"
    assert u.hours_to_string(1.25) == "1:15"
    assert u.hours_to_string(4.0) == "4:00"
    assert u.hours_to_string(0.0) == "0:00"
