from core import status
from core.response import Response


def test_response_init() -> None:
    response = Response(
        status_code=status.CREATED, headers={"X-Custom-Header": "test"}, body="Hello, World!"
    )

    assert response.status_code == status.CREATED
    assert response.headers == {"X-Custom-Header": "test"}
    assert response.body == "Hello, World!"


def test_response_build() -> None:
    response = Response(
        status_code=status.CREATED, headers={"X-Custom-Header": "test"}, body="Hello, World!"
    )
    built_response = response.build()

    assert built_response == b"HTTP/1.1 201 Created\r\nX-Custom-Header: test\r\n\r\nHello, World!"


def test_response_body_setter() -> None:
    response = Response()
    response.body = "New Body"
    assert response.body == "New Body"


def test_response_headers_setter() -> None:
    response = Response()
    response.headers = {"New-Header": "test"}

    assert response.headers == {"New-Header": "test"}
