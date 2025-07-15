class Queue:
    def __init__(self):
        self._container = []

    def enqueue(self, item):
        self._container.insert(0, item)
        print(f"Enqueued {item}")

    def dequeue(self):
        if not self._container:
            raise IndexError("dequeue from empty queue")
        item = self._container.pop()
        print(f"Dequeued {item}")
        return item

    def is_empty(self):
        return len(self._container) == 0

    def __len__(self):
        return len(self._container)