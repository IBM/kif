# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, Iterable, NoReturn, Optional, override, Union
from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet
from .value import Text

TTextSet = Union['TextSet', Iterable[Text]]


class TextSet(KIF_ObjectSet):
    """Set of texts.

    Parameters:
       texts: Texts.
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

    def __init__(self, *texts: Text):
        super().__init__(*texts)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_text(arg, i)

    @property
    def args_set(self) -> frozenset[Text]:
        """The set of texts as a frozen set."""
        return self.get_args_set()

    @override
    def get_args_set(self) -> frozenset[Text]:
        """Gets the set of texts as a frozen set.

        Returns:
           Frozen set
        """
        return cast(frozenset[Text], self._get_args_set())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'TextSet':
        """Computes the union of self and `others`.

        Parameters:
           others: Text sets.

        Returns:
           The resulting text set.
        """
        return cast(TextSet, self._union(others))
