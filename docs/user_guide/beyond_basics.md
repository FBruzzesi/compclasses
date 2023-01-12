# Beyond the basics

## delegatee class

Instead of using an iterable in the `delegates` dictionary, it is possible to pass a `delegatee` instance as a value.

This will yield more flexibility and features when decide to forward class attributes and methods.

Let's see in detail which features are currently available.

## Features

### Class attributes and methods validation

When using `delegatee` class we have the option to check whether or not attributes and methods are present in the class.

If we do so (`validate=True` parameter), then an `AttributeError` is raised if the attribute/method is not found in the class definition.

Remark that instance attributes, those which are often defined in the `__init__` method as `self.attr_name = ...`, cannot be detected from the class definition only, therefore it is not possible to check for them in advance.

If you want to forward such attributes, we suggest to set `validate=False`.

!!! note "Why should you check if an attribute/method is present?"

    A validation step makes sure that changing something from the component class doesn't break the class using the given component somewhere down the rabbit hole, but it gets detected as soon as possible.

### The "star" argument

Sometimes you want to forward all the methods of a given class. To accomplish that, it is enough to pass `attrs=["*"]` to the `delegatee` class.

Doing so will parse and add all the class attributes and methods of the `delegatee_cls` to the composed class.

This gives the possibility to forward all the methods/attributes of a component with a single instruction.

!!! warning

    Dunder methods and instance attributes **are not** forwarded unless explicitly specified in the `attrs` parameter.

### Custom prefix & suffix

It is also possible to specify custom prefix and/or suffix for each component. The default behaviour is to call it as in the delegatee class, but it is possible to change that.

!!! warning

    Dunder methods ignore the prefix and suffix parameters.

### Verbosity

`compclass` decorator accepts a `verbose` parameter.

Its default value is 0, which simply means silent, however it is possible to set it with an integer from 1 to 4:

- `verbose=1`: *setting* a method from a class component is explicit.
- `verbose=2`: *calling* a method from a class component is explicit.
- `verbose=3`: *deleting* a method from a class component is explicit.
- `verbose=4`: *setting-calling-deleting* a method from a class component is explicit.

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
    verbose=4  # verbisity level to use
)
class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self._foo = foo
        self._bar = bar
```
>Setting get_value_from_foo from _foo.get_value
>
>Setting hello_from_foo from _foo.hello
>
>Setting \_\_len\_\_ from _bar.\_\_len\_\_
>
>Setting bar_b from _bar.b

Let's see what is happening here:

- Setting `verbose=4` leads to logging which attributes/methods are set in the `Baz` class and from which method.
- Passing `attrs=("*", )` forwards all non-dunder methods of `Foo` to `Baz`, namely `get_value` and `hello`.
- Since we are using a suffix, the new methods in `Baz` are called `get_value_from_foo` and `hello_from_foo`.
- Similarly we use a prefix in `Bar` delegatee, hence `b` becomes `bar_b`, yet `__len__` is forwarded as-is.

```python title="calling methods"
foo = Foo(123)
bar = Bar()
baz = Baz(foo, bar)

baz.get_value_from_foo()  # 123
baz.hello_from_foo("Github")  # 'Hello Github, this is Foo!
len(baz)  # 42
baz.bar_b  # 1
```

>Calling get_value_from_foo from _foo.get_value
>
>Calling hello_from_foo from _foo.hello
>
>Calling __len__ from _bar.__len__
>
>Calling bar_b from _bar.b

As expected, we can call the methods directly as we named them. Since `verbose=4` then also each call is logged.

Let's now see what happens if a class attribute or an undefined method is passed in the `attrs` list:

```python title="validating attributes/methods"
delegatee(delegatee_cls=Foo, attrs=("_value",))
delegatee(delegatee_cls=Foo, attrs=("some_fake_method",))
```

> (...) AttributeError: '<class '__main__.Foo'>' has no attribute/method '_value'
>
> (...) AttributeError: '<class '__main__.Foo'>' has no attribute/method 'some_fake_method'

In the first case, we cannot detect `_value` attribute, since this doesn't exist at `Foo` definition time, but only when an object is instantiated.
For the same reason, these attributes are not picked up when setting `attrs=["*"]`.

For the latter case, it is clear that the method is not present in the class definition, and an error is raised.

!!! tip
    If you want to forward instance attributes, then this is possible by explicitly setting `validate=False`.
