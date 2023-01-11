# Why Composition

## TL;DR

Overall, composition is a more flexible and transparent way to reuse code and design classes in Python. It allows to build classes that are customized to your specific needs, and it promotes code reuse and modularity.

## Composition over Inheritance

There are a few reasons why composition is generally preferred over inheritance in Python. Here a short list.

### Flexibility

Composition allows us to choose exactly which methods and attributes we want to include in our class, whereas inheritance requires to inherit the entire interface of the parent class. This allows us to design classes in a way that is tailored to specific needs.

### Transparency

When using inheritance, it can be difficult to understand how a class is behaving, because it may be using methods and attributes from multiple ancestor classes.

With composition, the behavior of a class is more transparent, as it is clear which methods and attributes are being used and from where they come from exactly.

### Maintainability

Inheritance can lead to complex class hierarchies and dependencies, which can make it difficult to maintain and modify the code.

Composition, on the other hand, is easier to maintain since allows us to build classes using simple, independent components that are easy to understand and modify.

### Code reuse

Composition promotes code reuse: instead of inheriting from a parent class and modifying its behavior, you can use composition to reuse code by encapsulating it in a separate class and composing it into your new class. This can make your code more modular and easier to reuse.

## Rule of Thumb

Overall, we can say that composition is a more flexible and transparent than inheritance. This doesn't mean that we should never use inheritance.

As a rule of thumb, one can think to:

- Use **composition** if object `A` *has a* relationship with object `B` (e.g. a square has a side).
- Use **inheritance** if object `A` *is a* specification of object `B` (e.g. a square is a shape).

One of the most common *drawback* of using composition is *exactly* the fact that methods/attributes provided by single components may have to be implemented again.

## Resources/References

There are many resources where one can get a better understanding of why and when to prefer composition over inheritance:

- [Wikipedia page](https://en.wikipedia.org/wiki/Composition_over_inheritance)
- [Stack overflow discussion](https://stackoverflow.com/questions/49002/prefer-composition-over-inheritance)
- [The perils of inheritance - by Ariel Ortiz](https://www.youtube.com/watch?v=YXiaWtc0cgE&list=WL&index=1)
