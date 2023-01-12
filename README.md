<img src="docs/img/compclass-logo.svg" width=180 height=180 align="right">

# Compclasses

Like *dataclasses*, but for composition.

As the Gang of Four (probably) said:

> favor object composition over class inheritance.

However when we use composition in Python, we cannot access methods directly from the composed class, and we either re-define these methods from scratch, or access them using chaining.

This codebase wants to address such issue and make it easy to do so, by [delegating](https://en.wikipedia.org/wiki/Delegation_(object-oriented_programming)) the desired methods of a class to its attributes.

---

**Documentation**: https://fbruzzesi.github.io/compclasses

**Source Code**: https://github.com/fbruzzesi/compclasses

---

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which everything breaks. If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Installation

**compclasses** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, ideally by using a virtual environment.

From a terminal it is possible to install it with:

```bash
python -m pip install compclasses
```

## Getting Started

Let's suppose to have the following classes:

```python
class Foo:
    """Foo class"""

    def __init__(self, value: int):
        """foo init"""
        self.value = value

    def get_foo(self):
        """get value attribute"""
        return self.value

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
        self._foo = foo
        self._bar = bar
```

Now let's instantiate them and try see how we would access the inner methods/attributes:

```python
foo = Foo(123)
bar = Bar()

baz = Baz(foo, bar)

baz._foo.get_foo()  # -> 123
baz._foo.hello_from_foo("GitHub")  # -> "Hello GitHub, this is Foo!"
baz._bar.__len__()  # -> 42

len(baz)  # -> TypeError: object of type 'Baz' has no len()
```

Using the `compclass` decorator we can *forward* the methods that we want to the `Baz` class at definition time:

```python
from compclasses import compclass

delegates = {
    "_foo": ( "get_foo", "hello_from_foo"),
    "_bar": ("__len__", )
}

@compclass(delegates=delegates)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar

baz = Baz(foo, bar)
baz.get_foo()  # -> 123
baz.hello_from_foo("GitHub")  # -> "Hello GitHub, this is Foo!"
len(baz)  # -> 42
```

We can see how now we can access the methods directly.

Remark that in the `delegates` dictionary, we have that:

- the key corresponds to the attribute name in the Baz class
- the value should be an iterable of string corresponding to methods/attributes present in the class instance associated to the key-attribute.

### delegatee class

Instead of using an iterable in the `delegates` dictionary, it is possible to pass a `delegatee` instance as a value.

Such class supports some additional features such as:

- class attributes and methods validation.
- it allows to pass `*` value to pass all non-dunder attributes/methods.
- adding custom attributes/methods prefix and/or suffix.

Since `get_foo` and `hello_from_foo` are the only two methods of the `Foo` class, the previous example can be rewritten as:

```python
from compclasses import compclass, delegatee

delegates = {
    "_foo": delegatee(Foo, attrs=["*"]),
    "_bar": delegatee(Bar, attrs=["__len__"])
}

@compclass(delegates=delegates)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar

baz = Baz(foo, bar)
baz.get_foo()  # -> 123
baz.hello_from_foo("GitHub")  # -> "Hello GitHub, this is Foo!"
len(baz)  # -> 42
```

Check the dedicated [documentation page](https://fbruzzesi.github.io/compclasses/user_guide/beyond_basics/) to get a better understanding and see more examples on how `delegatee` can be used, its pros and cons.

## Why Composition (TL;DR)

Overall, composition is a more flexible and transparent way to reuse code and design classes in Python. It allows to build classes that are customized to your specific needs, and it promotes code reuse and modularity.

A more detailed explaination is present in the dedicated [documentation page](https://fbruzzesi.github.io/compclasses/composition).

## Feedbacks

Any feedback, improvement/enhancement or issue is welcome in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Contributing

Please refer to the [contributing guidelines](https://fbruzzesi.github.io/compclasses/contribute) in the documentation site.

## Inspiration

This projects is inspired by the [forwardable](https://github.com/5long/forwardable) library, a "utility for easy object composition via delegation".

However I was looking for both more flexibility and more features. In particular:

- a clear separation between class definition and method forwarding;
- a validation step to make sure that changing something from the component doesn't break the class;
- the possibility to forward all the methods/attributes of a given component with a single instruction;
- the chance of adding prefix and/or suffix for each component;

Please refer to [Beyond the basics](user_guide/beyond_basics.md) page to see example usages.

## Licence

The project has a [MIT Licence](https://github.com/FBruzzesi/compclasses/blob/main/LICENSE)
