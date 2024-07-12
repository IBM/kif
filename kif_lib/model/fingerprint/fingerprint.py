# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import Any, Callable, Optional, override, Self, Set, Union
from ..kif_object import KIF_Object
from ..set import SnakSet, TSnakSet
from ..snak import Snak, TSnak
from ..value import TValue, Value

TFingerprint = Union['Fingerprint', TValue, TSnak, TSnakSet]


class Fingerprint(KIF_Object):
    """Fingerprint.

    Parameters:
       value_spec: Value or snak set.
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
        elif isinstance(arg, (Snak, SnakSet, Value)):
            return cls(arg)
        elif isinstance(arg, (list, tuple, Set)):
            return cls(SnakSet.check(
                arg, function or cls.check, name, position))
        else:
            return cls(Value.check(
                arg, function or cls.check, name, position))

    def __init__(self, value_spec: TFingerprint):
        super().__init__(value_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            if isinstance(arg, type(self_)):
                return arg[0]
            elif isinstance(arg, (SnakSet, Value)):
                return arg
            elif isinstance(arg, Snak):
                return SnakSet(arg)
            elif isinstance(arg, (list, tuple, Set)):
                return SnakSet.check(arg, type(self_), None, i)
            else:
                return Value.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

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
        value = self.args[0]
        return value if isinstance(value, Value) else default

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
