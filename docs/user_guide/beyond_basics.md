# Beyond the basics

## delegatee class

Instead of using an iterable in the `delegates` dictionary, it is possible to pass a [delegatee](https://fbruzzesi.github.io/compclasses/api/delegatee/) instance as a value.

This will yield more flexibility and features when decide to forward class attributes and methods.

Let's see in detail which features are currently available.

## Features

### Attributes and methods validation

When using `delegatee` class we have the option to check whether or not attributes and methods are present in the class.

If we do so (`validate=True` parameter), then an `AttributeError` is raised if the attribute/method is not found in the class definition.

Remark that we check for:

- class attributes and methods;
- instance attributes assigned in the `__init__` method, by parsing the `__init__` code and look for `self.attr_name = ...` syntax.

!!! note "Why should you check if an attribute/method is present?"

    A validation step makes sure that changing something from the component class doesn't break the class using the given component somewhere down the rabbit hole, but it gets detected as soon as possible.

### The "star" argument

Sometimes you want to forward all the methods of a given class. To accomplish that, it is enough to pass `attrs=["*"]` to the `delegatee` class.

Doing so will parse and add all the class attributes, methods and instance attributes of the `delegatee_cls` to the composed class.

This gives the possibility to forward all the methods/attributes of a component with a single instruction.

!!! warning

    Dunder methods and instance attributes **are not** forwarded unless explicitly specified in the `attrs` parameter.

### Custom prefix & suffix

It is also possible to specify custom prefix and/or suffix for each component. The default behaviour is to call it as in the delegatee class, but it is possible to change that.

!!! warning

    Dunder methods ignore the prefix and suffix parameters.

### Verbosity

`compclass` and `CompclassMeta` accept a `verbose` parameter which defines the level of verbosity when setting those forwarded methods.

If the value is `True` then we explicitly "declare" each forwarded method/attribute.

## Examples

As in the previous section let's define the `Foo` and `Bar` classes:

```python title="classes definition"
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
```

Now instead of using a list of attribute/methods name, let's define delegates using `delegatee` class, with few extra params:

```python title="delegatee class"
from compclasses import compclass, delegatee

delegates = {
    "_foo": delegatee(
        delegatee_cls=Foo,  # class definition of the _foo instance
        attrs=("*", ),  # list of attributes/methods to forward
        suffix="_from_foo"  # let's add a prefix to distinguish from where the method is forwarded, this can be any string
        ),
    "_bar": delegatee(
        delegatee_cls=Bar,
        attrs=("__len__", "b"),
        validate=True,  # we want to validate that Bar class has "__len__" method and "b" attribute
        prefix="bar_"  # let's add a prefix to distinguish from where the method is forwarded, this can be any string
        )
}

@compclass(
    delegates=delegates,
    verbose=True  # verbisity level to use
)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar

# Unable to parse __init__ method of <class '__main__.Bar'> due to the following reason: module, class, method, function, traceback, frame, or code object was expected, got wrapper_descriptor
# Setting get_value_from_foo from _foo.get_value
# Setting hello_from_foo from _foo.hello
# Setting _value_from_foo from _foo._value
# Setting __len__ from _bar.__len__
# Setting bar_b from _bar.b
```

Let's see what is happening here:

- `Bar`'s `delegatee` have `validate=True` param, therefore checks `__len__` and `b` are presents. While doing so it fails to find an `__init__` method (this is an implementation detail of the class `object` implemented in _C_). Notice that however this does not raise an error. It would have if any of `__len__` or `b` were not found.
- Passing `attrs=("*", )` for `Foo` allows to forward all non-dunder methods of `Foo` to `Baz`, namely `get_value`, `hello` and `_value` (this last one is found in `Foo.__init__`).
- Since we are using a suffix, the new methods in `Baz` are called `get_value_from_foo`, `hello_from_foo` and `_value_from_foo`.
- Similarly we use a prefix in `Bar` delegatee, hence `b` becomes `bar_b`, yet `__len__` is forwarded as-is.

Let's now see what happens if a class attribute or an undefined method is passed in the `attrs` list:

```python title="validating attributes/methods"
delegatee(delegatee_cls=Foo, attrs=("_value",))
delegatee(delegatee_cls=Foo, attrs=("some_fake_method",))
```
> (...) AttributeError: '<class '__main__.Foo'>' has no attribute nor method 'some_fake_method'

In the first case, `_value` attribute can be detected from the `__init__` method as we saw above already.

For the latter case, it is clear that the method is not present in the class definition, and an error is raised.
