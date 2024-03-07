# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, Collection, Iterable, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable

T_KIF_ObjectSet = Union['KIF_ObjectSet', Iterable[KIF_Object]]
TFrozenset = frozenset


class KIF_ObjectSet(KIF_Object):
    """Set of KIF objects.

    Parameters:
       objects: KIF objects.
    """

    @classmethod
    def _check_arg_kif_object_set(
            cls,
            arg: T_KIF_ObjectSet,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['KIF_ObjectSet', NoReturn]:
        if not KIF_Object.test(arg) and isinstance(arg, Iterable):
            arg = cls(*arg)
        return cast(KIF_ObjectSet, cls._check_arg_isinstance(
            arg, KIF_ObjectSet, function, name, position))

    __slots__ = (
        '_frozenset',
    )

    _frozenset: frozenset[KIF_Object]

    def __init__(self, *objects: KIF_Object):
        super().__init__(*objects)

    def _set_args(self, args):
        self._frozenset = frozenset(args)
        self._args = tuple(sorted(self._frozenset))

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_kif_object(arg, i)

    def __contains__(self, v):
        return v in self._frozenset if KIF_Object.test(v) else False

    def _get_frozenset(self) -> TFrozenset[KIF_Object]:
        return self._frozenset

    def _union(self, others: Collection['KIF_ObjectSet']) -> 'KIF_ObjectSet':
        return self.__class__(*self._frozenset.union(*map(
            KIF_ObjectSet._get_frozenset, others)))

    @property
    def frozenset(self) -> TFrozenset[KIF_Object]:
        """The set of KIF objects as a frozen set."""
        return self.get_frozenset()

    def get_frozenset(self) -> TFrozenset[KIF_Object]:
        """Gets the set of KIF objects as a frozen set.

        Returns:
           Frozen set.
        """
        return self._get_frozenset()

    def union(self, *others: 'KIF_ObjectSet') -> 'KIF_ObjectSet':
        """Computes the union of self and `others`.

        Parameters:
           others: KIF object sets.

        Returns:
           The resulting KIF object set.
        """
        return self._union(others)
