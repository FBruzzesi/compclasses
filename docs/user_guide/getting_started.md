# Getting Started

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
