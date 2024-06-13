# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, cast, Iterable, Optional, override, Union
from .kif_object import TLocation
from .kif_object_set import KIF_ObjectSet
from .value import Text, Value

TFrozenset = frozenset
TTextSet = Union['TextSet', Iterable[Text]]
TValueSet = Union['ValueSet', Iterable[Value]]


class ValueSet(KIF_ObjectSet):
    """Set of values.

    Parameters:
       values: Values.
    """

    @classmethod
    def _check_arg_value_set(
            cls,
            arg: TValueSet,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'ValueSet':
        return cast(ValueSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._preprocess_arg_value(arg, i)

    @property
    @override
    def frozenset(self) -> TFrozenset[Value]:
        """The set of values as a frozen set."""
        return self.get_frozenset()

    @override
    def get_frozenset(self) -> TFrozenset[Value]:
        """Gets the set of values as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[Value], self._get_frozenset())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'ValueSet':
        """Computes the union of self and `others`.

        Parameters:
           others: Value sets.

        Returns:
           The resulting value set.
        """
        return cast(ValueSet, self._union(others))


class TextSet(ValueSet):
    """Set of texts.

    Parameters:
       texts: Texts.
    """

    @classmethod
    def _check_arg_text_set(
            cls,
            arg: TTextSet,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'TextSet':
        return cast(TextSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._preprocess_arg_text(arg, i)

    @property
    @override
    def frozenset(self) -> TFrozenset[Text]:
        """The set of texts as a frozen set."""
        return self.get_frozenset()

    @override
    def get_frozenset(self) -> TFrozenset[Text]:
        """Gets the set of texts as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[Text], self._get_frozenset())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'TextSet':
        """Computes the union of self and `others`.

        Parameters:
           others: Text sets.

        Returns:
           The resulting text set.
        """
        return cast(TextSet, self._union(others))
