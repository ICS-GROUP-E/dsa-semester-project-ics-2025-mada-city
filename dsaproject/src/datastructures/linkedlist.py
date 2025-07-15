class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        print(f"Inserted {value} at head")

    def search(self, target):
        current = self.head
        while current:
            if current.value == target:
                print(f"Found {target}")
                return current
            current = current.next
        print(f"{target} not found")
        return None

    def delete(self, target):
        prev = None
        current = self.head
        while current:
            if current.value == target:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                print(f"Deleted {target}")
                return True
            prev = current
            current = current.next
        print(f"{target} not found for deletion")
        return False