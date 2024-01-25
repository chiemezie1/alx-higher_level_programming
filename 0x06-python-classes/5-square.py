#!/usr/bin/python3

class Node:
    """Node class for singly linked list"""

    def __init__(self, data, next_node=None):
        """Initialize a new Node"""
        self.data = data
        self.next_node = next_node

    @property
    def data(self):
        """Retrieve the data value of the node"""
        return self.__data

    @data.setter
    def data(self, value):
        """Set the data value of the node"""
        if not isinstance(value, int):
            raise TypeError("data must be an integer")
        self.__data = value

    @property
    def next_node(self):
        """Retrieve the next_node value of the node"""
        return self.__next_node

    @next_node.setter
    def next_node(self, value):
        """Set the next_node value of the node"""
        if value is not None and not isinstance(value, Node):
            raise TypeError("next_node must be a Node object")
        self.__next_node = value


class SinglyLinkedList:
    """SinglyLinkedList class"""

    def __init__(self):
        """Initialize an empty SinglyLinkedList"""
        self.head = None

    def sorted_insert(self, value):
        """Insert a new Node into the correct sorted position in the list"""
        new_node = Node(value)
        if self.head is None or self.head.data >= value:
            new_node.next_node = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next_node is not None and current.next_node.data < value:
                current = current.next_node
            new_node.next_node = current.next_node
            current.next_node = new_node

    def __str__(self):
        """Print the entire list in stdout"""
        result = []
        current = self.head
        while current is not None:
            result.append(str(current.data))
            current = current.next_node
        return "\n".join(result)
