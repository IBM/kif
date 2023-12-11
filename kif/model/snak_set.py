# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable
from typing import cast, NoReturn, Optional, Union

from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet
from .snak import Snak

TSnakSet = Union['SnakSet', Iterable[Snak]]


class SnakSet(KIF_ObjectSet):
    """Set of snaks.

    Parameters:
       args: Snaks.
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

    def __init__(self, *args: Snak):
        super().__init__(*args)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_snak(arg, i)

    @property
    def args_set(self) -> frozenset[Snak]:
        """Set arguments as frozen set."""
        return self.get_args_set()

    def get_args_set(self) -> frozenset[Snak]:
        """Gets set arguments as frozen set.

        Returns:
           Set arguments as set.
        """
        return cast(frozenset[Snak], self._get_args_set())

    def union(self, *others: 'SnakSet') -> 'SnakSet':
        """Computes the union of set and `others`.

        Parameters:
           others: Snak sets.

        Returns:
           The resulting snak set.
        """
        return cast(SnakSet, self._union(others))
