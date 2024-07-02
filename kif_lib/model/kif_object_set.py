# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import (
    Any,
    Callable,
    ClassVar,
    Iterable,
    Optional,
    override,
    Self,
    Union,
)
from .kif_object import KIF_Object

T_KIF_ObjectSet = Union['KIF_ObjectSet', Iterable[KIF_Object]]


class KIF_ObjectSet(KIF_Object):
    """Set of KIF objects.

    Parameters:
       objects: KIF objects.
    """

    children_class: ClassVar[type[KIF_Object]] = KIF_Object  # pyright: ignore

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'children_class' in kwargs:
            cls.children_class = kwargs['children_class']
            assert issubclass(cls.children_class, KIF_Object)

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
        elif not isinstance(arg, KIF_Object) and isinstance(arg, Iterable):
            return cls(*map(
                lambda x: cls.children_class.check(
                    x, function or cls.check, name, position), arg))
        else:
            raise cls._check_error(arg, function, name, position)

    __slots__ = (
        '_frozenset',
    )

    _frozenset: frozenset[KIF_Object]

    @override
    def __init__(self, *objects: KIF_Object):
        super().__init__(*objects)

    @override
    def _set_args(self, args: tuple[Any, ...]):
        self._frozenset = frozenset(args)
        self._args = tuple(sorted(self._frozenset))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self.children_class.check(arg, type(self), None, i)

    def __contains__(self, v: Any) -> bool:
        if isinstance(v, self.children_class):
            return v in self._frozenset
        else:
            return False

    def _get_frozenset(self) -> frozenset[KIF_Object]:
        return self._frozenset

    def union(self, *others: Self) -> Self:
        """Computes the union of self and `others`.

        Parameters:
           others: KIF object sets.

        Returns:
           The resulting KIF object set.
        """
        return self.__class__(*self._frozenset.union(*map(
            lambda s: s._frozenset, others)))
