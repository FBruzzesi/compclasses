# Getting Started

## Introduction

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

## compclass (decorator)

Using the [compclass](../api/compclass.md) decorator we can *forward* the methods that we want to the `Baz` class from its attributes at definition time:

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

The `compclass` decorator adds each attribute and method as a [property attribute](https://docs.python.org/3/library/functions.html#property), callable as
`self.<attr_name>` instead of `self.<delegatee_cls>.<attr_name>`

## CompclassMeta (metaclass)

The equivalent, but alternative, way of doing it is by using the [`CompclassMeta`](../api/compclassmeta.md) metaclass when you define the class.

```python title="Using CompclassMeta"
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

## Next Steps

Instead of using an iterable in the `delegates` dictionary, we suggest to use a [delegatee](https://fbruzzesi.github.io/compclasses/api/delegatee/) instance as a value.

This will yield more flexibility and features when decide to forward class attributes and methods.

In the next section we will do a deep dive into what these features are, how to use them and their pros and cons.
