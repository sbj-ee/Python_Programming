# Collections

`list`, `tuple`, `dict`, and `set` are the four built-in containers, plus
the `collections` module's specialized variants for common patterns.

## list vs tuple

```python
lst = [1, 2, 3]     # mutable, use for homogeneous sequences that change
tup = (1, 2, 3)      # immutable, use for fixed records or dict/set keys

point = (3, 4)       # a tuple often represents a fixed-shape record
x, y = point          # unpacking works on any iterable, not just tuples

single = (1,)         # the comma matters -- (1) is just the int 1
```

## Slicing: `[start:stop:step]`

Works identically on `list`, `tuple`, and `str`.

```python
seq = [0, 1, 2, 3, 4, 5]
seq[2:4]     # [2, 3]      -- stop is exclusive
seq[:3]      # [0, 1, 2]
seq[-2:]     # [4, 5]      -- negative indices count from the end
seq[::2]     # [0, 2, 4]   -- every other element
seq[::-1]    # [5, 4, 3, 2, 1, 0]  -- reversed

seq[10:20]   # []  -- out-of-range slices don't raise, they return empty
```

## Comprehensions

```python
squares = [x * x for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]

lookup = {x: x * x for x in range(5)}          # dict comprehension
unique = {len(w) for w in ["a", "bb", "cc"]}     # set comprehension

# Generator expression: like a list comprehension, but lazy (no ()).
lazy_squares = (x * x for x in range(10**6))    # nothing computed yet
```

## dict: the workhorse container

```python
d = {"a": 1, "b": 2}
d["c"] = 3                  # insert or overwrite
d.get("z", "default")       # no KeyError on a missing key
d.setdefault("a", 99)       # only sets if the key is absent -- returns d["a"]

d.keys(), d.values(), d.items()   # live views, not copies

merged = {"a": 1} | {"a": 2, "b": 3}   # 3.9+: right side wins on conflict
```

## collections.defaultdict, Counter, deque, namedtuple

```python
from collections import Counter, defaultdict, deque, namedtuple

groups = defaultdict(list)      # missing keys get a fresh [] automatically
groups["fruit"].append("apple")  # no KeyError, no manual initialization

freq = Counter("mississippi")
freq.most_common(2)             # [('i', 4), ('s', 4)]

dq = deque([1, 2, 3])
dq.appendleft(0)                # O(1) at both ends, unlike list.insert(0, x)
dq.append(4)

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p[0]                       # both work -- named AND positional access
```

## Set algebra

```python
a, b = {1, 2, 3}, {2, 3, 4}
a | b   # union: {1, 2, 3, 4}
a & b   # intersection: {2, 3}
a - b   # difference: {1}
a ^ b   # symmetric difference: {1, 4}

a.issubset(b), a.issuperset(b), a.isdisjoint(b)
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `list.pop(0)` in a hot loop | O(n) per call -- O(n²) overall | Use `collections.deque.popleft()`, O(1) |
| Mutating a dict/set while iterating it | `RuntimeError: dictionary changed size during iteration` | Iterate over `list(d.items())` if mutating |
| `d[key]` on a missing key | `KeyError` | `d.get(key, default)` or `defaultdict` |
| `set()` for order-preserving dedup | Sets are unordered | `list(dict.fromkeys(items))` preserves first-seen order |
| `(1)` meaning a one-element tuple | It's just `int(1)` | Use `(1,)` -- the trailing comma is required |
