from core.request import Request


def test_request_on_url() -> None:
    request = Request()
    request.on_url(b"/test?query=value")

    assert request.path == "/test"
    assert request.query_string == "query=value"


def test_request_on_header() -> None:
    request = Request()
    request.on_header(b"Content-Type", b"application/json")

    assert request.get_header("Content-Type") == "application/json"


def test_request_on_body() -> None:
    request = Request()
    request.on_body(b"body content")

    assert request.body == "body content"


def test_request_on_message_complete() -> None:
    request = Request()

    request.on_message_complete()

    assert request.method != ""
    assert request.version is not None


def test_request_repr() -> None:
    request = Request()
    assert repr(request) == "<Request method= path= version=None>"
