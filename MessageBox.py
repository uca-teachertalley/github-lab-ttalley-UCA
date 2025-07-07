DEFAULT_SIZE = 10


class MessageBox:
    def __init__(self, num_entries=DEFAULT_SIZE):
        self.my_size = num_entries
        self.count = 0
        self.messages = [None] * self.my_size
        self.empty_box = [True] * self.my_size

    def send(self, index, message):
        if index < 0 or index >= self.my_size:
            raise IndexError("Index out of bounds")
        if self.full(index):
            raise RuntimeError("Message box position is full")
        self.messages[index] = message
        self.empty_box[index] = False
        self.count += 1

    def receive(self, index):
        if index < 0 or index >= self.my_size:
            raise IndexError("Index out of bounds")
        if self.empty(index):
            raise RuntimeError("Message box position is empty")
        message = self.messages[index]
        self.messages[index] = None
        self.empty_box[index] = True
        self.count -= 1
        return message

    def empty(self, index=None):
        if index is None:
            return self.count == 0
        if index < 0 or index >= self.my_size:
            raise IndexError("Index out of bounds")
        return self.empty_box[index]

    def full(self, index=None):
        if index is None:
            return self.count == self.my_size
        return not self.empty(index)

    def get_size(self):
        return self.my_size

    def get_count(self):
        return self.count

    def to_string(self):
        result = []
        for i in range(self.my_size):
            if not self.empty(i):
                result.append(str(self.messages[i]))
        return " ".join(result)

    def print(self):
        print(self.to_string())

    def print_verbose(self):
        for i in range(self.my_size):
            if self.empty(i):
                result = "<empty>"
            else:
                result = str(self.messages[i])
            print(f"{i}:{result}:")

    def __str__(self):
        return self.to_string()


def main():
    # Create a MessageBox instance
    print("Creating a MessageBox with default size...")
    mb = MessageBox()

    print(f"MessageBox size: {mb.get_size()}")
    print(f"Current count: {mb.get_count()}")
    print(f"Is empty (overall): {mb.empty()}")
    print(f"Is full (overall): {mb.full()}")
    print()

    # Test sending messages
    print("Sending messages...")
    mb.send(0, "Hello")
    mb.send(2, "World")
    mb.send(5, "Python")

    print(f"Current count after sending: {mb.get_count()}")
    print(f"Is empty (overall): {mb.empty()}")
    print(f"Is full (overall): {mb.full()}")
    print()

    # Test individual position checks
    print("Checking individual positions...")
    print(f"Position 0 empty: {mb.empty(0)}")
    print(f"Position 1 empty: {mb.empty(1)}")
    print(f"Position 0 full: {mb.full(0)}")
    print(f"Position 1 full: {mb.full(1)}")
    print()

    # Test printing methods
    print("Testing print methods...")
    print("to_string():", mb.to_string())
    print("print():")
    mb.print()
    print("print_verbose():")
    mb.print_verbose()
    print("__str__():", str(mb))
    print()

    # Test receiving messages
    print("Receiving messages...")
    msg1 = mb.receive(0)
    print(f"Received from position 0: {msg1}")
    msg2 = mb.receive(2)
    print(f"Received from position 2: {msg2}")

    print(f"Current count after receiving: {mb.get_count()}")
    print("Current state:")
    mb.print_verbose()
    print()

    # Test error conditions
    print("Testing error conditions...")
    try:
        mb.send(15, "Out of bounds")  # Should raise IndexError
    except IndexError as e:
        print(f"Caught expected IndexError: {e}")

    try:
        mb.send(5, "Already full")  # Should raise RuntimeError
        mb.send(5, "This will fail")  # Should raise RuntimeError
    except RuntimeError as e:
        print(f"Caught expected RuntimeError: {e}")

    try:
        mb.receive(1)  # Should raise RuntimeError (empty position)
    except RuntimeError as e:
        print(f"Caught expected RuntimeError: {e}")

    try:
        mb.receive(-1)  # Should raise IndexError
    except IndexError as e:
        print(f"Caught expected IndexError: {e}")


if __name__ == "__main__":
    main()
