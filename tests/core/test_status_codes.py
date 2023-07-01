import pytest

from core import Status


def test_get_status_reason():
    assert Status.get_status_reason(Status.OK) == "OK"
    assert Status.get_status_reason(Status.NOT_FOUND) == "Not Found"
    assert Status.get_status_reason(Status.INTERNAL_SERVER_ERROR) == "Internal Server Error"
    assert Status.get_status_reason(999) == "Unknown Status"


@pytest.mark.parametrize(
    "status_code,expected_reason",
    [
        (Status.OK, "OK"),
        (Status.NOT_FOUND, "Not Found"),
        (Status.INTERNAL_SERVER_ERROR, "Internal Server Error"),
        (999, "Unknown Status"),
    ],
)
def test_get_status_reason_parametrized(status_code, expected_reason):
    assert Status.get_status_reason(status_code) == expected_reason
