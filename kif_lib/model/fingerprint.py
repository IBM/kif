# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable

from ..typing import cast, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable
from .snak import Snak
from .snak_set import SnakSet, TSnakSet
from .value import Entity, Property, Value

TFingerprint = Union['Fingerprint', Value, Snak, TSnakSet]
TEntityFingerprint = Union['EntityFingerprint', Entity, Snak, TSnakSet]
TPropertyFingerprint = Union['PropertyFingerprint', Property, Snak, TSnakSet]


class Fingerprint(KIF_Object):
    """Fingerprint.

    Parameters:
       arg1: Value or snak set.
    """

    @classmethod
    def _check_arg_fingerprint(
            cls,
            arg: TFingerprint,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Fingerprint', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, Value, Snak, SnakSet, Iterable),
            function, name, position))

    def __init__(self, arg1: TFingerprint):
        return super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
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
        """Fingerprint value."""
        return self.get_value()

    def get_value(self, default: Optional[Value] = None) -> Optional[Value]:
        """Gets fingerprint value.

        If fingerprint has no value, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Fingerprint value or `default` (fingerprint has no value).
        """
        val = self.args[0]
        return val if isinstance(val, Value) else default

    @property
    def snak_set(self) -> Optional[SnakSet]:
        """Fingerprint snak set."""
        return self.get_snak_set()

    def get_snak_set(
            self,
            default: Optional[SnakSet] = None
    ) -> Optional[SnakSet]:
        """Gets fingerprint snak set.

        If fingerprint has no snak set, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Fingerprint snak set or `default` (fingerprint has no snak set).
        """
        snaks = self.args[0]
        return snaks if isinstance(snaks, SnakSet) else default


class EntityFingerprint(Fingerprint):
    """Entity fingerprint.

    Parameters:
       arg1: Entity or snak set.
    """

    @classmethod
    def _check_arg_entity_fingerprint(
            cls,
            arg: TEntityFingerprint,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['EntityFingerprint', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, Entity, SnakSet, Iterable), function, name, position))

    def __init__(self, arg1: TEntityFingerprint):
        return super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, EntityFingerprint):
                return arg.args[0]
            elif isinstance(arg, Value):
                return self._preprocess_arg_entity(arg, i)
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            else:
                return self._preprocess_arg_snak_set(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def entity(self) -> Optional[Entity]:
        """Fingerprint entity."""
        return self.get_entity()

    def get_entity(
            self,
            default: Optional[Entity] = None
    ) -> Optional[Entity]:
        """Gets fingerprint entity.

        If fingerprint has no entity, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Fingerprint entity or `default` (fingerprint has no entity).
        """
        return cast(Optional[Entity], self.get_value(default))


class PropertyFingerprint(Fingerprint):
    """Property fingerprint.

    Parameters:
       arg1: Property or snak set.
    """

    @classmethod
    def _check_arg_property_fingerprint(
            cls,
            arg: TPropertyFingerprint,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['PropertyFingerprint', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, Property, SnakSet, Iterable),
            function, name, position))

    def __init__(self, arg1: TPropertyFingerprint):
        return super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, PropertyFingerprint):
                return arg.args[0]
            elif isinstance(arg, Value):
                return self._preprocess_arg_property(arg, i)
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            else:
                return self._preprocess_arg_snak_set(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def property(self) -> Optional[Property]:
        """Fingerprint property."""
        return self.get_property()

    def get_property(
            self,
            default: Optional[Property] = None
    ) -> Optional[Property]:
        """Gets fingerprint property.

        If fingerprint has no property, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Fingerprint property or `default` (fingerprint has no property).
        """
        return cast(Optional[Property], self.get_value(default))
