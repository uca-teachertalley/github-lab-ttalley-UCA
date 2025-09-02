"""
MessageBox module
Author: Terry Talley
Implements a fixed-size message box for storing and retrieving messages by index.
"""

DEFAULT_SIZE = 10


class MessageBox:
    """
    A fixed-size message box for storing and retrieving messages by index.
    Supports sending, receiving, and checking the status of message slots.
    """

    def __init__(self, num_entries=DEFAULT_SIZE):
        """
        Initialize the MessageBox with a given number of entries.
        Args:
            num_entries (int): The number of message slots in the box.
        """
        self.my_size = num_entries
        self.count = 0
        self.messages = [None] * self.my_size
        self.empty_box = [True] * self.my_size

    def send(self, index, message):
        """
        Send a message to a specific index in the message box.
        Args:
            index (int): The position to store the message.
            message: The message to store.
        Raises:
            IndexError: If the index is out of bounds.
            RuntimeError: If the position is already full.
        """
        if index < 0 or index >= self.my_size:
            raise IndexError("Index out of bounds")
        if self.full(index):
            raise RuntimeError("Message box position is full")
        self.messages[index] = message
        self.empty_box[index] = False
        self.count += 1

    def receive(self, index):
        """
        Receive (remove and return) a message from a specific index.
        Args:
            index (int): The position to retrieve the message from.
        Returns:
            The message at the given index.
        Raises:
            IndexError: If the index is out of bounds.
            RuntimeError: If the position is empty.
        """
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
        """
        Check if the message box or a specific position is empty.
        Args:
            index (int, optional): The position to check. 
                If None, checks if the box is empty overall.
        Returns:
            bool: True if empty, False otherwise.
        Raises:
            IndexError: If the index is out of bounds.
        """
        if index is None:
            return self.count == 0
        if index < 0 or index >= self.my_size:
            raise IndexError("Index out of bounds")
        return self.empty_box[index]

    def full(self, index=None):
        """
        Check if the message box or a specific position is full.
        Args:
            index (int, optional): The position to check. 
                If None, checks if the box is full overall.
        Returns:
            bool: True if full, False otherwise.
        """
        if index is None:
            return self.count == self.my_size
        return not self.empty(index)

    def get_size(self):
        """
        Get the size (number of slots) of the message box.
        Returns:
            int: The size of the message box.
        """
        return self.my_size

    def get_count(self):
        """
        Get the current number of messages in the message box.
        Returns:
            int: The number of messages currently stored.
        """
        return self.count

    def to_string(self):
        """
        Return a string representation of all non-empty messages in the box.
        Returns:
            str: Space-separated string of messages.
        """
        result = []
        for i in range(self.my_size):
            if not self.empty(i):
                result.append(str(self.messages[i]))
        return " ".join(result)

    def print(self):
        """
        Print a string representation of all non-empty messages in the box.
        """
        print(self.to_string())

    def print_verbose(self):
        """
        Print the contents of each slot in the message box, showing <empty> for empty slots.
        """
        for i in range(self.my_size):
            if self.empty(i):
                result = "<empty>"
            else:
                result = str(self.messages[i])
            print(f"{i}:{result}:")

    def __str__(self):
        """
        Return a string representation of all non-empty messages in the box.
        Returns:
            str: Space-separated string of messages.
        """
        return self.to_string()


def main():
    """
    Demonstrate the usage of the MessageBox class with various operations and error handling.
    """
    # Create a MessageBox instance
    print("Creating a MessageBox with default size...")
    mbox = MessageBox()

    print(f"MessageBox size: {mbox.get_size()}")
    print(f"Current count: {mbox.get_count()}")
    print(f"Is empty (overall): {mbox.empty()}")
    print(f"Is full (overall): {mbox.full()}")
    print()

    # Test sending messages
    print("Sending messages...")
    mbox.send(0, "Hello")
    mbox.send(2, "World")
    mbox.send(5, "Python")

    print(f"Current count after sending: {mbox.get_count()}\n",
          f"Is empty (overall): {mbox.empty()}\n",
          f"Is full (overall): {mbox.full()}")

    # Test individual position checks
    print("Checking individual positions...\n",
          f"Position 0 empty: {mbox.empty(0)}\n",
          f"Position 1 empty: {mbox.empty(1)}\n",
          f"Position 0 full: {mbox.full(0)}\n",
          f"Position 1 full: {mbox.full(1)}")

    # Test printing methods
    print("Testing print methods...")
    print("to_string():", mbox.to_string())
    print("print():")
    mbox.print()

    print("print_verbose():")
    mbox.print_verbose()
    print("__str__():", str(mbox))
    print()

    # Test receiving messages
    print("Receiving messages...")
    msg1 = mbox.receive(0)
    print(f"Received from position 0: {msg1}")
    msg2 = mbox.receive(2)
    print(f"Received from position 2: {msg2}")

    print(f"Current count after receiving: {mbox.get_count()}")
    print("Current state:")
    mbox.print_verbose()
    print()

    # Test error conditions
    print("Testing error conditions...")
    try:
        mbox.send(15, "Out of bounds")  # Should raise IndexError
    except IndexError as expected_exception:
        print(f"Caught expected IndexError: {expected_exception}")

    try:
        mbox.send(5, "Already full")  # Should raise RuntimeError
        mbox.send(5, "This will fail")  # Should raise RuntimeError
    except RuntimeError as expected_exception:
        print(f"Caught expected RuntimeError: {expected_exception}")

    try:
        mbox.receive(1)  # Should raise RuntimeError (empty position)
    except RuntimeError as expected_exception:
        print(f"Caught expected RuntimeError: {expected_exception}")

    try:
        mbox.receive(-1)  # Should raise IndexError
    except IndexError as expected_exception:
        print(f"Caught expected IndexError: {expected_exception}")


if __name__ == "__main__":
    main()
