# Beyond the basics

## delegatee class

Instead of using an iterable in the `delegates` dictionary, it is possible to pass a `delegatee` instance as a value.

This will yield more flexibility and features when decide to forward class attributes and methods.

## Features

### Class attributes and methods validation

When using `delegatee` class we have the option to check whether or not attributes and methods are present in the class.

If we do so (`validate=True` parameter), then an `AttributeError` is raised if the attribute/method is not found in the class definition.

Remark that instance attributes, those which are often defined in the `__init__` method as `self.attr_name = ...`, cannot be detected from the class definition only, therefore it is not possible to check for them in advance.

If you want to forward such attributes, we suggest to set `validate=False`.

!!! note "Why should you check if an attribute/method is present?"

    A validation step makes sure that changing something from the component class doesn't break the class using the given component somewhere down the rabbit hole, but it gets detected as soon as possible.

### The "star" argument

Sometimes you want to forward all the methods of a given class. To accomplish that, it is enough to pass `attrs = ["*"]` to the `delegatee` class.

Doing so will parse and add all the class attributes and methods of the `delegatee_cls` to the composed class.

This gives the possibility to forward all the methods/attributes of a component with a single instruction.

!!! warning

    Dunder methods **are not** forwarded unless explicitly specified in the `attrs` param.

### Custom prefix & suffix

It is also possible to specify custom prefix and/or suffix for each component. The default behaviour is to call it as in the delegatee class, but it is possible to change that.

!!! warning

    Dunder methods ignore the prefix and suffix params.


## Examples
