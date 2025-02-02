from uuid import uuid4

class Todo:
    def __init__(self, text: str):
        self.id = uuid4()
        self.text = text
        self.done = False


