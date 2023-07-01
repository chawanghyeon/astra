from core import Request


def test_request_repr():
    request = Request()
    assert repr(request) == "<Request method=None path= version=None>"
