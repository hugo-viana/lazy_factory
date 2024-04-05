from typing import Dict, List, Protocol, Type, runtime_checkable

import pytest

from lazy_factory import LazyFactory


# Setup tests


@runtime_checkable
class CarProtocol(Protocol):
    def drive(self) -> str:
        """Drive the car."""
        ...


class Sedan:
    def drive(self) -> str:
        """Drive the Sedan car.

        Returns:
            str: dummy test string.

        """
        return "Driving a sedan"


class SUV:
    def drive(self) -> str:
        """Drive the SUV car.

        Returns:
            str: dummy test string.

        """
        return "Driving an SUV"


class Hatchback:
    def drive(self) -> str:
        """Drive the Hatchback car.

        Returns:
            str: dummy test string.

        """
        return "Driving a Hatchback"


class LuxurySedan:
    def drive(self) -> str:
        """Drive the Luxury Sedan car.

        Returns:
            str: dummy test string.

        """
        return "Driving a Luxury Sedan"


car_types_dict: Dict[str, Type[CarProtocol]] = {
    "sedan": Sedan,
    "suv": SUV,
    "hatchback": Hatchback,
}

car_types_lst: List[Type[CarProtocol]] = [Sedan, SUV, Hatchback]


# Functional tests


def test_default_values() -> None:
    """Ensure basic initialization with default values."""
    dummy_factory = LazyFactory[CarProtocol]()  # Act

    assert dummy_factory.factory_items == {}
    assert dummy_factory.case_sensitive is True


def test_drive_result() -> None:
    """Ensure retrieved item works as expected."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)
    sedan_car = car_factory.get_item("sedan")()

    drive_msg = sedan_car.drive()  # Act

    assert drive_msg == "Driving a sedan"


def test_car_instance() -> None:
    """Ensure retrieved item is of expected class/type."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)

    sedan_car = car_factory.get_item("sedan")()  # Act

    assert isinstance(sedan_car, Sedan)


def test_protocol() -> None:
    """Ensure retrieved item is of expected protocol."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)

    sedan_cls = car_factory.get_item("sedan")  # Act

    assert issubclass(sedan_cls, CarProtocol)


def test_list_instead_of_dict() -> None:
    """Ensure classes are stored with their name in case a list is provided."""
    car_factory = LazyFactory[CarProtocol](car_types_lst)

    sedan_car = car_factory.get_item("Sedan")()  # Act

    assert isinstance(sedan_car, Sedan)


def test_already_exists_item() -> None:
    """Ensure existing items are not overwritten and an error is raised."""
    car_factory = LazyFactory[CarProtocol](car_types_lst)
    expected_err_msg = (
        "cannot register class Sedan because this factory "
        + "already has an item named Sedan"
    )

    with pytest.raises(ValueError) as exc_info:
        car_factory.register(Sedan)

    assert str(exc_info.value) == expected_err_msg


def test_init_with_case_sensitive_false() -> None:
    """Ensure item names are stored in uppercase."""
    expected_list = sorted(["SEDAN", "SUV", "HATCHBACK"])
    car_factory = LazyFactory[CarProtocol](
        car_types_dict,
        case_sensitive=False,
    )

    stored_list = sorted(car_factory.factory_items.keys())  # Act

    assert stored_list == expected_list


def test_get_item_with_case_sensitive_false() -> None:  # noqa: AAA01
    """Ensure case sensitivity doesn't affect the retrieval method."""
    car_factory = LazyFactory[CarProtocol](
        car_types_dict,
        case_sensitive=False,
    )
    sedan_car_1 = car_factory.get_item("sedan")
    sedan_car_2 = car_factory.get_item("SEDAN")
    sedan_car_3 = car_factory.get_item("SeDaN")

    assert sedan_car_1 is sedan_car_2 is sedan_car_3


def test_clear_factory() -> None:
    """Ensure clear() empties factory items."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)

    car_factory.clear()  # Act

    assert len(car_factory.factory_items) == 0


def test_single_register() -> None:
    """Ensure single register works as expected."""
    car_factory = LazyFactory[CarProtocol]({})

    car_factory.register(Sedan)  # Act

    assert len(car_factory.factory_items) == 1
    assert "Sedan" in car_factory.factory_items.keys()
    assert car_factory.factory_items["Sedan"] is Sedan


def test_remove_item() -> None:
    """Ensure remove item works as expected."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)
    original_len = len(car_factory.factory_items)

    car_factory.remove_item("sedan")  # Act

    assert len(car_factory.factory_items) == (original_len - 1)
    assert "sedan" not in car_factory.factory_items.keys()


def test_update_item() -> None:
    """Ensure removes and adds new item maintaining the same name/alias."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)
    original_len = len(car_factory.factory_items)

    car_factory.update_item("sedan", LuxurySedan)  # Act

    assert len(car_factory.factory_items) == original_len
    assert "sedan" in car_factory.factory_items.keys()
    assert car_factory.factory_items["sedan"] is LuxurySedan


def test_bulk_register_dict_error() -> None:
    """Ensure error when case unsensitive and similar names."""
    car_types_dict_dupl: Dict[str, Type[CarProtocol]] = {
        "sedan": Sedan,
        "SEDAN": LuxurySedan,
    }
    expected_err_msg = (
        "there are classes that have the same name with "
        + "different case-styles, and since factory case "
        + "sensitivity is disabled they cannot be registered"
    )

    with pytest.raises(ValueError) as exc_info:
        LazyFactory[CarProtocol](car_types_dict_dupl, case_sensitive=False)

    assert str(exc_info.value) == expected_err_msg


def test_bulk_register_lst_error() -> None:
    """Ensure error when duplicate names found in list."""
    SEDAN = Sedan  # noqa: N806
    car_types_lst_dupl: List[Type[CarProtocol]] = [Sedan, SEDAN]
    expected_err_msg = "there are duplicate classes in the provided items list"

    with pytest.raises(ValueError) as exc_info:
        LazyFactory[CarProtocol](car_types_lst_dupl)

    assert str(exc_info.value) == expected_err_msg


def test_check_item_exists_error() -> None:
    """Ensure error when item doesn't exist in factory."""
    car_factory = LazyFactory[CarProtocol](car_types_dict)
    expected_err_msg = "item bike is not registered in the current factory"

    with pytest.raises(ValueError) as exc_info:
        car_factory.check_item_exists("bike")

    assert str(exc_info.value) == expected_err_msg
