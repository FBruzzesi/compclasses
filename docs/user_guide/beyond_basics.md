# Beyond the basics

## delegatee class

In order to have both more flexibility and more features, we can use the `delegatee` class instead of an iterable specifying which methods and class attributes should be forwarded.

## Features

### Attributes and methods validation

When using `delegatee` class we have the option to check whether or not attributes and methods are present in the class.
If we do so (`validate=True` parameter), then an `AttributeError` is raised if the attribute/method is not found in the class definition.

Remark that instance attributes, those which are often defined in the `__init__` method as `self.attr_name = ...`, cannot be detected from the class definition only, therefore it is not possible to check for them in advance.

If you want to forward such method, we suggest to set `validate=False`.

### The "star" argument

Sometimes you want to forward all the methods of a given class. To accomplish that, it is enough to define `attrs = ["*"]`.

Doing so will parse and add all the class attributes and methods of the `delegatee_cls` to the composed class.

Remark that dunder methods **are not** forwarded unless explicitly specified in the `attrs` param.

### Custom prefix & suffix

It is also possible to specify custom prefix and/or suffix for the forwarded method. The default behaviour is to call it as in the delegatee class, but it is possible to change that.

Remark that forwarded dunder methods ignore the prefix and suffix params.

## Examples
