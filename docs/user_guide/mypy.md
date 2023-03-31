# MyPy Compliance

## The problem
For those who follow the mypy religion, I hear you! I do too!

And adding methods/attributes dynamically will make MyPy complain and scream at you:

```py
from compclasses import CompclassMeta

class Foo:
    """Foo class"""

    _value: int = 1
    
    def get_value(self):
        """get value attribute"""
        return self._value

class Baz(metaclass=CompclassMeta, delegates={"_foo": ("_value", "get_value")}):
    """Baz class"""

    def __init__(self, foo: Foo):
        self._foo = foo


baz = Baz(foo=Foo())
baz._value  # error: "Baz" has no attribute "_value"
baz.get_value()  # error: "Baz" has no attribute "get_value"
```

There are at least two ways to make mypy quiet about this.

## Solutions

### Make a promise

You can make a promise to mypy in the class definition that such attribute/method will exist even without defining it directly:
```py
from typing import Callable

class Baz(metaclass=CompclassMeta, delegates={"_foo": ("_value", "get_value")}):
    """Baz class"""
    
    _value: int
    get_value: Callable

    def __init__(self, foo: Foo):
        self._foo = foo

baz = Baz(foo=Foo())
baz._value
baz.get_value()
```

This can be annoying, especially when adding a suffix and/or a prefix, however will give you the best results from your IDE.

### type: ignore

This is the dirty way which saves you when you are kind of desperate (let's be honest!):

```py
class Baz(metaclass=CompclassMeta, delegates={"_foo": ("_value", "get_value")}):
    """Baz class"""

    def __init__(self, foo: Foo):
        self._foo = foo

baz = Baz(foo=Foo())
baz._value  # type: ignore
baz.get_value()  # type: ignore
```
