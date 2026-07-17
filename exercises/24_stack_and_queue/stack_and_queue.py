"""Exercise 24: Stack & Queue.

Both are built on collections.deque, which offers O(1) append/pop at both
ends (unlike list.pop(0), which is O(n)). Includes two classic applications:
balanced-bracket checking and breadth-first search.
"""

from collections import deque


class Stack:
    """LIFO: push and pop from the same end."""

    def __init__(self) -> None:
        self._data: deque[int] = deque()

    def push(self, item: int) -> None:
        self._data.append(item)

    def pop(self) -> int:
        return self._data.pop()

    def peek(self) -> int:
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


class Queue:
    """FIFO: push at one end, pop from the other."""

    def __init__(self) -> None:
        self._data: deque[int] = deque()

    def enqueue(self, item: int) -> None:
        self._data.append(item)

    def dequeue(self) -> int:
        return self._data.popleft()

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


def is_balanced(expression: str) -> bool:
    """Classic stack application: match ( ) [ ] { }."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in expression:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """Classic queue application: breadth-first search over an adjacency list."""
    visited = {start}
    order: list[str] = []
    queue: deque[str] = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def main() -> None:
    s = Stack()
    for v in [1, 2, 3]:
        s.push(v)
    print(f"stack peek: {s.peek()}")
    print(f"stack pop order: {[s.pop() for _ in range(len(s))]}")

    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    print(f"queue dequeue order: {[q.dequeue() for _ in range(len(q))]}")

    for expr in ["(a[b]{c})", "([)]", "((()", "{[()]}"]:
        print(f"is_balanced({expr!r}) = {is_balanced(expr)}")

    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C", "E"],
        "E": ["D"],
    }
    print(f"bfs(graph, 'A') = {bfs(graph, 'A')}")


if __name__ == "__main__":
    main()
