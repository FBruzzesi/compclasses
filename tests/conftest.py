from typing import Type

import pytest


def create_foo_cls() -> Type:
    """Define Foo class"""

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

    return Foo


def create_bar_cls() -> Type:
    """Define Bar class"""

    class Bar:
        """Bar class"""

        b: float = 0.1

        def __bool__(self) -> bool:
            """Custom bar bool method"""
            return True

    return Bar


def create_baz_cls() -> Type:
    """Define Baz class"""

    class Baz:
        """Baz class"""

        def __init__(self, foo, bar):

            self.foo = foo  # instance of Foo class
            self.bar = bar  # instance of Bar class

    return Baz


@pytest.fixture(scope="function")
def foo_cls() -> Type:
    """Fixture returning Foo class definition"""

    return create_foo_cls()


@pytest.fixture(scope="function")
def bar_cls() -> Type:
    """Fixture returning Bar class definition"""

    return create_bar_cls()


@pytest.fixture(scope="function")
def baz_cls() -> Type:
    """Fixture returning Baz class definition"""

    return create_baz_cls()
