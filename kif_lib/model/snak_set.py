# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, Iterable, NoReturn, Optional, override, Union
from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet
from .snak import Snak

TSnakSet = Union['SnakSet', Iterable[Snak]]


class SnakSet(KIF_ObjectSet):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    @classmethod
    def _check_arg_snak_set(
            cls,
            arg: TSnakSet,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['SnakSet', NoReturn]:
        return cast(SnakSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    def __init__(self, *snaks: Snak):
        super().__init__(*snaks)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_snak(arg, i)

    @property
    @override
    def args_set(self) -> frozenset[Snak]:
        """The set of snaks as a frozen set."""
        return self.get_args_set()

    @override
    def get_args_set(self) -> frozenset[Snak]:
        """Gets the set of snaks as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[Snak], self._get_args_set())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'SnakSet':
        """Computes the union of self and `others`.

        Parameters:
           others: Snak sets.

        Returns:
           The resulting snak set.
        """
        return cast(SnakSet, self._union(others))
