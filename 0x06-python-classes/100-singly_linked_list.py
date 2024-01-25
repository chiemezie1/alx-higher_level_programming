class Node:
    """Class representing a node in a singly linked list."""
    def __init__(self, data, next_node=None):
        """Initialize a new Node."""
        self.data = data
        self.next_node = next_node

    @property
    def data(self):
        """Retrieve data attribute."""
        return self._data

    @data.setter
    def data(self, value):
        """Set data attribute."""
        if not isinstance(value, int):
            raise TypeError("data must be an integer")
        self._data = value

    @property
    def next_node(self):
        """Retrieve next_node attribute."""
        return self._next_node

    @next_node.setter
    def next_node(self, value):
        """Set next_node attribute."""
        if value is not None and not isinstance(value, Node):
            raise TypeError("next_node must be a Node object")
        self._next_node = value


class SinglyLinkedList:
    """Class representing a singly linked list."""
    def __init__(self):
        """Initialize an empty singly linked list."""
        self.head = None

    def sorted_insert(self, value):
        """Insert a new Node into the correct sorted position."""
        new_node = Node(value)
        if self.head is None or value < self.head.data:
            new_node.next_node = self.head
            self.head = new_node
            return

        current = self.head
        while current.next_node is not None and current.next_node.data < value:
            current = current.next_node

        new_node.next_node = current.next_node
        current.next_node = new_node

    def __str__(self):
        """Return a string representation of the list."""
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next_node
        return '\n'.join(result)
