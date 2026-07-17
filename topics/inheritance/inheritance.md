# Inheritance

Python supports single and multiple inheritance. `super()` delegates to the
next class in the Method Resolution Order (MRO) — not necessarily the
"parent" in a simple sense once multiple inheritance is involved.

## Single inheritance and super()

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):                     # override
        return f"{self.name} says Woof!"

class ServiceDog(Dog):
    def __init__(self, name, handler):
        super().__init__(name)            # delegate to Animal.__init__
        self.handler = handler
    def speak(self):
        base = super().speak()             # extend Dog.speak(), don't replace it
        return f"{base} (working with {self.handler})"
```

## Polymorphism

```python
animals = [Dog("Rex"), Animal("Generic")]
for a in animals:
    print(a.speak())   # same call, different behavior per actual type

isinstance(ServiceDog("Buddy", "Alex"), Animal)   # True -- whole hierarchy
```

## Abstract base classes: enforcing a contract

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

Shape()      # TypeError: Can't instantiate abstract class Shape
Circle(2)    # fine -- area() is implemented
```

## Multiple inheritance and the MRO

```python
class Swimmer:
    def move(self): return "swims"

class Runner:
    def move(self): return "runs"

class Amphibious(Swimmer, Runner):
    pass

Amphibious().move()          # "swims" -- Swimmer is listed first
Amphibious.__mro__            # (Amphibious, Swimmer, Runner, object)
```

Python resolves multiple inheritance with C3 linearization: a consistent
left-to-right, depth-first order that guarantees each class appears before
its own bases, and preserves the order bases were listed in.

## Mixins: composition via small, focused base classes

```python
class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggingMixin:
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")

class User(JSONMixin, LoggingMixin):
    def __init__(self, name):
        self.name = name

u = User("Ada")
u.to_json()          # mixin behavior, no direct inheritance relationship needed
u.log("created")
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Forgetting `super().__init__()` in a subclass | Parent's setup never runs; missing attributes later | Always call `super().__init__(...)` unless deliberately replacing it |
| Assuming multiple inheritance resolves left-to-right always intuitively | Surprising method resolution with diamond hierarchies | Print `Cls.__mro__` when in doubt |
| Deep inheritance chains for code reuse | Fragile, hard to reason about ("fragile base class" problem) | Prefer composition or `typing.Protocol` where inheritance isn't semantically required |
| Overriding `__init__` without matching the base signature | `TypeError` when base code calls it with different arguments | Keep overridden signatures compatible, or accept `*args, **kwargs` |
| Using inheritance purely to share utility methods | Couples unrelated classes; mixins/composition are usually clearer | Reach for a mixin or a standalone helper function instead |
