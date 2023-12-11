# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable
from typing import cast, NoReturn, Optional, Union

from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet
from .value import Text

TTextSet = Union['TextSet', Iterable[Text]]


class TextSet(KIF_ObjectSet):
    """Set of texts.

    Parameters:
       args: Texts.
    """

    @classmethod
    def _check_arg_text_set(
            cls,
            arg: TTextSet,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['TextSet', NoReturn]:
        return cast(TextSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    def __init__(self, *args: Text):
        super().__init__(*args)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_text(arg, i)

    @property
    def args_set(self) -> frozenset[Text]:
        """Set arguments as frozen set."""
        return self.get_args_set()

    def get_args_set(self) -> frozenset[Text]:
        """Gets set arguments as frozen set.

        Returns:
           Set arguments as set.
        """
        return cast(frozenset[Text], self._get_args_set())

    def union(self, *others: 'TextSet') -> 'TextSet':
        """Computes the union of set and `others`.

        Parameters:
           others: Text sets.

        Returns:
           The resulting text set.
        """
        return cast(TextSet, self._union(others))
