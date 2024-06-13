# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, cast, Iterable, Optional, override, TypeAlias, Union
from .kif_object import TLocation
from .kif_object_set import KIF_ObjectSet
from .snak import Snak

TFrozenset = frozenset
TSnakSet: TypeAlias = Union['SnakSet', Iterable[Snak]]


class SnakSet(KIF_ObjectSet):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    @classmethod
    def _check_arg_snak_set(
            cls,
            arg: TSnakSet,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'SnakSet':
        return cast(SnakSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._preprocess_arg_snak(arg, i)

    @property
    @override
    def frozenset(self) -> TFrozenset[Snak]:
        """The set of snaks as a frozen set."""
        return self.get_frozenset()

    @override
    def get_frozenset(self) -> TFrozenset[Snak]:
        """Gets the set of snaks as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[Snak], self._get_frozenset())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'SnakSet':
        """Computes the union of self and `others`.

        Parameters:
           others: Snak sets.

        Returns:
           The resulting snak set.
        """
        return cast(SnakSet, self._union(others))
