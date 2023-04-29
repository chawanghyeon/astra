class Request:
    def __init__(self):
        self._method = None
        self._version = None
        self._path = None
        self._headers = None
        self._body = None

    @property
    def method(self):
        return self._method.decode()

    def __repr__(self):
        return f"<Request method={self.method} path={self.path} version={self.version} headers={self.headers}>"
