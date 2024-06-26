---
title: Python Metaclass and It's Magic Methods
date: 2024-06-27
tags: ["python", "metaclass"]
---

Metaclasses are a very confusing and complicated topic in Python, at least for me. Everything seems clear when I read about this topic, but I forget it after a few days. So, I thought it would be better to blog about my understanding to ensure this concept always stays with me.

## What are metaclasses ?


A `metaclass` is simply a class of a class. In Python, everything is an object, including `class`. Python's built-in function `type` is responsible for creating new type objects, also known as classes, at runtime. You can verify this by checking the `type` of the `class` property.


```python
>> class A:
>>    pass
>> A.__class__
>> type
```

A type function when supplied with one argument, returns the type of the object which is nothing but its class. If you supply 3 arguments, it creates a new `type` i.e class at runtime.

```python
>> class A:
>>     pass
>> a = A()
>> type(a)
>> __main__.A
>> B = type(‘B’, (), {“a”: 2}) // name, bases, attributes
>> B.a
>> 2
```

You can see that a class definition is just syntactic sugar for a “type” call at runtime, which is invoked when the interpreter parses the class definition.

Python allows us to customize the class construction behavior by subclassing the “type” class and overriding certain magic methods, namely: “new,” “init,” “call,” and “prepare.” Once this custom metaclass is defined, we can have new classes use this metaclass by passing it as an argument in the class definition using the “metaclass” keyword.

Before we understand how the aforementioned magic methods work in the case of metaclasses, let's understand how they work in normal classes.

## Magic methods and their behaviour

Let's understand the order of method execution before we look at a simple example. The “__prepare__” method is only applicable when the class is a metaclass (explained later), so we will focus on the “__new__,” “__init__,” and “__call__” methods.

Each of the above methods receives the same arguments as the constructor, except for __call__.

### `__new__`
- It is called before an instance of a class is created, that is, when you try to instantiate a class.
- It is the first method invoked among the magic methods mentioned earlier.
- It is a static method where the first argument is the class whose object will be created. The rest are the arguments passed to the constructor.
- This method must return the created object; otherwise, “__init__” won’t be called next.

### `__init__`
- We are all familiar with this method call. It initializes the object.
- It is the second method called right after the “__new__” method call.
- It returns nothing.

### `__call__`
- This is invoked when an instance of the class is called as a function.
- It is typically needed when a function or service requires a callable object, probably needed when you want stateful functions.
- It receives the arguments that are supplied when the object is called.

## Magic methods in normal classe

Let's try to implement the “Singleton” class using the above magic methods. To ensure that only one instance of a class exists at any moment, we need to intercept the object creation step. Just before an object is created, we will check if the object already exists. If it does, we return that instance; otherwise, we create it, store it in a map, and return the object.

Here is an implementation:

```python
class Singleton:
    __instances = {}
    def __new__(cls, *args, **kwargs):
        # this check make that we don't create an object of Singleton.
        # we want this functionality to be subclassed.
        if cls is Singleton:
            raise ValueError(f"{cls} can't be instantied. Subclass it to create objects")
        
        if cls in cls.__instances:
            return cls.__instances[cls]
        
        cls.__instances[cls] = super().__new__(cls)
        return cls.__instances[cls]


class A(Singleton):
    pass
```

### Explaination

As explained before, for normal classes (which don't use a metaclass), the __new__ method is invoked just before an object is instantiated. This makes it a perfect place to keep the logic to avoid creating unnecessary objects and always reuse the object for the given class.

## Using meta class

Let's explore metaclasses by building an AbstractMetaclass that throws an error if a class does not define all required abstract methods. Unlike Python's built-in abstractmethod decorator and ABC class, our metaclass will enforce the abstract method requirements at the time the class is defined, rather than when an instance of the class is created.

### Key Concepts:

- __new__: Called right after the class definition is parsed and just before the class object is created. It receives the name, bases, and attributes of the class.
- __init__: Called right after the class object is created. It also receives the name, bases, and attributes of the class.
- __call__: Called when you try to instantiate an object of the class. It receives the same arguments as the class constructor.
- __prepare__: Customizes the class namespace. It returns a dictionary-like object to store class variables and functions.


### Implementation:

Let's implement AbstractMetaclass to enforce that all abstract methods are defined in subclasses:

```python
from abc import abstractmethod

# if you define methods on metaclass, they become classmethods of the class being created
# so define it outside
def get_abstract_methods(cls):
    seen = set()
    missing_implementation = []

    while isinstance(cls, AbstractMeta):
        for name, value in vars(cls).items():
            if name in seen:
                # this to make sure that we don't process the method defined in the parent class and if
                # it is already seen that means, the method is overriden.
                continue
            seen.add(name)

            if hasattr(value, "__isabstractmethod__"):
                missing_implementation.append(name)
            
        cls = cls.__mro__[1]
    
    return missing_implementation

class AbstractMeta(type):

    def __init__(cls, name, bases, attributes):
        # we want to catch the class early, if it does not adhere to the abstract class protocol
        # can't do it in "__new__" as we need access to its mro.

        # if the class directly inherits from AbstractClass, then the class defines the abstract methods
        # so no need to check for this class. For the rest we find AbstractClass in the class mro.
        if 'AbstractClass' not in [base.__qualname__ for base in bases]:
            abstract_methods = get_abstract_methods(cls)
            if abstract_methods:
                raise TypeError(f"no implementation for methods: {', '.join(abstract_methods)} in class {name}")
            
        # if all abstract methods are implemented then return the class object.
        return super().__init__(name, bases, attributes)


# convenience class
class AbstractClass(metaclass=AbstractMeta):
    pass

class Shape(AbstractClass):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Square(Shape):
    pass
```

I hope you now have a good understanding of what a metaclass is and how its magic methods work. Thank you for reading!
