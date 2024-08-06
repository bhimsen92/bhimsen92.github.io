---
title: 'How To Learn New Programming Language Quickly'
date: 2023-01-27
tags:
  - programming-language
---

Our job requires us to learn new programming languages once in a while. Some languages are easy while others have steep learning curve. I would have wished if there was a templte for learning languages because each language has similar concepts but with different syntax. Once you understand what is common between the language you know and the language you want to learn, all that is left is to master the syntax which comes with some practice. This document tries to encapsulate all that for the scala language and later use it to learn both Python, Rust and Java.

This document expects the reader to know at least one programming language and have some idea of what OOP(Object Oriented Programming) and Function Programming means.

What is a programming language ? Though I don’t know the textbook definition, in my opinion a programming language is a system(of notations) which has facilities to represent real world entities and manipulate them using predefined or custom operations to produce a result.

Based on the above definition, it is very easy to deduce that every programming language should have few things or sometime more in common. So first we list down all things that are common between languages. Later we will diverge based on whether the language is an OO(object oriented) or functional language.

## Language Learning Template

1. Build and Dependency management: How to build and load dependencies for your project.
2. Primitive data types to represent real world data. Real world is made up of numbers and characters(strings).
3. Operations.
4. Custom data types to represent complex real world entities. From here onwards called objects.
5. Ways to define variables and constants.
6. Constructs for looping and branching.
7. Functions or methods to encapsulate a block of code or steps.
8. Modules or packages or namespaces to organise code into logical groups.
9. Collections or data structures to simplify programming.

### If the language supports object oriented programming then it should have:

10. Classes and objects to represent real world entities.
11. Inheritance: A way to create new classes using existing classes.
12. Interface: A technique to build abstractions. It allows you to define operations or methods without their implementation. [not all languages support this feature]
13. Multiple Inheritance. [not all languages support this feature]

### If the language is Functional language:

14. Supports functions as first class objects. That is, there is no difference between regular values and functions. They can be assigned, passed to functions and can be returned from functions.
15. As a consequence of the above statement, support for Higher order functions.
16. Closure.
17. Immutable data structures or a way to define immutable values.
18. Tail recursion.

### Threading and Multi Process computations:

19. Ability to create threads and handle concurrent computation.
20. Locks and other ways to protect critical sections of the code.
21. Support for asynchronous programming.

In the upcoming posts, we will use the above template to learn Scala, Go, Rust and Java.