import pytest

from core import status


def test_get_status_reason() -> None:
    assert status.get_status_reason(status.OK) == "OK"
    assert status.get_status_reason(status.NOT_FOUND) == "Not Found"
    assert status.get_status_reason(status.INTERNAL_SERVER_ERROR) == "Internal Server Error"
    assert status.get_status_reason(999) == "Unknown Status"


@pytest.mark.parametrize(
    "status_code,expected_reason",
    [
        (status.OK, "OK"),
        (status.NOT_FOUND, "Not Found"),
        (status.INTERNAL_SERVER_ERROR, "Internal Server Error"),
        (999, "Unknown Status"),
    ],
)
def test_get_status_reason_parametrized(status_code: int, expected_reason: str) -> None:
    assert status.get_status_reason(status_code) == expected_reason
