"""Exercise 10: Linked Lists.

A singly linked list built from scratch, followed by a comparison against
collections.deque, the standard library's production-ready alternative.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None


class LinkedList:
    """Minimal singly linked list with head insertion, append, and search."""

    def __init__(self) -> None:
        self._head: Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[int]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"LinkedList({list(self)})"

    def push_front(self, value: int) -> None:
        self._head = Node(value, self._head)
        self._size += 1

    def append(self, value: int) -> None:
        new_node = Node(value)
        if self._head is None:
            self._head = new_node
        else:
            node = self._head
            while node.next is not None:
                node = node.next
            node.next = new_node
        self._size += 1

    def find(self, value: int) -> bool:
        return value in self

    def remove(self, value: int) -> bool:
        prev, node = None, self._head
        while node is not None:
            if node.value == value:
                if prev is None:
                    self._head = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return True
            prev, node = node, node.next
        return False


def main() -> None:
    ll = LinkedList()
    ll.push_front(3)
    ll.push_front(2)
    ll.push_front(1)
    ll.append(4)
    print(f"list: {ll}")
    print(f"len: {len(ll)}")
    print(f"find(3): {ll.find(3)}")
    print(f"find(99): {ll.find(99)}")

    ll.remove(2)
    print(f"after remove(2): {ll}")

    # --- Traversal via the __iter__ we defined ---
    print(f"as a python list: {[v for v in ll]}")

    # --- Real code uses collections.deque: O(1) append/pop from both ends ---
    dq: deque[int] = deque()
    dq.appendleft(3)
    dq.appendleft(2)
    dq.appendleft(1)
    dq.append(4)
    print(f"deque: {dq}")
    dq.remove(2)
    print(f"deque after remove(2): {dq}")

    # A hand-rolled linked list is O(n) to append (without a tail pointer)
    # and O(n) to index. deque is a doubly linked list of blocks under the
    # hood, with O(1) append/pop at both ends — use it in real code.


if __name__ == "__main__":
    main()
