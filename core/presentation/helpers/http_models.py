from typing import Any


class HttpRequest:
    """Http Request representation"""

    def __init__(
        self, header: dict = None, body: dict = None, query: dict = None
    ) -> None:
        self.header = header
        self.body = body
        self.query = query

    def __repr__(self) -> str:
        return f'HttpRequest(header={self.header}, body={self.body}, query={self.query})'


class HttpResponse:
    """Http Response representation"""

    def __init__(self, status_code: int, body: Any) -> None:
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return (
            f'HttpResponse(status_code={self.status_code}, body={self.body})'
        )
