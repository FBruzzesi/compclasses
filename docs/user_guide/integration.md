# Integration with Pydantic and dataclasses

Integrating with [Pydantic](https://docs.pydantic.dev/latest/) and [dataclasses](https://docs.python.org/3/library/dataclasses.html) can be beneficial for leveraging the powerful features provided by these libraries while also enjoying the flexibility and ease of use offered by composition.

Integration is possible and seamless, as **Compclasses** is designed to be compatible with both.

Let's see how this integration would work in practice.

First let's define the `Foo` and `Bar` classes:

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

    def __repr__(self) -> str:
        return f"Foo({self._value})"


class Bar:
    """Bar class"""
    b: int = 1

    def __len__(self) -> int:
        """Custom len method"""
        return 42
    def __repr__(self) -> str:
        return "baaarepr"

foo = Foo(123)
bar = Bar()

delegates = {
    "foo": ( "get_value", "hello"),
    "bar": ("__len__", )
}
```
## Pydantic

Pydantic is a popular library for data validation and parsing, which allows you to define data models using Python annotations. Pydantic provides automatic validation and conversion of data based on the defined models, while Compclasses enables composition and delegation of methods, making it easier to work with complex object structures.

The integration with Pydantic can be done by using the [compclass](../api/compclass.md) decorator, which will create a new class inheriting from the Pydantic `BaseModel` class, and will add the methods defined in the `delegates` dictionary.

```python title="Pydantic integration"
from compclasses import compclass
from pydantic import BaseModel

@compclass(delegates=delegates, verbose=False)
class Baz(BaseModel):
    """Baz class"""
    foo: Foo
    bar: Bar

    class Config:
        arbitrary_types_allowed = True

baz = Baz(foo=foo, bar=bar)
baz, len(baz), baz.get_value(), baz.hello("there")
# (Baz(foo=Foo(123), bar=baaarepr), 42, 123, 'Hello there, this is Foo!')
```

On the other hand using the [CompclassMeta](../api/compclassmeta.md) metaclass will result in the following error:

> TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases


## Dataclasses

Dataclasses are a Python built-in module that provides a concise syntax for defining classes with automatic generation of common methods. By integrating Compclasses with dataclasses, you can enhance the functionality and extensibility of your dataclasses.

The integration with dataclasses can be done by using both [compclass](../api/compclass.md) decorator and [CompclassMeta](../api/compclassmeta.md) metaclass:

=== "dataclass + compclass"

    ```python
    from compclasses import compclass
    from dataclasses import dataclass

    @dataclass
    @compclass(delegates=delegates, verbose=False)
    class Baz:
        """Baz class"""
        foo: Foo
        bar: Bar

    baz = Baz(foo=foo, bar=bar)
    baz, len(baz), baz.get_value(), baz.hello("there")
    # (Baz(foo=Foo(123), bar=baaarepr), 42, 123, 'Hello there, this is Foo!')
    ```


=== "dataclass + CompclassMeta"

    ```python
    from compclasses import CompclassMeta
    from dataclasses import dataclass

    @dataclass
    class Baz(metaclass=CompclassMeta, delegates=delegates, verbose=False):
        """Baz class"""
        foo: Foo
        bar: Bar

    baz = Baz(foo=foo, bar=bar)
    baz, len(baz), baz.get_value(), baz.hello("there")
    # (Baz(foo=Foo(123), bar=baaarepr), 42, 123, 'Hello there, this is Foo!')
    ```
