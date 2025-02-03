from uuid import uuid4

class Url:
    def __init__(self, url: str):
        self.id = uuid4()
        self.url = url


