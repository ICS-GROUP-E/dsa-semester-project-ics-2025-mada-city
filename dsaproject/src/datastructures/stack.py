class Stack:
    def __init__(self):
        self._container = []

    def push(self, item):
        self._container.append(item)
        print(f"Pushed {item}")

    def pop(self):
        if not self._container:
            raise IndexError("pop from empty stack")
        item = self._container.pop()
        print(f"Popped {item}")
        return item

    def is_empty(self):
        return len(self._container) == 0

    def peek(self):
        return self._container[-1] if self._container else None

    def __len__(self):
        return len(self._container)