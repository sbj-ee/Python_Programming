"""Exercise 23: Binary Search Tree.

Insert, search, delete (all three cases: leaf, one child, two children),
and the three standard traversals.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: TreeNode | None, value: int) -> TreeNode:
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        # equal values are ignored (no duplicates)
        return node

    def search(self, value: int) -> bool:
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def delete(self, value: int) -> None:
        self.root = self._delete(self.root, value)

    def _delete(self, node: TreeNode | None, value: int) -> TreeNode | None:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Case 1: leaf, or Case 2: one child -- return the surviving side
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children -- replace value with the in-order
            # successor (smallest value in the right subtree), then delete
            # that successor from the right subtree.
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def height(self) -> int:
        def _height(node: TreeNode | None) -> int:
            if node is None:
                return -1
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def inorder(self) -> Iterator[int]:
        yield from self._inorder(self.root)

    def _inorder(self, node: TreeNode | None) -> Iterator[int]:
        if node is not None:
            yield from self._inorder(node.left)
            yield node.value
            yield from self._inorder(node.right)

    def preorder(self) -> Iterator[int]:
        yield from self._preorder(self.root)

    def _preorder(self, node: TreeNode | None) -> Iterator[int]:
        if node is not None:
            yield node.value
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)

    def postorder(self) -> Iterator[int]:
        yield from self._postorder(self.root)

    def _postorder(self, node: TreeNode | None) -> Iterator[int]:
        if node is not None:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.value


def main() -> None:
    bst = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80, 10]:
        bst.insert(v)

    print(f"inorder (sorted): {list(bst.inorder())}")
    print(f"preorder: {list(bst.preorder())}")
    print(f"postorder: {list(bst.postorder())}")
    print(f"height: {bst.height()}")

    print(f"search(40): {bst.search(40)}")
    print(f"search(99): {bst.search(99)}")

    # Case 1: delete a leaf
    bst.delete(10)
    print(f"after deleting leaf 10: {list(bst.inorder())}")

    # Case 2: delete a node with one child
    bst.delete(20)
    print(f"after deleting 20 (one child): {list(bst.inorder())}")

    # Case 3: delete a node with two children
    bst.delete(50)
    print(f"after deleting root 50 (two children): {list(bst.inorder())}")


if __name__ == "__main__":
    main()
