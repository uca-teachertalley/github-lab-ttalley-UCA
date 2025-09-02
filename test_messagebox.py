
"""
Unit tests for the MessageBox class.
"""

import unittest
from MessageBox import MessageBox, DEFAULT_SIZE

# pylint: disable=too-many-public-methods
class TestMessageBox(unittest.TestCase):
    """
    Unit tests for the MessageBox class, covering initialization, sending, receiving,
    and state-checking methods, as well as error conditions.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mbox = MessageBox()
        self.small_mbox = MessageBox(3)

    def test_init_default_size(self):
        """Test MessageBox initialization with default size."""
        mbox = MessageBox()
        self.assertEqual(mbox.get_size(), DEFAULT_SIZE)
        self.assertEqual(mbox.get_count(), 0)
        self.assertTrue(mbox.empty())
        self.assertFalse(mbox.full())

    def test_init_custom_size(self):
        """Test MessageBox initialization with custom size."""
        mbox = MessageBox(5)
        self.assertEqual(mbox.get_size(), 5)
        self.assertEqual(mbox.get_count(), 0)
        self.assertTrue(mbox.empty())
        self.assertFalse(mbox.full())

    def test_send_valid_message(self):
        """Test sending a message to a valid empty position."""
        self.mbox.send(0, "Hello")
        self.assertEqual(self.mbox.get_count(), 1)
        self.assertFalse(self.mbox.empty(0))
        self.assertTrue(self.mbox.full(0))
        self.assertFalse(self.mbox.empty())
        self.assertFalse(self.mbox.full())

    def test_send_multiple_messages(self):
        """Test sending multiple messages to different positions."""
        self.mbox.send(0, "Hello")
        self.mbox.send(5, "World")
        self.mbox.send(9, "Python")

        self.assertEqual(self.mbox.get_count(), 3)
        self.assertFalse(self.mbox.empty())
        self.assertFalse(self.mbox.full())

        # Check individual positions
        self.assertTrue(self.mbox.full(0))
        self.assertTrue(self.mbox.empty(1))
        self.assertTrue(self.mbox.full(5))
        self.assertTrue(self.mbox.full(9))

    def test_send_index_out_of_bounds(self):
        """Test sending to invalid indices raises IndexError."""
        with self.assertRaises(IndexError):
            self.mbox.send(-1, "Invalid")

        with self.assertRaises(IndexError):
            self.mbox.send(DEFAULT_SIZE, "Invalid")

        with self.assertRaises(IndexError):
            self.mbox.send(100, "Invalid")

    def test_send_to_full_position(self):
        """Test sending to an already full position raises RuntimeError."""
        self.mbox.send(0, "First message")

        with self.assertRaises(RuntimeError):
            self.mbox.send(0, "Second message")

    def test_receive_valid_message(self):
        """Test receiving a message from a valid position."""
        self.mbox.send(0, "Test message")
        message = self.mbox.receive(0)

        self.assertEqual(message, "Test message")
        self.assertEqual(self.mbox.get_count(), 0)
        self.assertTrue(self.mbox.empty(0))
        self.assertTrue(self.mbox.empty())

    def test_receive_multiple_messages(self):
        """Test receiving multiple messages."""
        self.mbox.send(0, "Hello")
        self.mbox.send(5, "World")

        msg1 = self.mbox.receive(0)
        msg2 = self.mbox.receive(5)

        self.assertEqual(msg1, "Hello")
        self.assertEqual(msg2, "World")
        self.assertEqual(self.mbox.get_count(), 0)
        self.assertTrue(self.mbox.empty())

    def test_receive_index_out_of_bounds(self):
        """Test receiving from invalid indices raises IndexError."""
        with self.assertRaises(IndexError):
            self.mbox.receive(-1)

        with self.assertRaises(IndexError):
            self.mbox.receive(DEFAULT_SIZE)

    def test_receive_from_empty_position(self):
        """Test receiving from an empty position raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            self.mbox.receive(0)

        # Send and receive, then try to receive again
        self.mbox.send(0, "Test")
        self.mbox.receive(0)

        with self.assertRaises(RuntimeError):
            self.mbox.receive(0)

    def test_empty_overall(self):
        """Test empty() method for overall MessageBox state."""
        self.assertTrue(self.mbox.empty())

        self.mbox.send(0, "Test")
        self.assertFalse(self.mbox.empty())

        self.mbox.receive(0)
        self.assertTrue(self.mbox.empty())

    def test_empty_specific_position(self):
        """Test empty() method for specific positions."""
        self.assertTrue(self.mbox.empty(0))
        self.assertTrue(self.mbox.empty(5))

        self.mbox.send(0, "Test")
        self.assertFalse(self.mbox.empty(0))
        self.assertTrue(self.mbox.empty(5))

    def test_empty_index_out_of_bounds(self):
        """Test empty() with invalid index raises IndexError."""
        with self.assertRaises(IndexError):
            self.mbox.empty(-1)

        with self.assertRaises(IndexError):
            self.mbox.empty(DEFAULT_SIZE)

    def test_full_overall(self):
        """Test full() method for overall MessageBox state."""
        self.assertFalse(self.mbox.full())

        # Fill all positions
        for i in range(DEFAULT_SIZE):
            self.mbox.send(i, f"Message {i}")

        self.assertTrue(self.mbox.full())

    def test_full_specific_position(self):
        """Test full() method for specific positions."""
        self.assertFalse(self.mbox.full(0))

        self.mbox.send(0, "Test")
        self.assertTrue(self.mbox.full(0))
        self.assertFalse(self.mbox.full(1))

    def test_get_size(self):
        """Test get_size() method."""
        self.assertEqual(self.mbox.get_size(), DEFAULT_SIZE)
        self.assertEqual(self.small_mbox.get_size(), 3)

    def test_get_count(self):
        """Test get_count() method."""
        self.assertEqual(self.mbox.get_count(), 0)

        self.mbox.send(0, "Test1")
        self.assertEqual(self.mbox.get_count(), 1)

        self.mbox.send(5, "Test2")
        self.assertEqual(self.mbox.get_count(), 2)

        self.mbox.receive(0)
        self.assertEqual(self.mbox.get_count(), 1)

        self.mbox.receive(5)
        self.assertEqual(self.mbox.get_count(), 0)

    def test_to_string_empty(self):
        """Test to_string() method with empty MessageBox."""
        self.assertEqual(self.mbox.to_string(), "")

    def test_to_string_with_messages(self):
        """Test to_string() method with messages."""
        self.mbox.send(0, "Hello")
        self.mbox.send(2, "World")
        self.mbox.send(1, "Test")

        result = self.mbox.to_string()
        # Messages should appear in order they were stored, not sent
        self.assertEqual(result, "Hello Test World")

    def test_str_method(self):
        """Test __str__ method."""
        self.mbox.send(0, "Hello")
        self.mbox.send(2, "World")

        self.assertEqual(str(self.mbox), "Hello World")
        self.assertEqual(str(self.mbox), self.mbox.to_string())

    def test_message_types(self):
        """Test sending different types of messages."""
        self.mbox.send(0, "String message")
        self.mbox.send(1, 42)
        self.mbox.send(2, [1, 2, 3])
        self.mbox.send(3, {"key": "value"})

        self.assertEqual(self.mbox.receive(0), "String message")
        self.assertEqual(self.mbox.receive(1), 42)
        self.assertEqual(self.mbox.receive(2), [1, 2, 3])
        self.assertEqual(self.mbox.receive(3), {"key": "value"})

    def test_fill_and_empty_cycle(self):
        """Test filling the MessageBox completely and then emptying it."""
        # Fill all positions
        for i in range(self.small_mbox.get_size()):
            self.small_mbox.send(i, f"Message {i}")

        self.assertTrue(self.small_mbox.full())
        self.assertEqual(self.small_mbox.get_count(), 3)

        # Try to add one more (should fail)
        with self.assertRaises(RuntimeError):
            self.small_mbox.send(0, "This should fail")

        # Empty all positions
        messages = []
        for i in range(self.small_mbox.get_size()):
            messages.append(self.small_mbox.receive(i))

        self.assertTrue(self.small_mbox.empty())
        self.assertEqual(self.small_mbox.get_count(), 0)
        self.assertEqual(messages, ["Message 0", "Message 1", "Message 2"])

    def test_print_methods(self):
        """Test that print methods don't raise exceptions."""
        # Test with empty MessageBox
        try:
            self.mbox.print()
            self.mbox.print_verbose()
        except Exception as unexpected: # pylint: disable=broad-except
            self.fail(f"Print methods raised an exception with empty MessageBox: {unexpected}")

        # Test with messages
        self.mbox.send(0, "Hello")
        self.mbox.send(2, "World")

        try:
            self.mbox.print()
            self.mbox.print_verbose()
        except Exception as unexpected: # pylint: disable=broad-except
            self.fail(f"Print methods raised an exception with messages: {unexpected}")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
