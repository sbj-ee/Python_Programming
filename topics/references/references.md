# References

A Python variable is a name bound to an object living somewhere in memory —
not a box that holds a value. Assignment binds a name to an object; it never
copies the object. This single idea explains most of the "surprising"
behavior newcomers hit around mutable state.

## Names are bindings, not boxes

```python
a = [1, 2, 3]
b = a            # b is now another name for the SAME list object
b.append(4)
a                # [1, 2, 3, 4] -- a sees the change too

id(a) == id(b)   # True -- same object
a is b           # True -- identity check
```

## is vs ==

```python
x = [1, 2]
y = [1, 2]
x == y      # True  -- equal contents
x is y      # False -- different objects

# CPython caches small ints (-5..256) and some string literals, so:
m, n = 5, 5
m is n      # True -- implementation detail, don't rely on it for correctness
```

Use `==` to compare values. Use `is` only for identity checks — most
commonly `is None`, `is True`, `is False`, or checking whether two names
refer to the exact same object.

## Function arguments are passed by object reference

```python
def mutate(lst):
    lst.append(99)      # mutates the caller's object

def rebind(lst):
    lst = [0, 0, 0]     # rebinds the LOCAL name only -- caller unaffected

shared = [1, 2]
mutate(shared)   # shared == [1, 2, 99]
rebind(shared)   # shared unchanged -- rebind() never touched the original
```

Python is neither "pass by value" nor "pass by reference" in the C/C++
sense — it is pass by object reference. Mutating the object the argument
refers to is visible to the caller; rebinding the local name is not.

## The mutable default argument trap

```python
def append_bad(item, target=[]):   # DANGER: target is created ONCE
    target.append(item)             # at function definition time
    return target

append_bad(1)   # [1]
append_bad(2)   # [1, 2]  <- unexpected: leaked state from the prior call!

def append_good(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

## Shallow vs. deep copy

```python
import copy

nested = [[1, 2], [3, 4]]
shallow = copy.copy(nested)      # or nested[:], or list(nested)
deep = copy.deepcopy(nested)

nested[0].append(99)
shallow[0]   # [1, 2, 99] -- inner list is SHARED, so it changed too
deep[0]      # [1, 2]     -- fully independent
```

`list(x)` and `x[:]` are shallow copies — they copy the container but not
the objects inside it. For a container of immutable elements (ints, strs),
shallow is indistinguishable from deep. For a container of mutable
elements (lists of lists, lists of objects), the difference matters.

## Garbage collection

CPython uses reference counting as the primary mechanism: an object is
freed the instant its refcount hits zero — deterministic and immediate,
unlike most garbage-collected languages. A secondary cyclic garbage
collector (the `gc` module) periodically finds and frees reference cycles
(e.g., two objects that reference each other) that refcounting alone can
never clean up.

```python
import sys
a = []
sys.getrefcount(a)   # includes the temporary reference getrefcount itself holds
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Mutable default argument (`def f(x=[])`) | State leaks across calls | Default to `None`, create inside the function |
| Using `is` to compare values | Works by luck on small ints/interned strings, breaks otherwise | Use `==` for value comparison |
| `b = a` expecting a copy | `b` aliases `a`; mutating one mutates both | Use `copy.copy()`/`copy.deepcopy()`/`list(a)` |
| `[[0] * 3] * 2` for a 2D grid | All rows are the SAME inner list | `[[0] * 3 for _ in range(2)]` |
| Assuming reassignment inside a function affects the caller | It only rebinds the local name | Mutate the object in place, or return and reassign at the call site |
