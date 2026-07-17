"""Exercise 14: Inheritance.

Single and multiple inheritance, super(), and the Method Resolution Order
(MRO) that decides which class's method runs when several bases define one.
"""


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"

    def describe(self) -> str:
        return f"I am {self.name}, a {type(self).__name__}"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"


class ServiceAnimal(Dog):
    def __init__(self, name: str, handler: str) -> None:
        super().__init__(name)  # delegate to the parent's __init__
        self.handler = handler

    def describe(self) -> str:
        # Extend, don't just replace: call the parent version and add to it.
        base = super().describe()
        return f"{base}, working with {self.handler}"


# --- Multiple inheritance and the MRO ---
class Swimmer:
    def move(self) -> str:
        return "swims"


class Runner:
    def move(self) -> str:
        return "runs"


class Amphibious(Swimmer, Runner):
    """Python resolves attribute lookup via C3 linearization (the MRO).
    Left-to-right base order matters: Swimmer is checked before Runner.
    """

    pass


def main() -> None:
    animals: list[Animal] = [Dog("Rex"), Cat("Whiskers"), Animal("Generic")]
    for a in animals:
        print(a.speak())

    # --- Polymorphism: the same call, different behavior per subclass ---
    for a in animals:
        print(a.describe())

    service_dog = ServiceAnimal("Buddy", "Alex")
    print(service_dog.speak())  # inherited from Dog
    print(service_dog.describe())  # overridden, extends Animal's version

    # --- isinstance respects the whole hierarchy ---
    print(f"isinstance(service_dog, Dog) = {isinstance(service_dog, Dog)}")
    print(f"isinstance(service_dog, Animal) = {isinstance(service_dog, Animal)}")
    print(f"isinstance(service_dog, Cat) = {isinstance(service_dog, Cat)}")

    # --- MRO in action ---
    frog = Amphibious()
    print(f"frog.move() = {frog.move()}")  # "swims": Swimmer comes first
    print("MRO:", [cls.__name__ for cls in Amphibious.__mro__])


if __name__ == "__main__":
    main()
