from __future__ import annotations
from typing import Any, List, Optional

class Array:
    """
    A thin wrapper over a Python list to expose explicit capacity control and
    O(n) insert/delete semantics.
    """

    def __init__(self, capacity: int):
        self._data: List[Optional[Any]] = [None] * capacity
        self._size = 0

    def _check_bounds(self, index: int):
        if not 0 <= index < self._size:
            raise IndexError("index out of range")

    def _make_room(self, index: int):
        """Shift elements right to open a hole at index (O(n))."""
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

    def _close_gap(self, index: int):
        """Shift elements left to erase position index (O(n))."""
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None

    def insert(self, index: int, value: Any):
        if self._size == len(self._data):
            raise OverflowError("array is full")
        if not 0 <= index <= self._size:
            raise IndexError("index out of range")
        self._make_room(index)
        self._data[index] = value
        self._size += 1

    def delete(self, index: int):
        self._check_bounds(index)
        self._close_gap(index)
        self._size -= 1

    def access(self, index: int) -> Any:
        self._check_bounds(index)
        return self._data[index]

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Array({[self._data[i] for i in range(self._size)]})"

class Matrix:
    """
    Simple row‑major matrix. Each row is an Array instance to keep the theme.
    """
    def __init__(self, rows: int, cols: int):
        self._rows = [Array(cols) for _ in range(rows)]
        # pre‑fill matrix with zeros
        for r in self._rows:
            for c in range(cols):
                r.insert(c, 0)

    def set(self, r: int, c: int, val: Any):
        self._rows[r]._data[c] = val

    def get(self, r: int, c: int) -> Any:
        return self._rows[r]._data[c]

    def __repr__(self):
        return "\n".join(repr(row) for row in self._rows)


class Stack:
    """
    Classic LIFO stack with push/pop O(1). We reuse Python list because its
    append/pop are amortized O(1) and contiguous; perfect for stack behavior.
    """
    def __init__(self):
        self._s: List[Any] = []

    def push(self, val: Any):
        self._s.append(val)

    def pop(self) -> Any:
        if not self._s:
            raise IndexError("pop from empty stack")
        return self._s.pop()

    def peek(self) -> Any:
        return self._s[-1]

    def __len__(self):
        return len(self._s)

    def __repr__(self):
        return f"Stack(top→{list(reversed(self._s))})"

class Queue:
    """
    Fixed‑capacity circular queue: head for dequeue, tail for enqueue.
    Enqueue/Dequeue are O(1) with simple pointer arithmetic.
    """
    def __init__(self, capacity: int):
        self._buf: List[Optional[Any]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def enqueue(self, val: Any):
        if self._size == len(self._buf):
            raise OverflowError("queue full")
        self._buf[self._tail] = val
        self._tail = (self._tail + 1) % len(self._buf)
        self._size += 1

    def dequeue(self) -> Any:
        if not self._size:
            raise IndexError("dequeue from empty queue")
        val = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % len(self._buf)
        self._size -= 1
        return val

    def __len__(self):
        return self._size

    def __repr__(self):
        # show logical order without copying whole buffer
        items = [self._buf[(self._head + i) % len(self._buf)] for i in range(self._size)]
        return f"Queue({items})"


class Node:
    """Internal list node – value + pointer."""
    def __init__(self, value: Any, nxt: Node | None = None):
        self.value, self.next = value, nxt


class LinkedList:
    """
    Pointer‑based list: insert/delete at head are O(1); arbitrary positions O(n).
    Demonstrates non‑contiguous allocation: great for inserts, cache‑unfriendly
    for indexed access.
    """
    def __init__(self):
        self.head: Node | None = None

    def insert(self, pos: int, value: Any):
        if pos == 0:
            self.head = Node(value, self.head)
            return
        prev = self._node_at(pos - 1)
        prev.next = Node(value, prev.next)

    # delete node at position
    def delete(self, pos: int):
        if pos == 0:
            if not self.head:
                raise IndexError("delete from empty list")
            self.head = self.head.next
            return
        prev = self._node_at(pos - 1)
        if not prev.next:
            raise IndexError("position out of range")
        prev.next = prev.next.next

    # traverse generator
    def traverse(self):
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    # node at index
    def _node_at(self, pos: int) -> Node:
        cur, i = self.head, 0
        while cur and i < pos:
            cur, i = cur.next, i + 1
        if cur is None:
            raise IndexError("position out of range")
        return cur

    def __repr__(self):
        return f"LinkedList([{', '.join(map(str, self.traverse()))}])"


class TreeNode:
    def __init__(self, value: Any):
        self.value = value
        self.children: List[TreeNode] = []

    def add_child(self, node: "TreeNode"):
        self.children.append(node)

    def dfs(self):
        """Depth‑first generator (pre‑order)."""
        yield self.value
        for child in self.children:
            yield from child.dfs()

    def __repr__(self):
        return f"TreeNode({self.value})"


if __name__ == "__main__":
    print("Array:")
    arr = Array(5)
    for i in range(3):
        arr.insert(i, i * 10)
    print(arr)
    arr.delete(1)
    print("after delete:", arr, "\n")

    print("Stack:")
    s = Stack()
    for c in "abcd":
        s.push(c)
    print(s)
    print("pop->", s.pop(), "peek->", s.peek(), "\n")

    print("Queue")
    q = Queue(4)
    for i in range(3):
        q.enqueue(i)
    print(q)
    print("dequeue->", q.dequeue(), q)
    q.enqueue(99)
    print("after enqueue 99:", q, "\n")

    print("LinkedList:")
    ll = LinkedList()
    for i in range(5):
        ll.insert(i, i)
    print(ll)
    ll.delete(2)
    print("after delete pos2:", ll, "\n")

    print("Tree demo (DFS):")
    root = TreeNode("root")
    child_a = TreeNode("A"); child_b = TreeNode("B")
    root.add_child(child_a); root.add_child(child_b)
    child_a.add_child(TreeNode("A1"))
    child_b.add_child(TreeNode("B1")); child_b.add_child(TreeNode("B2"))
    print("DFS traversal:", list(root.dfs()))