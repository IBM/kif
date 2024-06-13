# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable

from ..typing import Any, cast, Optional, override, Union
from .kif_object import KIF_Object, TLocation
from .snak import Snak
from .snak_set import SnakSet, TSnakSet
from .value import Entity, Property, Value

TFingerprint = Union['Fingerprint', Value, Snak, TSnakSet]
TEntityFingerprint = Union['EntityFingerprint', Entity, Snak, TSnakSet]
TPropertyFingerprint = Union['PropertyFingerprint', Property, Snak, TSnakSet]


class Fingerprint(KIF_Object):
    """Fingerprint.

    Parameters:
       value_spec: Value or snak set.
    """

    @classmethod
    def _check_arg_fingerprint(
            cls,
            arg: TFingerprint,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Fingerprint':
        return cls(cls._check_arg_isinstance(
            arg, (cls, Value, Snak, SnakSet, Iterable),
            function, name, position))

    def __init__(self, value_spec: TFingerprint):
        super().__init__(value_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            if isinstance(arg, Fingerprint):
                return arg.args[0]
            elif isinstance(arg, Value):
                return arg
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            else:
                return self._preprocess_arg_snak_set(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def value(self) -> Optional[Value]:
        """The value of fingerprint."""
        return self.get_value()

    def get_value(self, default: Optional[Value] = None) -> Optional[Value]:
        """Gets the value of fingerprint.

        If the value is ``None``, returns `default`.

        Parameters:
           default: Default value.

        Returns:
           Value.
        """
        val = self.args[0]
        return val if isinstance(val, Value) else default

    @property
    def snak_set(self) -> Optional[SnakSet]:
        """The snak set of fingerprint."""
        return self.get_snak_set()

    def get_snak_set(
            self,
            default: Optional[SnakSet] = None
    ) -> Optional[SnakSet]:
        """Gets the snak set of fingerprint.

        If the snak set is ``None``, returns `default`.

        Parameters:
           default: Default snak set.

        Returns:
           Snak set.
        """
        snaks = self.args[0]
        return snaks if isinstance(snaks, SnakSet) else default


class EntityFingerprint(Fingerprint):
    """Entity fingerprint.

    Parameters:
       entity_spec: Entity or snak set.
    """

    @classmethod
    def _check_arg_entity_fingerprint(
            cls,
            arg: TEntityFingerprint,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'EntityFingerprint':
        return cls(cls._check_arg_isinstance(
            arg, (cls, Entity, SnakSet, Iterable), function, name, position))

    def __init__(self, entity_spec: TEntityFingerprint):
        super().__init__(entity_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            if isinstance(arg, EntityFingerprint):
                return arg.args[0]
            elif isinstance(arg, Value):
                return self._preprocess_arg_entity(cast(Entity, arg), i)
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            else:
                return self._preprocess_arg_snak_set(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def entity(self) -> Optional[Entity]:
        """The entity of fingerprint."""
        return self.get_entity()

    def get_entity(
            self,
            default: Optional[Entity] = None
    ) -> Optional[Entity]:
        """Gets the entity of fingerprint.

        If the entity is ``None``, returns `default`.

        Parameters:
           default: Default entity.

        Returns:
           Entity.
        """
        return cast(Optional[Entity], self.get_value(default))


class PropertyFingerprint(Fingerprint):
    """Property fingerprint.

    Parameters:
       property_spec: Property or snak set.
    """

    @classmethod
    def _check_arg_property_fingerprint(
            cls,
            arg: TPropertyFingerprint,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'PropertyFingerprint':
        return cls(cls._check_arg_isinstance(
            arg, (cls, Property, SnakSet, Iterable),
            function, name, position))

    def __init__(self, property_spec: TPropertyFingerprint):
        super().__init__(property_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            if isinstance(arg, PropertyFingerprint):
                return arg.args[0]
            elif isinstance(arg, Value):
                return self._preprocess_arg_property(cast(Property, arg), i)
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            else:
                return self._preprocess_arg_snak_set(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def property(self) -> Optional[Property]:
        """The property of fingerprint."""
        return self.get_property()

    def get_property(
            self,
            default: Optional[Property] = None
    ) -> Optional[Property]:
        """Gets the property of fingerprint.

        If the property is ``None``, returns `default`.

        Parameters:
           default: Default property.

        Returns:
           Property.
        """
        return cast(Optional[Property], self.get_value(default))
