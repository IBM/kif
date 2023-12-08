# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Collection, Iterable
from typing import cast, NoReturn, Optional, Union

from .kif_object import KIF_Object, TCallable

T_KIF_ObjectSet = Union['KIF_ObjectSet', Iterable[KIF_Object]]


class KIF_ObjectSet(KIF_Object):
    """Set of KIF objects.

    Parameters:
       args: objects.
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
        '_args_set',
    )

    _args_set: frozenset[KIF_Object]

    def __init__(self, *args: KIF_Object):
        super().__init__(*args)

    def _set_args(self, args):
        self._args_set = frozenset(args)
        self._args = tuple(sorted(self._args_set))

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_kif_object(arg, i)

    def __contains__(self, v):
        return v in self._args_set if KIF_Object.test(v) else False

    def _get_args_set(self) -> frozenset[KIF_Object]:
        return self._args_set

    def _union(self, others: Collection['KIF_ObjectSet']) -> 'KIF_ObjectSet':
        return self.__class__(*self._args_set.union(*map(
            KIF_ObjectSet._get_args_set, others)))
