import pytest

from lms import calculate_fine


@pytest.mark.parametrize("days, expected", [
    pytest.param(0, 0, id="zero-no-fine"),
    pytest.param(4, 20, id="valid-overdue"),
    pytest.param(1, 5, id="boundary-first-overdue-day"),
    pytest.param(365, 1825, id="large-valid-input"),
])
def test_calculate_fine(days, expected):
    assert calculate_fine(days) == expected


@pytest.mark.parametrize("days", [-1, -10], ids=["boundary-below-zero", "negative"])
def test_negative_days(days):
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_fine(days)


@pytest.mark.parametrize("days", [1.5, "3", None, True])
def test_invalid_type(days):
    with pytest.raises(TypeError, match="must be an integer"):
        calculate_fine(days)
