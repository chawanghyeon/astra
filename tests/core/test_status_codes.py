import pytest
from core.status_codes import (
    get_status_reason,
    OK,
    NOT_FOUND,
    INTERNAL_SERVER_ERROR,
)


def test_get_status_reason():
    assert get_status_reason(OK) == "OK"
    assert get_status_reason(NOT_FOUND) == "Not Found"
    assert get_status_reason(INTERNAL_SERVER_ERROR) == "Internal Server Error"
    assert get_status_reason(999) == "Unknown Status"


@pytest.mark.parametrize(
    "status_code,expected_reason",
    [
        (OK, "OK"),
        (NOT_FOUND, "Not Found"),
        (INTERNAL_SERVER_ERROR, "Internal Server Error"),
        (999, "Unknown Status"),
    ],
)
def test_get_status_reason_parametrized(status_code, expected_reason):
    assert get_status_reason(status_code) == expected_reason
