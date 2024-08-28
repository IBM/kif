# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import (
    Any,
    cast,
    ClassVar,
    Generic,
    Iterable,
    Location,
    override,
    Self,
    TypeAlias,
    TypeVar,
    Union,
)
from .kif_object import KIF_Object
from .snak import Snak, TSnak
from .value import Text, TText, TValue, Value

TValueSet: TypeAlias = Union['ValueSet', Iterable[TValue]]

TTextSet: TypeAlias = Union['TextSet', Iterable[TText]]

TSnakSet: TypeAlias = Union['SnakSet', Iterable[TSnak]]

TReferenceRecord: TypeAlias = Union['ReferenceRecord', TSnakSet]

TReferenceRecordSet: TypeAlias =\
    Union['ReferenceRecordSet', Iterable[TReferenceRecord]]

_TObj = TypeVar('_TObj', bound=KIF_Object)


class KIF_ObjectSet(KIF_Object, Generic[_TObj]):
    """Set of KIF objects.

    Parameters:
       objects: KIF objects.
    """

    children_class: ClassVar[type[KIF_Object]]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        if 'children_class' in kwargs:
            cls.children_class = kwargs['children_class']
            assert issubclass(cls.children_class, KIF_Object)

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif not isinstance(arg, KIF_Object) and isinstance(arg, Iterable):
            return cls(*map(
                lambda x: cast(_TObj, cls.children_class.check(
                    x, function or cls.check, name, position)), arg))
        else:
            raise cls._check_error(arg, function, name, position)

    __slots__ = (
        '_frozenset',
    )

    _frozenset: frozenset[_TObj]

    @override
    def _set_args(self, args: tuple[Any, ...]) -> None:
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

    def union(self, *others: Self) -> Self:
        """Computes the union of self and `others`.

        Parameters:
           others: KIF object sets.

        Returns:
           The resulting KIF object set.
        """
        return self.__class__(*self._frozenset.union(*map(
            lambda x: x._frozenset, others)))


class ValueSet(KIF_ObjectSet[Value], children_class=Value):
    """Set of values.

    Parameters:
       values: Values.
    """

    children_class: ClassVar[type[Value]]  # pyright: ignore

    @override
    def __init__(self, *values: TValue) -> None:
        super().__init__(*values)


class TextSet(ValueSet, children_class=Text):
    """Set of texts.

    Parameters:
       texts: Texts.
    """

    children_class: ClassVar[type[Text]]  # pyright: ignore

    @override
    def __init__(self, *texts: TText) -> None:
        super().__init__(*texts)


class SnakSet(KIF_ObjectSet[Snak], children_class=Snak):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    children_class: ClassVar[type[Snak]]  # pyright: ignore

    @override
    def __init__(self, *snaks: Snak) -> None:
        super().__init__(*snaks)


class ReferenceRecord(SnakSet, children_class=Snak):
    """Reference record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, SnakSet):
            return cls(*arg)
        else:
            return super().check(arg, function, name, position)


class ReferenceRecordSet(
        KIF_ObjectSet[ReferenceRecord],
        children_class=ReferenceRecord
):
    """Set of reference records.

    Parameters:
       reference_records: Reference records.
    """

    children_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore

    @override
    def __init__(self, *reference_records: TReferenceRecord) -> None:
        super().__init__(*reference_records)
