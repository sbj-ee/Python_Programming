# Generators

A generator is a function containing `yield`: calling it doesn't run the
body, it returns a lazy iterator that runs up to the next `yield` each time
you ask for a value. This makes generators the idiomatic way to process
sequences too large to hold in memory, or infinite in principle.

## The iterator protocol, by hand

```python
class CountUp:
    def __init__(self, start, stop):
        self.current, self.stop = start, stop
    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

list(CountUp(0, 5))   # [0, 1, 2, 3, 4]
```

## The same thing, with yield

```python
def count_up(start, stop):
    current = start
    while current < stop:
        yield current
        current += 1

gen = count_up(0, 3)
next(gen)   # 0 -- runs to the first yield, then pauses
next(gen)   # 1 -- resumes right after the yield, runs to the next one
next(gen)   # 2
next(gen)   # StopIteration -- the function returned
```

`yield` turns an ordinary function into a generator function automatically;
no manual `__iter__`/`__next__` bookkeeping required.

## Infinite generators, safely bounded by the consumer

```python
def fibonacci():
    a, b = 0, 1
    while True:              # never terminates on its own
        yield a
        a, b = b, a + b

import itertools
list(itertools.islice(fibonacci(), 10))   # take only the first 10
```

## Generator expressions

```python
squares = (x * x for x in range(10**6))   # nothing computed yet -- lazy
sum(squares)                                # computed one at a time, O(1) memory

# vs. a list comprehension, which builds the WHOLE list immediately:
squares_list = [x * x for x in range(10**6)]   # allocates ~8MB immediately
```

## yield from: delegating to a sub-generator

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # delegates iteration to the recursive call
        else:
            yield item

list(flatten([1, [2, 3, [4, 5]], 6]))   # [1, 2, 3, 4, 5, 6]
```

## itertools: the standard toolbox

```python
import itertools

itertools.chain([1, 2], [3, 4])            # 1, 2, 3, 4
itertools.combinations("ABC", 2)            # AB, AC, BC
itertools.groupby("aaabbc")                 # (a, aaa), (b, bb), (c, c)
itertools.islice(fibonacci(), 5, 10)         # slice a generator lazily
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Iterating an exhausted generator again | Yields nothing -- silently, no error | Generators are single-use; call the generator function again for a fresh one |
| Building a huge list where a generator would do | Unnecessary memory use for large/streaming data | Use a generator expression or `yield` |
| Forgetting a generator is lazy | Side effects inside it don't happen until iterated | Wrap in `list(...)` if you need eager evaluation |
| Infinite generator without a bound at the consumer | Hangs forever | Pair with `itertools.islice` or an explicit `break` |
| Mixing `return value` in a generator expecting it in the yielded stream | The value becomes `StopIteration.value`, not a yielded item | Use `yield value` for stream items; `return` only ends the generator |
