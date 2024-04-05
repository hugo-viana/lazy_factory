# :factory: lazy_factory
Lazy Factory Generic Class for simple Factory Pattern usages in **Python**.

If you're new to the design patterns concepts (like the Factory method) just visit one of my favorite websites: [Refactoring Guru](https://refactoring.guru)


# :question: What's a Lazy Factory?

A lazy factory, is a factory that returns classes/types instead of an initialized class object.

Normally the standard behavior for factory classes is to return an initialized object, but in several projects i've work on, there are many times when you need to defer the initialization process to later on, or you need to specify different initialization arguments for different factories. This way, instead of having to design/code a new factory class every time you need one (and do all the testing, docstrings, type-checking, etc), you can just use the LazyFactory generic class of this library.


# :anchor: Installation

As simple as it comes:

```
pip install lazy_factory
```


# :arrow_forward: Usage

## :wink: Basic Usage

Let's see how we can use this lazy factory with an example:

1. Suppose you have 3 types of cars (Sedan, SUV and Hatchback) that follow a specific protocol (for this example let's work with just a simple 'drive' method):

    ```python
    class CarProtocol(Protocol):
        def drive(self) -> str:
            ...


    class Sedan:
        def drive(self) -> str:
            return "Driving a sedan"


    class SUV:
        def drive(self) -> str:
            return "Driving an SUV"


    class Hatchback:
        def drive(self) -> str:
            return "Driving a Hatchback"
    ```

1. In order to store them in a factory just initialize a new `LazyFactory` object with the factory items an their names/aliases (in a dict-form):

    ```python
    from lazy_factory import LazyFactory

    car_types: Dict[str, Type[CarProtocol]] = {
        "sedan": Sedan,
        "suv": SUV,
        "hatchback": Hatchback,
    }

    car_factory = LazyFactory[CarProtocol](car_types)
    ```

    If you don't need/want to setup names/aliases for your classes, just put them in a list and LazyFactory will store them with their class name:

    ```python
    from lazy_factory import LazyFactory

    car_types: List[Type[CarProtocol]] = [Sedan, SUV, Hatchback]

    car_factory = LazyFactory[CarProtocol](car_types)
    ```

    :sparkles: Note 1: we initialized the LazyFactory object enforcing the type `CarProtocol` like `LazyFactory[CarProtocol](...)` so that type-checkers (like **mypy**) know the type of items the factory returns. If you don't use type-check (you're a very naughty boy) you can just initialize it without specifying any type `LazyFactory(...)`. And the same goes for the car_types dict or list, instead of `car_types: Dict[str, Type[CarProtocol]] = {...}` or `car_types: List[Type[CarProtocol]] = [...]` you can just use `car_types = {...}` or `car_types = [...]`.

    :sparkles: Note 2: Althougth it is not the must common scenario, you can initialize the `LazyFactory` without any factory items, but in this case you would have to add them later on using the `register()` and/or `bulk_register()` methods (see details further down on this docs).

1. And to access a specific car class in your code, just call the `get_item()` method of your factory with the name/alias set previously:

    ```python
    sedan_car_cls = car_factory.get_item("sedan")
    ```

    And when you need to initialize your sedan car object just do it:
    ```python
    sedan_car = sedan_car_cls(...)
    ```

    or you can do it all in the same step, if you prefer:
    ```python
    sedan_car = car_factory.get_item("sedan")(...)
    ```

## :zap: Advanced Usage (additional options and methods)

### :zap: Handle case sensitivity in names/aliases of stored factory items

If you don't want to worry about case sentitivity in names/aliases of stored factory items you can turn it off during initialization.

Back to our example, with `case_sensitive=False` "sedan", "SEDAN", or "SeDaN" will al retrieve the same item: the `Sedan` class:

```python
car_factory = LazyFactory[CarProtocol](
    car_types,
    case_sensitive=False,
)

sedan_car_1 = car_factory.get_item("sedan")
sedan_car_2 = car_factory.get_item("SEDAN")
sedan_car_3 = car_factory.get_item("SeDaN")

assert sedan_car_1 is sedan_car_2 is sedan_car_3
```

### :zap: Check if an item exists in the factory

If you need to check if an item already exists in the current factory, you'll have to use the `check_item_exists()` method:

```python
car_factory.check_item_exists("sedan")
```

By default it will return True if the item exists, and in case it doesn't exist it will raise a `ValueError`.

If you don't want to implement any error handling on your side of the code, you can disable the error raising by setting and optional argument `raise_error=False` and it will return a boolean result (True if it exists, and False otherwise):

```python
car_factory.check_item_exists("sedan", raise_error=False)
```


### :zap: Register additional factory items (after initialization)

#### Individual item

Imagine you have a new car type (a luxury sedan) you want to add as a new factory item (assuming you cannot register it at initialization):

```python
class LuxurySedan:
    def drive(self) -> str:
        """Drive the Sedan car.

        Returns:
            str: dummy test string.

        """
        return "Driving a luxury sedan"
```

Just call the `register()` method providing a name/alias:

```python
car_factory.register(LuxurySedan, "luxury")
```

or without name/alias:

```python
car_factory.register(LuxurySedan)
```

#### Several items

If you need to add several items to the factory, you can always add them one by one using the `register()` method, but you can also add them all at once (in bulk) using the `bulk_register()` method:

```python
car_factory.bulk_register(car_types)
```

The `bulk_register()` method accepts either a dict or a list (just like at initialization).

### :zap: Remove a factory item

To remove a specific factory item from "storage" just call the `remove_item()` method passing along the item name/alias:

```python
car_factory.remove_item("sedan")
```

### :zap: Clear (remove all) factory items

If for some reason you need to remove all factory items from "storage" just call the `clear()` method:

```python
car_factory.clear()
```

### :zap: Change/Update a factory item

If you need to update an item in your factory, just call the `update_item()` method passing the existing item name/alias and the new item class/type.

For example, you have registered the `Sedan` class as `sedan` and now you want to change it to the `LuxurySedan` class.

```python
car_factory.update_item("sedan", LuxurySedan)
```


# :rocket: Library Development

## Setup development

Clone repo, create a new virtual environment, activate it and install development requirements:

```
pip install -r requirements_dev.txt
```

## CQA (Code Quality Assurance)

Every commit must be checked with flake8, mypy and pytest with coverage:

```
flake8
```

```
mypy .
```

```
pytest --cov
```

## Build and distribute a new version

**Build package:**

```
py -m build
```

**Publish new version to test PyPi:**

```
py -m twine upload --repository testpypi dist/*
```

**Publish new version to PyPi (production):**

```
py -m twine upload dist/*
```
