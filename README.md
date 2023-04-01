<img src="docs/img/compclass-logo.svg" width=180 height=180 align="right">

# Compclasses

![](https://img.shields.io/github/license/FBruzzesi/compclasses)
<img src ="docs/img/interrogate-shield.svg">
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Like *dataclasses*, but for composition.

As the Gang of Four (probably) said:

> favor object composition over class inheritance.

However when we use composition in Python, we cannot access methods directly from the composed class, and we either re-define these methods from scratch, or access them using chaining.

This codebase wants to address such issue and make it easy to do so, by [delegating](https://en.wikipedia.org/wiki/Delegation_(object-oriented_programming)) the desired methods of a class to its attributes.

---

**Documentation**: https://fbruzzesi.github.io/compclasses

**Source Code**: https://github.com/fbruzzesi/compclasses

---

## Table of Content

- [Compclasses](#compclasses)
  * [Table of Content](#table-of-content)
  * [Alpha Notice](#alpha-notice)
  * [Installation](#installation)
  * [Getting Started](#getting-started)
    + [compclass (decorator)](#compclass-decorator)
    + [CompclassMeta (metaclass)](#compclassmeta-metaclass)
  * [Advanced usage](#advanced-usage)
  * [Why Composition (TL;DR)](#why-composition-tldr)
  * [Feedbacks](#feedbacks)
  * [Contributing](#contributing)
  * [Inspiration](#inspiration)
  * [Licence](#licence)

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which everything breaks. If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Installation

**compclasses** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, ideally by using a virtual environment.

From a terminal it is possible to install it with:

```bash
python -m pip install compclasses
```

## Getting Started

Let's suppose we have the following 3 classes, `Foo`, `Bar` and `Baz`:

- `Foo` and `Bar` are independent from one another;
- `Baz` get initialized with two class attributes (`_foo`, `_bar`) which are instances of the other two classes.

```python title="Classes definition"
class Foo:
    """Foo class"""

    def __init__(self, value: int):
        """foo init"""
        self._value = value

    def get_value(self):
        """get value attribute"""
        return self._value

    def hello(self, name: str) -> str:
        """Method with argument"""
        return f"Hello {name}, this is Foo!"


class Bar:
    """Bar class"""
    b: int = 1

    def __len__(self) -> int:
        """Custom len method"""
        return 42

class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar
```

Now let's instantiate them and try see how we would access the "inner" attributes/methods:

```python title="Naive approach"
foo = Foo(123)
bar = Bar()

baz = Baz(foo, bar)

baz._foo.get_value()  # -> 123
baz._foo.hello("GitHub")  # -> "Hello GitHub, this is Foo!"
baz._bar.__len__()  # -> 42

len(baz)  # -> TypeError: object of type 'Baz' has no len()
```

### compclass (decorator)

Using the [compclass](https://fbruzzesi.github.io/compclasses/api/compclass) decorator we can *forward* the methods that we want to the `Baz` class from its attributes at definition time:

```python title="Using compclass"
from compclasses import compclass

delegates = {
    "_foo": ( "get_value", "hello"),
    "_bar": ("__len__", )
}

@compclass(delegates=delegates)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar

baz = Baz(foo, bar)
baz.get_value()  # -> 123
baz.hello("GitHub")  # -> "Hello GitHub, this is Foo!"
len(baz)  # -> 42
```

We can see how now we can access the methods directly.

Remark that in the `delegates` dictionary, we have that:

- the keys correspond to the attribute names in the `Baz` class;
- each value should be an iterable of string corresponding to methods/attributes present in the class instance associated to the key-attribute.

The `compclass` decorator adds each attribute and method as a [property attribute](http://docs.python.org/3/library/functions.html#property), callable as
`self.<attr_name>` instead of `self.<delegatee_cls>.<attr_name>`

### CompclassMeta (metaclass)

The equivalent, but alternative, way of doing it is by using the [`CompclassMeta`](https://fbruzzesi.github.io/compclasses/api/compclassmeta.md) metaclass when you define the class.

```python
from compclasses import CompclassMeta

delegates = {
    "_foo": ( "get_value", "hello"),
    "_bar": ("__len__", )
}

class Baz(metaclass=CompclassMeta, delegates=delegates):
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar

baz = Baz(foo, bar)
baz.get_value()  # -> 123
baz.hello("GitHub")  # -> "Hello GitHub, this is Foo!"
len(baz)  # -> 42
```

As you can see the syntax is nearly one-to-one with the `compclass` decorator, and the resulting behaviour is exactly the same!

## Advanced usage

Instead of using an iterable in the `delegates` dictionary, we suggest to use a [delegatee](https://fbruzzesi.github.io/compclasses/api/delegatee) instance as a value.

This will yield more flexibility and features when decide to forward class attributes and methods.

Check the dedicated [documentation page](https://fbruzzesi.github.io/compclasses/user_guide/beyond_basics/) to get a better understanding and see more examples on how `delegatee` can be used, its pros and cons.

## Why Composition (TL;DR)

Overall, composition is a more flexible and transparent way to reuse code and design classes in Python. It allows to build classes that are customized to your specific needs, and it promotes code reuse and modularity.

A more detailed explaination is present in the [documentation page](https://fbruzzesi.github.io/compclasses/composition).

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
