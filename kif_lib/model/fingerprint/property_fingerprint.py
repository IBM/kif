# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import Any, Callable, cast, Optional, override, Self, Union
from ..set import TSnakSet
from ..snak import TSnak
from ..value import Property, TProperty, Value
from .entity_fingerprint import EntityFingerprint
from .fingerprint import Fingerprint

TPropertyFingerprint = Union['PropertyFingerprint', TProperty, TSnak, TSnakSet]


class PropertyFingerprint(EntityFingerprint):
    """Property fingerprint.

    Parameters:
       property_spec: Property or snak set.
    """

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        else:
            fp = Fingerprint.check(
                arg, function or cls.check, name, position)
            if isinstance(fp[0], Value):
                return cls(Property.check(
                    fp[0], function or cls.check, name, position))
            else:
                return cls(fp[0])

    def __init__(self, property_spec: TPropertyFingerprint):
        super().__init__(property_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            arg = Fingerprint._static_preprocess_arg(self, arg, i)
            if isinstance(arg, Value):
                return Property.check(arg, type(self), None, i)
            else:
                return arg
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
        return cast(Optional[Property], self.get_entity(default))
