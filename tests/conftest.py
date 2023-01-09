import pytest


class Foo:
    """Foo class"""

    a: int = 1

    def __init__(self, value: int):
        """foo init"""
        self._foo: int = value

    def get_foo(self):
        """get _foo attribute"""
        return self._foo

    def hello_from_foo(self, name: str) -> str:
        """Method with argument"""
        return f"Hello {name}, this is Foo!"

    def __len__(self):
        """Custom foo len method"""
        return 123

    # TODO: add staticmethod's, classmethod's, property's to test


class Bar:
    """Bar class"""

    b: float = 0.1

    def __len__(self) -> int:
        """Custom bar len method"""
        return 42


class Baz:
    """Baz class"""

    def __init__(self, foo: Foo, bar: Bar):
        self.foo = foo
        self.bar = bar


@pytest.fixture
def foo_cls():
    """Fixture returning Foo class definition"""

    return Foo


@pytest.fixture
def bar_cls():
    """Fixture returning Bar class definition"""

    return Bar


@pytest.fixture
def baz_cls():
    """Fixture returning Bar class definition"""

    return Baz
