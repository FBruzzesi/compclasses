<img src="img/compclass-logo.svg" width=180 height=180 align="right">

# Compclasses

Like *dataclasses*, but for composition.

As the Gang of Four (probably) said:

> favor object composition over class inheritance.

However when we use composition in Python, we cannot access methods directly from the composed class.

This codebase wants to address such issue and make it easy to do so, by injecting the desired methods in the new class.
