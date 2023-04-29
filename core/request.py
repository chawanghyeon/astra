class Request:
    def __init__(self):
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = b""

    def on_url(self, url):
        self.path = url

    def on_header(self, name, value):
        self.headers[name.decode()] = value.decode()

    def on_body(self, body):
        self.body += body

    def on_message_complete(self):
        pass  # Here you can add any post-processing needed after the message is complete

    def __repr__(self):
        return f"<Request method={self.method} path={self.path} version={self.version} headers={self.headers}>"
