"""Lazy Factory main module."""

from typing import Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union


T = TypeVar("T")


class LazyFactory(Generic[T]):
    """Lazy Factory class."""

    factory_items: Dict[str, Type[T]]
    case_sensitive: bool

    def __init__(
        self,
        items: Optional[  # noqa: TAE002
            Union[Dict[str, Type[T]], List[Type[T]]]
        ] = None,
        case_sensitive: bool = True,
    ) -> None:
        """Initialize factory object and store items (classes/types).

        Args:
            items: Optional. initial classes/types to be stored and later
                retrieved by the factory.
            case_sensitive: Optional. Whether the future retrieval of items by
                name should be or none case sensitive. Defaults to True.

        """
        self.factory_items = {}
        self.case_sensitive = case_sensitive
        self.clear()
        if items is not None:
            self.bulk_register(items)

    def _handle_naming(self, name: str) -> str:
        if self.case_sensitive is False:
            return name.upper()
        return name

    def get_item(self, name: str) -> Type[T]:
        """Retrieve factory item (class).

        Args:
            name: item name (class/type name).

        Returns:
            Type[T]: item (class/type) object (uninitialized).

        """
        name = self._handle_naming(name)
        self.check_item_exists(name)
        return self.factory_items[name]

    def register(self, item: Type[T], name: Optional[str] = None) -> None:
        """Register new factory item.

        Args:
            item: new factory item.
            name: Optional. New factory item name/alias. Defaults to None.

        """
        name, item = self._pre_register(item, name)
        self._register(name, item)

    def bulk_register(
        self,
        items: Union[Dict[str, Type[T]], List[Type[T]]],  # noqa: TAE002
    ) -> None:
        """Bulk-Register new factory items.

        Args:
            items: classes/types to be stored and later retrieved by
                the factory.

        """
        # Ensure all new items pass the pre-register validations
        if isinstance(items, list):
            valid_items = self._bulk_register_lst(items)
        else:  # dict
            valid_items = self._bulk_register_dict(items)
        # Register validated items
        for item in valid_items:
            self._register(item[0], item[1])

    def _bulk_register_dict(
        self,
        items: Dict[str, Type[T]],
    ) -> List[Tuple[str, Type[T]]]:  # noqa: TAE002
        """Bulk-Register new factory items.

        Args:
            items: classes/types to be stored and later retrieved by
                the factory.

        Returns:
            List[Tuple[str, Type[T]]]: list of items (name and item tuples).

        Raises:
            ValueError: there are classes with the same  name (but in different
                case-styles) and case sensitivity is disabled for this factory
                instance.

        """
        # Ensure all new items pass the pre-register validations
        if self.case_sensitive is False:
            keys_upper = [self._handle_naming(k) for k in items.keys()]
            if len(keys_upper) > len(list(set(keys_upper))):
                raise ValueError(
                    "there are classes that have the same name with "
                    + "different case-styles, and since factory case "
                    + "sensitivity is disabled they cannot be registered",
                )
        # Return validated items
        return [self._pre_register(v, k) for k, v in items.items()]

    def _bulk_register_lst(
        self,
        items: List[Type[T]],
    ) -> List[Tuple[str, Type[T]]]:  # noqa: TAE002
        """Bulk-Register new factory items.

        Args:
            items: classes/types to be stored and later retrieved by
                the factory.

        Returns:
            List[Tuple[str, Type[T]]]: list of items (name and item tuples).

        Raises:
            ValueError: if there are duplicates on the provided list of items.

        """
        # Ensure all new items pass the pre-register validations
        if len(items) > len(list(set(items))):
            raise ValueError(
                "there are duplicate classes in the provided items list",
            )
        # Return validated items
        return [self._pre_register(item) for item in items]

    def _pre_register(
        self,
        item: Type[T],
        name: Optional[str] = None,
    ) -> Tuple[str, Type[T]]:
        """Perform pre-register validations.

        Args:
            item: new factory item.
            name: Optional. New factory item name/alias. Defaults to None.

        Raises:
            ValueError: item already exists.

        Returns:
            Tuple[str, Type[T]]: new item name and class/type.

        """
        if name is None:
            name = item.__name__
        name = self._handle_naming(name)
        if self.check_item_exists(name, raise_error=False) is True:
            raise ValueError(
                f"cannot register class {item.__name__} because this factory "
                + f"already has an item named {name}",
            )
        return name, item

    def _register(self, name: str, item: Type[T]) -> None:
        """Register new factory item.

        Args:
            name: new factory item name/alias.
            item: new factory item.

        """
        self.factory_items[name] = item

    def remove_item(self, name: str) -> None:
        """Remove item from factory.

        Args:
            name: item name/alias.

        """
        name = self._handle_naming(name)
        self.check_item_exists(name)
        del self.factory_items[name]

    def check_item_exists(self, name: str, raise_error: bool = True) -> bool:
        """Check if an item exists in the current factory.

        Args:
            name: item name/alias.
            raise_error: if True will raise an error if item doesn't exist in
                factory. If false it will return a boolean True if it exists,
                or a boolean False if it doesn't exist.

        Returns:
            bool: True if exists. False otherwise.

        Raises:
            ValueError: in case item is not registered in the current factory.

        """
        if name not in self.factory_items.keys():
            if raise_error is False:
                return False
            raise ValueError(
                f"item {name} is not registered in the current factory",
            )
        return True

    def clear(self) -> None:
        """Clear (remove all) factory items."""
        self.factory_items.clear()

    def update_item(self, name: str, new_item: Type[T]) -> None:
        """Update a factory item.

        Args:
            name: existing factory item name/alias.
            new_item: new factory item.

        """
        self.remove_item(name)
        self.register(new_item, name)
