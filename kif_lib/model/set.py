# Copyright (C) 2024-2025 IBM Corp.
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
from .snak import Snak, TSnak
from .term import ClosedTerm, Variable

TSnakSet: TypeAlias = Union['SnakSet', Iterable[TSnak]]
VSnakSet: TypeAlias = Union['SnakSetVariable', 'SnakSet']
VTSnakSet: TypeAlias = Union[Variable, VSnakSet, TSnakSet]

TQualifierRecord: TypeAlias = Union['QualifierRecord', TSnakSet]
VQualifierRecord: TypeAlias =\
    Union['QualifierRecordVariable', 'QualifierRecord']
VTQualifierRecord: TypeAlias =\
    Union[Variable, VQualifierRecord, TQualifierRecord]

TReferenceRecord: TypeAlias = Union['ReferenceRecord', TSnakSet]
VReferenceRecord: TypeAlias =\
    Union['ReferenceRecordVariable', 'ReferenceRecord']
VTReferenceRecord: TypeAlias =\
    Union[Variable, VReferenceRecord, TReferenceRecord]

TReferenceRecordSet: TypeAlias =\
    Union['ReferenceRecordSet', Iterable[TReferenceRecord]]
VReferenceRecordSet: TypeAlias =\
    Union['ReferenceRecordSetVariable', 'ReferenceRecordSet']
VTReferenceRecordSet: TypeAlias =\
    Union[Variable, VReferenceRecordSet, TReferenceRecordSet]

_TClosedTerm = TypeVar('_TClosedTerm', bound=ClosedTerm)


class ClosedTermSet(ClosedTerm, Generic[_TClosedTerm]):
    """Set of closed terms.

    Parameters:
       child: Closed term.
    """

    children_class: ClassVar[type[ClosedTerm]]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        if 'children_class' in kwargs:
            cls.children_class = kwargs['children_class']
            assert issubclass(cls.children_class, ClosedTerm)
        super().__init_subclass__(**kwargs)

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
        elif not isinstance(arg, ClosedTerm) and isinstance(arg, Iterable):
            return cls(*map(
                lambda x: cast(_TClosedTerm, cls.children_class.check(
                    x, function or cls.check, name, position)), arg))
        else:
            raise cls._check_error(arg, function, name, position)

    __slots__ = (
        '_frozenset',
    )

    _frozenset: frozenset[_TClosedTerm]

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

    def issubset(self, other: Self) -> bool:
        """Tests whether self is a subset of `other`.

        Parameters:
           other: Closed-term set.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._frozenset.issubset(other._frozenset)

    def issuperset(self, other: Self) -> bool:
        """Tests whether self is a superset of `other`.

        Parameters:
           other: Closed-term set.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._frozenset.issuperset(other._frozenset)

    def intersection(self, *others: Self) -> Self:
        """Computes the intersection of self and `others`.

        Parameters:
           others: Closed-term sets.

        Returns:
           Closed-term set.
        """
        return type(self)(*self._frozenset.intersection(*map(
            lambda x: x._frozenset, others)))

    def union(self, *others: Self) -> Self:
        """Computes the union of self and `others`.

        Parameters:
           others: Closed-term sets.

        Returns:
           Closed-term set.
        """
        return type(self)(*self._frozenset.union(*map(
            lambda x: x._frozenset, others)))


class SnakSetVariable(Variable):
    """Snak set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[SnakSet]]  # pyright: ignore


class SnakSet(
        ClosedTermSet[Snak],
        children_class=Snak,
        variable_class=SnakSetVariable
):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    children_class: ClassVar[type[Snak]]            # pyright: ignore
    variable_class: ClassVar[type[SnakSetVariable]]  # pyright: ignore

    @override
    def __init__(self, *snaks: Snak) -> None:
        super().__init__(*snaks)


class QualifierRecordVariable(SnakSetVariable):
    """Qualifier record variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[QualifierRecord]]  # pyright: ignore


class QualifierRecord(
        SnakSet,
        children_class=Snak,
        variable_class=QualifierRecordVariable
):
    """Qualifier record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    variable_class: ClassVar[type[QualifierRecordVariable]]  # pyright: ignore

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


class ReferenceRecordVariable(SnakSetVariable):
    """Reference record variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore


class ReferenceRecord(
        SnakSet,
        children_class=Snak,
        variable_class=ReferenceRecordVariable
):
    """Reference record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    variable_class: ClassVar[type[ReferenceRecordVariable]]  # pyright: ignore

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


class ReferenceRecordSetVariable(Variable):
    """Reference record set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ReferenceRecordSet]]  # pyright: ignore


class ReferenceRecordSet(
        ClosedTermSet[ReferenceRecord],
        children_class=ReferenceRecord,
        variable_class=ReferenceRecordSetVariable
):
    """Set of reference records.

    Parameters:
       reference_records: Reference records.
    """

    children_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore
    variable_class: ClassVar[type[                   # pyright: ignore
        ReferenceRecordSetVariable]]

    @override
    def __init__(self, *reference_records: TReferenceRecord) -> None:
        super().__init__(*reference_records)
