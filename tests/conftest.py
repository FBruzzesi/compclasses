import pytest


class Foo:
    """Foo class"""

    a: float = 0.1

    def __init__(self, value: int):
        """foo init"""
        self._foo: int = value

    def get_foo(self):
        """get _foo attribute"""
        return self._foo

    def hello_from_foo(self, name: str) -> str:
        """Method with argument"""
        return f"Hello {name}, this is Bar!"

    def __len__(self) -> int:
        """Custom len method"""
        return 42

    # TODO: test staticmethod's, classmethod's, property's


class Bar:
    """Bar class"""

    def __init__(self, foo: Foo, bar_value: int = 123):
        self.foo = foo
        self._bar = bar_value

    def get_bar(self):
        """get _bar attribute"""
        return self._bar


@pytest.fixture
def foo_cls():
    """Fixture returning Foo class definition"""

    return Foo


@pytest.fixture
def bar_cls():
    """Fixture returning Bar class definition"""

    return Bar
