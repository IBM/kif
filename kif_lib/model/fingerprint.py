# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import functools
from typing import TYPE_CHECKING

from .. import itertools
from ..typing import (
    Any,
    cast,
    Iterator,
    Literal,
    Location,
    override,
    Self,
    Set,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object
from .set import SnakSet
from .snak import Snak, TSnak, ValueSnak
from .value import (
    DeepDataValue,
    Entity,
    Property,
    PseudoProperty,
    Quantity,
    Time,
    TValue,
    Value,
)

if TYPE_CHECKING:  # pragma: no cover
    from .filter import Filter

TFingerprint: TypeAlias =\
    Union['Fingerprint', 'TCompoundFingerprint', 'TAtomicFingerprint']

TCompoundFingerprint: TypeAlias = Union[
    'CompoundFingerprint', 'TAndFingerprint', 'TOrFingerprint']
TAndFingerprint: TypeAlias = Union[list[Snak], Set[Snak], SnakSet]
TOrFingerprint: TypeAlias = 'OrFingerprint'

TAtomicFingerprint: TypeAlias =\
    Union['AtomicFingerprint', 'TSnakFingerprint',
          'TValueFingerprint', 'TFullFingerprint', 'TEmptyFingerprint']
TSnakFingerprint: TypeAlias = Union['SnakFingerprint', TSnak]
TValueFingerprint: TypeAlias = Union['ValueFingerprint', TValue]
TFullFingerprint: TypeAlias = Union['FullFingerprint', bool, Literal[None]]
TEmptyFingerprint: TypeAlias = Union['EmptyFingerprint', bool]


class Fingerprint(KIF_Object):
    """Abstract base class for fingerprint expressions."""

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
        elif isinstance(arg, (list, Set, SnakSet)):
            return cast(Self, AndFingerprint.check(
                arg, function or cls.check, name, position))
        else:
            return cast(Self, AtomicFingerprint.check(
                arg, function or cls.check, name, position))

    def __and__(self, other: TFingerprint) -> AndFingerprint:
        return AndFingerprint(self, other)

    def __rand__(self, other: TFingerprint) -> AndFingerprint:
        return AndFingerprint(other, self)

    def __or__(self, other: TFingerprint) -> OrFingerprint:
        return OrFingerprint(self, other)

    def __ror__(self, other: TFingerprint) -> OrFingerprint:
        return OrFingerprint(other, self)

    @property
    def datatype_mask(self) -> Filter.DatatypeMask:
        """The datatypes shallow-matched by fingerprint."""
        return self.get_datatype_mask()

    def get_datatype_mask(self) -> Filter.DatatypeMask:
        """Gets the datatypes shallow-matched by fingerprint.

        Returns:
           Datatype mask.
        """
        return self._get_datatype_mask(False)

    @property
    def range_datatype_mask(self) -> Filter.DatatypeMask:
        """The datatypes shallow-matched by the range of fingerprint."""
        return self.get_range_datatype_mask()

    def get_range_datatype_mask(self) -> Filter.DatatypeMask:
        """Gets the datatypes shallow-matched by the range of fingerprint.

        Returns:
           Datatype mask.
        """
        return self._get_datatype_mask(True)

    @abc.abstractmethod
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        raise NotImplementedError

    def is_full(self) -> bool:
        """Tests whether fingerprint is full (matches anything).

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return isinstance(self, FullFingerprint)

    def is_empty(self) -> bool:
        """Tests whether fingerprint is empty (matches nothing).

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return isinstance(self, EmptyFingerprint)

    def match(self, value: TValue) -> bool:
        """Tests whether fingerprint shallow-matches value.

        Parameters:
           value: Value.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self.normalize()._match(Value.check(
            value, self.match, 'value', 1))

    @abc.abstractmethod
    def _match(self, value: Value) -> bool:
        raise NotImplementedError

    def normalize(
            self,
            datatype_mask: Filter.TDatatypeMask | None = None
    ) -> Fingerprint:
        """Reduce fingerprint to a normal form.

        If `datatype_mask` is given, ensures that the resulting fingerprint
        does not match values with a datatype not in `datatype_mask`.

        Parameters:
           value_class: Value class.

        Returns:
           Normal fingerprint.
        """
        from .filter import Filter
        mask = Filter.DatatypeMask.check_optional(
            datatype_mask, Filter.DatatypeMask.ALL,
            self.normalize, 'datatype_mask', 1)
        assert mask is not None
        return self._normalize(mask)

    @abc.abstractmethod
    def _normalize(
            self,
            datatype_mask: Filter.DatatypeMask
    ) -> Fingerprint:
        raise NotImplementedError


class CompoundFingerprint(Fingerprint):
    """Abstract base class for compound fingerprint expressions."""

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
        else:
            constr: type[CompoundFingerprint] = cls
            if cls is CompoundFingerprint:
                constr = AndFingerprint
            if isinstance(arg, Set):
                return cast(Self, constr(*sorted(arg)))
            if isinstance(arg, (list, SnakSet, tuple)):
                return cast(Self, constr(*arg))
            else:
                raise cls._check_error(arg, function, name, position)

    def __init__(self, *fps: TFingerprint) -> None:
        super().__init__(*fps)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Fingerprint.check(arg, type(self), None, i)

    @override
    def _normalize(
            self,
            datatype_mask: Filter.DatatypeMask
    ) -> Fingerprint:
        if datatype_mask.value == 0:
            return EmptyFingerprint()
        if len(self.args) == 0:  # 0-ary compound
            return FullFingerprint()
        if len(self.args) == 1:  # 1-ary compound
            return self.args[0]._normalize(datatype_mask)
        args = list(itertools.uniq(
            self._normalize_args(datatype_mask, iter(self.args))))
        assert len(args) >= 1
        if len(args) == 1:
            return args[0]
        elif (isinstance(self, AndFingerprint)
              and (EmptyFingerprint() in args or len(
                itertools.take(2, filter(
                    lambda fp: isinstance(fp, ValueFingerprint),
                    args))) > 1)):
            return EmptyFingerprint()
        elif (isinstance(self, OrFingerprint)
              and FullFingerprint() in args):
            return FullFingerprint()
        else:
            return type(self)(*args)

    def _normalize_args(
            self,
            datatype_mask: Filter.DatatypeMask,
            it: Iterator[Fingerprint]
    ) -> Iterator[Fingerprint]:
        count, skipped_full, skipped_empty = 0, False, False
        while True:
            try:
                arg = next(it)
            except StopIteration:
                assert not (skipped_full and skipped_empty)
                if count == 0:
                    if skipped_full:
                        yield FullFingerprint()
                    elif skipped_empty:
                        yield EmptyFingerprint()
                break
            arg = arg._normalize(datatype_mask)
            if isinstance(arg, type(self)):
                it = itertools.chain(arg.args, it)
                continue
            elif isinstance(arg, FullFingerprint):
                if isinstance(self, AndFingerprint):
                    skipped_full = True
                    continue    # skip full
                elif isinstance(self, OrFingerprint):
                    yield arg
                    break
                else:
                    raise self._should_not_get_here()
            elif isinstance(arg, EmptyFingerprint):
                if isinstance(self, OrFingerprint):
                    skipped_empty = True
                    continue    # skip empty
                elif isinstance(self, AndFingerprint):
                    yield arg
                    break
                else:
                    raise self._should_not_get_here()
            else:
                yield arg
                count += 1


class AndFingerprint(CompoundFingerprint):
    """Conjunction of fingerprint expressions."""

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        if range:
            f = Fingerprint.get_range_datatype_mask
        else:
            f = Fingerprint.get_datatype_mask
        return functools.reduce(
            lambda x, y: x & y, map(f, self.args), Filter.DatatypeMask.ALL)

    @override
    def _match(self, value: Value) -> bool:
        return all(map(lambda fp: fp._match(value), self.args))


#: Alias of :class:`AndFingerprint`.
And = AndFingerprint


class OrFingerprint(CompoundFingerprint):
    """Disjunction of fingerprint expressions."""

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        if range:
            f = Fingerprint.get_range_datatype_mask
        else:
            f = Fingerprint.get_datatype_mask
        return functools.reduce(
            lambda x, y: x | y, map(f, self.args), Filter.DatatypeMask(0))

    @override
    def _match(self, value: Value) -> bool:
        return any(map(lambda fp: fp._match(value), self.args))


#: Alias of :class:`OrFingerprint`.
Or = OrFingerprint


class AtomicFingerprint(Fingerprint):
    """Abstract base class for atomic fingerprint expressions."""

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
        elif isinstance(arg, (tuple, Snak)):
            return cast(Self, SnakFingerprint.check(
                arg, function or cls.check, name, position))
        elif arg is None or arg is True:
            return cast(Self, FullFingerprint.check(
                arg, function or cls.check, name, position))
        elif arg is False:
            return cast(Self, EmptyFingerprint.check(
                arg, function or cls.check, name, position))
        else:
            return cast(Self, ValueFingerprint.check(
                arg, function or cls.check, name, position))

    @override
    def _normalize(
            self,
            datatype_mask: Filter.DatatypeMask
    ) -> Fingerprint:
        if bool(self.datatype_mask & datatype_mask):
            return self
        else:
            return EmptyFingerprint()


class SnakFingerprint(AtomicFingerprint):
    """Snak fingerprint expression."""

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
        else:
            return cls(Snak.check(arg, function or cls.check, name, position))

    def __init__(self, snak: TSnak) -> None:
        super().__init__(snak)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            return Snak.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def snak(self) -> Snak:
        """The snak of snak fingerprint."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets the snak of snak fingerprint.

        Returns:
           Snak.
        """
        return self.args[0]

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        if range:
            return Filter.VALUE
        else:
            return Filter.ENTITY

    @override
    def _match(self, value: Value) -> bool:
        if isinstance(value, PseudoProperty):
            ###
            # IMPORTANT: Snak fingerprints should not match
            # pseudo-properties because the latter do not exist as entities
            # in the graph, and so cannot occur as subjects of statements.
            ###
            return False
        else:
            return self.datatype_mask.match(type(value))


class ConverseSnakFingerprint(SnakFingerprint):
    """Converse-snak fingerprint expression."""

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        if (isinstance(self.snak, ValueSnak)
                and isinstance(self.snak.value, Entity)):
            return Filter.VALUE
        else:
            return Filter.DatatypeMask(0)


class ValueFingerprint(AtomicFingerprint):
    """Value fingerprint expression."""

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
        else:
            return cls(Value.check(arg, function or cls.check, name, position))

    def __init__(self, value: TValue) -> None:
        super().__init__(value)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Value.check(arg, type(self), None, i)

    @property
    def value(self) -> Value:
        """The value of value fingerprint."""
        return self.get_value()

    def get_value(self) -> Value:
        """Gets the value of value fingerprint.

        Returns:
           Value.
        """
        return self.args[0]

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        if range:
            if isinstance(self.value, Property):
                if self.value.range is not None:
                    return Filter.DatatypeMask.check(type(self.value.range))
                else:
                    return Filter.VALUE
            else:
                return Filter.DatatypeMask(0)
        else:
            return Filter.DatatypeMask.check(type(self.value))

    @override
    def _match(self, value: Value) -> bool:
        v1, v2 = self.value, value
        t1, t2 = type(v1), type(v2)
        if t1 is not t2:
            if not issubclass(t1, t2):
                return False
            try:
                v2 = t1.check(v2)   # coerce v2 to type(v1)
            except (TypeError, ValueError):
                return False
        if isinstance(v2, Property):
            fr_prop, prop = cast(Property, v1), v2
            if fr_prop.iri != prop.iri:
                return False
            if (fr_prop.range is not None
                and prop.range is not None
                    and fr_prop.range != prop.range):
                return False
        elif not isinstance(v2, DeepDataValue):
            if v1 != v2:
                return False
        elif isinstance(v2, Quantity):
            assert isinstance(v1, Quantity)
            if (v1.amount != v2.amount
                or (v1.unit is not None
                    and v1.unit != v2.unit)
                or (v1.lower_bound is not None
                    and v1.lower_bound != v2.lower_bound)
                or (v1.upper_bound is not None
                    and v1.upper_bound != v2.upper_bound)):
                return False
        elif isinstance(v2, Time):
            assert isinstance(v1, Time)
            v1_time, v2_time = v1.time, v2.time
            if v1_time.tzinfo is None:
                v2_time = v2_time.replace(tzinfo=None)
            if (v1_time != v2_time
                or (v1.precision is not None
                    and v1.precision != v2.precision)
                or (v1.timezone is not None
                    and v1.timezone != v2.timezone)
                or (v1.calendar is not None
                    and v1.calendar != v2.calendar)):
                return False
        else:
            raise self._should_not_get_here()
        return True

    @override
    def _normalize(
            self,
            datatype_mask: Filter.DatatypeMask
    ) -> Fingerprint:
        if bool(self.datatype_mask & datatype_mask):
            return self
        else:
            try:
                return self.check(
                    datatype_mask._to_value_class().check(self.value))
            except (TypeError, ValueError):
                return EmptyFingerprint()
            else:
                raise self._should_not_get_here()


class FullFingerprint(AtomicFingerprint):
    """The full fingerprint (matches anything)."""

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
        elif arg is True or arg is None:
            return cls()
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self) -> None:
        super().__init__()

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        return Filter.VALUE

    @override
    def _match(self, value: Value) -> bool:
        return True


class EmptyFingerprint(AtomicFingerprint):
    """The empty fingerprint (matches nothing)."""

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
        elif arg is False:
            return cls()
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self) -> None:
        super().__init__()

    @override
    def _get_datatype_mask(self, range: bool) -> Filter.DatatypeMask:
        from .filter import Filter
        return Filter.DatatypeMask(0)

    @override
    def _match(self, value: Value) -> bool:
        return False

    @override
    def _normalize(
            self,
            datatype_mask: Filter.DatatypeMask
    ) -> Fingerprint:
        return self
