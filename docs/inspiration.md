# Inspiration

## Library

This projects is inspired by the [forwardable](https://github.com/5long/forwardable) library, a "utility for easy object composition via delegation".

However I was looking for both more flexibility and more features. In particular:

- a clear separation between class definition and method forwarding;
- a validation step to make sure that changing something from the component doesn't break the class;
- the possibility to forward all the methods/attributes of a given component with a single instruction;
- the chance of adding prefix and/or suffix for each component;

Please refer to [Beyond the basics](user_guide/beyond_basics.md) page to see example usages.

## Docs

Documentation style is inspired by [FastAPI](https://fastapi.tiangolo.com/) amazing docs.
