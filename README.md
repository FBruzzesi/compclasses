<img src="docs/img/compclass-logo.svg" width=180 height=180 align="right">

# compclasses

Like *dataclasses*, but for composition.

As the Gang of Four (probably) said:

> favor object composition over class inheritance.

However when we use composition in Python, we cannot access methods directly from the composed class, and we either re-define these methods from scratch, or access them using chaining.

This codebase wants to address such issue and make it easy to do so, by [delegating](https://en.wikipedia.org/wiki/Delegation_(object-oriented_programming)) the desired methods of a class to its attributes.

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which everything breaks. If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Getting Started

Let's suppose to have the following classes:

```python
class Foo:
    """Foo class"""

    def __init__(self, value: int):
        """foo init"""
        self._foo: int = value

    def get_foo(self):
        """get _foo attribute"""
        return self._foo

    def hello_from_foo(self, name: str) -> str:
        """Method with argument"""
        return f"Hello {name}, this is Foo!"


class Bar:
    """Bar class"""

    def __len__(self) -> int:
        """Custom len method"""
        return 42

class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self.foo = foo
        self.bar = bar
```

Now let's instantiate them and try see how we would access the inner methods/attributes:

```python
foo = Foo(123)
bar = Bar()

baz = Baz(foo, bar)

baz.foo.get_foo()  # -> 123
baz.foo.hello_from_foo("GitHub")  # -> "Hello GitHub, this is Foo!"
baz.bar.__len__()  # -> 42

len(baz)  # -> TypeError: object of type 'Baz' has no len()
```

Using the `compclass` decorator we can *forward* the methods that we want to the `Baz` class at definition time:

```python
from compclasses import compclass

delegates={
    "foo": ( "get_foo", "hello_from_foo"),
    "bar": ("__len__", )
}

@compclass(delegates=delegates)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self.foo = foo
        self.bar = bar

baz = Baz(foo, bar)
baz.get_foo()  # -> 123
baz.hello_from_foo("GitHub")  # -> "Hello GitHub, this is Foo!"
len(baz)  # -> 42
```

We can see how now we can access the methods directly.

Remark that in the `delegates` dictionary, we have that:

- the key corresponds to the attribute name in the Baz class
- the value should be an iterable of string corresponding to methods/attributes present in the class instance associated to the key-attribute.

## Installation

You can install the library using pip:

```bash
python -m pip install compclasses
```

## Why Composition

Composition is in general more flexible than inheritance. This doesn't mean that we should never use inheritance.

As a rule of thumb, one can think to:

- Use composition if object `A` *has a* relationship with object `B` (e.g. a square has a side).
- Use inheritance if object `A` *is a* specification of object `B` (e.g. a square is a shape).

One of the most common drawback of using composition is *exactly* the fact that methods/attributes provided by single components may have to be implemented again.

There are many resources where one can get a better understanding of why and when to prefer composition over inheritance:

- [Wikipedia page](https://en.wikipedia.org/wiki/Composition_over_inheritance)
- [Stack overflow discussion](https://stackoverflow.com/questions/49002/prefer-composition-over-inheritance)
- [The perils of inheritance - by Ariel Ortiz](https://www.youtube.com/watch?v=YXiaWtc0cgE&list=WL&index=1)

## Feedbacks

Any feedback, improvement/enhancement or issue is welcome in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Contributing

Make sure to check the [issue list](https://github.com/FBruzzesi/compclasses/issues) beforehand.

To get started locally, you can clone the repo and quickly get started using the `Makefile`:

```bash
git clone git@github.com:FBruzzesi/compclasses.git
cd compclasses
make init-dev
```

## Licence

This repository has a MIT Licence

## Other projects

This projects is inspired by the [forwardable](https://github.com/5long/forwardable) library, however I was looking for both more flexibility and more features.
