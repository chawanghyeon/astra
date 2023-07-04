from core import status
from core.response import Response


def test_response_init():
    response = Response(
        status_code=status.CREATED, headers={"X-Custom-Header": "test"}, body="Hello, World!"
    )

    assert response.status_code == status.CREATED
    assert response.headers == {
        "content-type": "text/plain; charset=utf-8",
        "server": "Astra/1.0",
        "x-custom-header": "test",
    }
    assert response.body == b"Hello, World!"


def test_response_build():
    response = Response(
        status_code=status.CREATED, headers={"X-Custom-Header": "test"}, body="Hello, World!"
    )
    built_response = response.build()

    assert (
        built_response
        == b"HTTP/1.1 201 Created\r\ncontent-type: text/plain; charset=utf-8\r\nserver:\
              Astra/1.0\r\nx-custom-header: test\r\n\r\nHello, World!"
    )


def test_response_body_setter():
    response = Response()
    response.body = "New Body"
    assert response.body == b"New Body"


def test_response_headers_setter():
    response = Response()
    response.headers = {"New-Header": "test"}

    assert response.headers == {
        "content-type": "text/plain; charset=utf-8",
        "server": "Astra/1.0",
        "new-header": "test",
    }
