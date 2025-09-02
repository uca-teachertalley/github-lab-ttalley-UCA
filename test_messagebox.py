
"""
Unit tests for the MessageBox class.
"""

import unittest
from message_box import MessageBox, DEFAULT_SIZE



class TestMessageBox(unittest.TestCase):
    """
    Unit tests for the MessageBox class, covering initialization, sending, receiving,
    and state-checking methods, as well as error conditions.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mb = MessageBox()
        self.small_mb = MessageBox(3)

    def test_init_default_size(self):
        """Test MessageBox initialization with default size."""
        mb = MessageBox()
        self.assertEqual(mb.get_size(), DEFAULT_SIZE)
        self.assertEqual(mb.get_count(), 0)
        self.assertTrue(mb.empty())
        self.assertFalse(mb.full())

    def test_init_custom_size(self):
        """Test MessageBox initialization with custom size."""
        mb = MessageBox(5)
        self.assertEqual(mb.get_size(), 5)
        self.assertEqual(mb.get_count(), 0)
        self.assertTrue(mb.empty())
        self.assertFalse(mb.full())

    def test_send_valid_message(self):
        """Test sending a message to a valid empty position."""
        self.mb.send(0, "Hello")
        self.assertEqual(self.mb.get_count(), 1)
        self.assertFalse(self.mb.empty(0))
        self.assertTrue(self.mb.full(0))
        self.assertFalse(self.mb.empty())
        self.assertFalse(self.mb.full())

    def test_send_multiple_messages(self):
        """Test sending multiple messages to different positions."""
        self.mb.send(0, "Hello")
        self.mb.send(5, "World")
        self.mb.send(9, "Python")

        self.assertEqual(self.mb.get_count(), 3)
        self.assertFalse(self.mb.empty())
        self.assertFalse(self.mb.full())

        # Check individual positions
        self.assertTrue(self.mb.full(0))
        self.assertTrue(self.mb.empty(1))
        self.assertTrue(self.mb.full(5))
        self.assertTrue(self.mb.full(9))

    def test_send_index_out_of_bounds(self):
        """Test sending to invalid indices raises IndexError."""
        with self.assertRaises(IndexError):
            self.mb.send(-1, "Invalid")

        with self.assertRaises(IndexError):
            self.mb.send(DEFAULT_SIZE, "Invalid")

        with self.assertRaises(IndexError):
            self.mb.send(100, "Invalid")

    def test_send_to_full_position(self):
        """Test sending to an already full position raises RuntimeError."""
        self.mb.send(0, "First message")

        with self.assertRaises(RuntimeError):
            self.mb.send(0, "Second message")

    def test_receive_valid_message(self):
        """Test receiving a message from a valid position."""
        self.mb.send(0, "Test message")
        message = self.mb.receive(0)

        self.assertEqual(message, "Test message")
        self.assertEqual(self.mb.get_count(), 0)
        self.assertTrue(self.mb.empty(0))
        self.assertTrue(self.mb.empty())

    def test_receive_multiple_messages(self):
        """Test receiving multiple messages."""
        self.mb.send(0, "Hello")
        self.mb.send(5, "World")

        msg1 = self.mb.receive(0)
        msg2 = self.mb.receive(5)

        self.assertEqual(msg1, "Hello")
        self.assertEqual(msg2, "World")
        self.assertEqual(self.mb.get_count(), 0)
        self.assertTrue(self.mb.empty())

    def test_receive_index_out_of_bounds(self):
        """Test receiving from invalid indices raises IndexError."""
        with self.assertRaises(IndexError):
            self.mb.receive(-1)

        with self.assertRaises(IndexError):
            self.mb.receive(DEFAULT_SIZE)

    def test_receive_from_empty_position(self):
        """Test receiving from an empty position raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            self.mb.receive(0)

        # Send and receive, then try to receive again
        self.mb.send(0, "Test")
        self.mb.receive(0)

        with self.assertRaises(RuntimeError):
            self.mb.receive(0)

    def test_empty_overall(self):
        """Test empty() method for overall MessageBox state."""
        self.assertTrue(self.mb.empty())

        self.mb.send(0, "Test")
        self.assertFalse(self.mb.empty())

        self.mb.receive(0)
        self.assertTrue(self.mb.empty())

    def test_empty_specific_position(self):
        """Test empty() method for specific positions."""
        self.assertTrue(self.mb.empty(0))
        self.assertTrue(self.mb.empty(5))

        self.mb.send(0, "Test")
        self.assertFalse(self.mb.empty(0))
        self.assertTrue(self.mb.empty(5))

    def test_empty_index_out_of_bounds(self):
        """Test empty() with invalid index raises IndexError."""
        with self.assertRaises(IndexError):
            self.mb.empty(-1)

        with self.assertRaises(IndexError):
            self.mb.empty(DEFAULT_SIZE)

    def test_full_overall(self):
        """Test full() method for overall MessageBox state."""
        self.assertFalse(self.mb.full())

        # Fill all positions
        for i in range(DEFAULT_SIZE):
            self.mb.send(i, f"Message {i}")

        self.assertTrue(self.mb.full())

    def test_full_specific_position(self):
        """Test full() method for specific positions."""
        self.assertFalse(self.mb.full(0))

        self.mb.send(0, "Test")
        self.assertTrue(self.mb.full(0))
        self.assertFalse(self.mb.full(1))

    def test_get_size(self):
        """Test get_size() method."""
        self.assertEqual(self.mb.get_size(), DEFAULT_SIZE)
        self.assertEqual(self.small_mb.get_size(), 3)

    def test_get_count(self):
        """Test get_count() method."""
        self.assertEqual(self.mb.get_count(), 0)

        self.mb.send(0, "Test1")
        self.assertEqual(self.mb.get_count(), 1)

        self.mb.send(5, "Test2")
        self.assertEqual(self.mb.get_count(), 2)

        self.mb.receive(0)
        self.assertEqual(self.mb.get_count(), 1)

        self.mb.receive(5)
        self.assertEqual(self.mb.get_count(), 0)

    def test_to_string_empty(self):
        """Test to_string() method with empty MessageBox."""
        self.assertEqual(self.mb.to_string(), "")

    def test_to_string_with_messages(self):
        """Test to_string() method with messages."""
        self.mb.send(0, "Hello")
        self.mb.send(2, "World")
        self.mb.send(1, "Test")

        result = self.mb.to_string()
        # Messages should appear in order they were stored, not sent
        self.assertEqual(result, "Hello Test World")

    def test_str_method(self):
        """Test __str__ method."""
        self.mb.send(0, "Hello")
        self.mb.send(2, "World")

        self.assertEqual(str(self.mb), "Hello World")
        self.assertEqual(str(self.mb), self.mb.to_string())

    def test_message_types(self):
        """Test sending different types of messages."""
        self.mb.send(0, "String message")
        self.mb.send(1, 42)
        self.mb.send(2, [1, 2, 3])
        self.mb.send(3, {"key": "value"})

        self.assertEqual(self.mb.receive(0), "String message")
        self.assertEqual(self.mb.receive(1), 42)
        self.assertEqual(self.mb.receive(2), [1, 2, 3])
        self.assertEqual(self.mb.receive(3), {"key": "value"})

    def test_fill_and_empty_cycle(self):
        """Test filling the MessageBox completely and then emptying it."""
        # Fill all positions
        for i in range(self.small_mb.get_size()):
            self.small_mb.send(i, f"Message {i}")

        self.assertTrue(self.small_mb.full())
        self.assertEqual(self.small_mb.get_count(), 3)

        # Try to add one more (should fail)
        with self.assertRaises(RuntimeError):
            self.small_mb.send(0, "This should fail")

        # Empty all positions
        messages = []
        for i in range(self.small_mb.get_size()):
            messages.append(self.small_mb.receive(i))

        self.assertTrue(self.small_mb.empty())
        self.assertEqual(self.small_mb.get_count(), 0)
        self.assertEqual(messages, ["Message 0", "Message 1", "Message 2"])

    def test_print_methods(self):
        """Test that print methods don't raise exceptions."""
        # Test with empty MessageBox
        try:
            self.mb.print()
            self.mb.print_verbose()
        except Exception as e:
            self.fail(f"Print methods raised an exception with empty MessageBox: {e}")

        # Test with messages
        self.mb.send(0, "Hello")
        self.mb.send(2, "World")

        try:
            self.mb.print()
            self.mb.print_verbose()
        except Exception as e:
            self.fail(f"Print methods raised an exception with messages: {e}")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
