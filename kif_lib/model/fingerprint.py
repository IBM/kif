# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import TYPE_CHECKING

from .. import itertools
from ..typing import (
    Any,
    Callable,
    cast,
    Iterator,
    Literal,
    Optional,
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
    Quantity,
    Time,
    TValue,
    Value,
)

if TYPE_CHECKING:  # pragma: no cover
    from .filter import Filter

TFingerprint: TypeAlias =\
    Union['Fingerprint', 'TCompoundFingerprint', 'TAtomicFingerprint']

TAtomicFingerprint: TypeAlias =\
    Union['AtomicFingerprint', 'TSnakFingerprint',
          'TValueFingerprint', 'TFullFingerprint', 'TEmptyFingerprint']
TSnakFingerprint: TypeAlias = Union['SnakFingerprint', TSnak]
TValueFingerprint: TypeAlias = Union['ValueFingerprint', TValue]
TFullFingerprint: TypeAlias = Union['FullFingerprint', bool, Literal[None]]
TEmptyFingerprint: TypeAlias = Union['EmptyFingerprint', bool]

TCompoundFingerprint: TypeAlias = Union[
    'CompoundFingerprint', 'TAndFingerprint', 'TOrFingerprint']
TAndFingerprint: TypeAlias = Union[list[Snak], Set[Snak], SnakSet]
TOrFingerprint: TypeAlias = 'OrFingerprint'


class Fingerprint(KIF_Object):
    """Abstract base class for fingerprints."""

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
        elif isinstance(arg, Set):
            return cast(Self, AndFingerprint(*sorted(arg)))
        elif isinstance(arg, (list, SnakSet)):
            return cast(Self, AndFingerprint(*arg))
        elif isinstance(arg, (tuple, Snak)):
            return cast(Self, SnakFingerprint.check(
                arg, function or cls.check, name, position))
        elif isinstance(arg, bool):
            return cast(Self, (
                FullFingerprint if arg else EmptyFingerprint)())
        elif arg is None:
            return cast(Self, FullFingerprint())
        else:
            return cast(Self, ValueFingerprint.check(
                arg, function or cls.check, name, position))

    def __and__(self, other: TFingerprint) -> 'Fingerprint':
        return AndFingerprint(self, other)

    def __rand__(self, other: TFingerprint) -> 'Fingerprint':
        return AndFingerprint(other, self)

    def __or__(self, other: TFingerprint) -> 'Fingerprint':
        return OrFingerprint(self, other)

    def __ror__(self, other: TFingerprint) -> 'Fingerprint':
        return OrFingerprint(other, self)

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
            datatype_mask: Optional['Filter.DatatypeMask'] = None
    ) -> 'Fingerprint':
        """Reduce fingerprint to a normal form.

        If `datatype_mask` is given, ensures that the resulting fingerprint
        does not match values with a datatype not in `datatype_mask`.

        Parameters:
           value_class: Value class.

        Returns:
           Normal fingerprint.

        """
        if isinstance(self, ValueFingerprint):
            if datatype_mask is None or datatype_mask.match(type(self.value)):
                return self
            else:
                return EmptyFingerprint()
        elif isinstance(self, AtomicFingerprint):
            return self
        else:
            args = list(itertools.unique_everseen(
                self._normalize_args(datatype_mask, iter(self.args))))
            if len(args) == 0:
                return FullFingerprint()
            if len(args) == 1:
                return args[0].normalize(datatype_mask)
            if (isinstance(self, AndFingerprint)
                and (EmptyFingerprint() in args or len(
                    itertools.take(2, filter(
                        lambda fp: isinstance(fp, ValueFingerprint),
                        args))) > 1)):
                return EmptyFingerprint()
            elif (isinstance(self, OrFingerprint)
                  and FullFingerprint() in args):
                return FullFingerprint()
            else:
                return self.__class__(*sorted(args))

    def _normalize_args(
            self,
            datatype_mask: Optional['Filter.DatatypeMask'],
            it: Iterator['Fingerprint']
    ) -> Iterator['Fingerprint']:
        while True:
            try:
                arg = next(it)
            except StopIteration:
                break
            arg = arg.normalize(datatype_mask)
            if isinstance(arg, type(self)):
                it = itertools.chain(arg.args, it)
                continue
            elif isinstance(arg, FullFingerprint):
                if isinstance(self, AndFingerprint):
                    continue    # skip full
                elif isinstance(self, OrFingerprint):
                    yield FullFingerprint()
                    break
                else:
                    raise self._should_not_get_here()
            elif isinstance(arg, EmptyFingerprint):
                if isinstance(self, OrFingerprint):
                    continue    # skip empty
                elif isinstance(self, AndFingerprint):
                    yield EmptyFingerprint()
                    break
                else:
                    raise self._should_not_get_here()
            else:
                yield arg


class CompoundFingerprint(Fingerprint):
    """Compound fingerprint."""

    def __init__(self, *fps: TFingerprint):
        super().__init__(*fps)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Fingerprint.check(arg, type(self), None, i)


class AndFingerprint(CompoundFingerprint):
    """Conjunction of fingerprints."""

    @override
    def _match(self, value: Value) -> bool:
        return all(map(lambda fp: fp._match(value), self.args))


class OrFingerprint(CompoundFingerprint):
    """Disjunction of fingerprints."""

    @override
    def _match(self, value: Value) -> bool:
        return any(map(lambda fp: fp._match(value), self.args))


class AtomicFingerprint(Fingerprint):
    """Atomic fingerprint."""


class SnakFingerprint(AtomicFingerprint):
    """Snak fingerprint."""

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
        else:
            return cls(Snak.check(arg, function or cls.check, name, position))

    def __init__(self, snak: TSnak):
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
    def _match(self, value: Value) -> bool:
        return True


class ConverseSnakFingerprint(SnakFingerprint):
    """Converse snak fingerprint."""

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
        else:
            snak = ValueSnak.check(
                arg, function or cls.check, name, position)
            if isinstance(snak.value, Entity):
                return cls(snak)
            else:
                raise cls._check_error(
                    arg, function or cls.check, name, position)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            snak = ValueSnak.check(arg, type(self), None, i)
            Entity.check(snak.value, type(self), None, i)
            return snak
        else:
            raise self._should_not_get_here()


class ValueFingerprint(AtomicFingerprint):
    """Value fingerprint."""

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
        else:
            return cls(Value.check(arg, function or cls.check, name, position))

    def __init__(self, value: TValue):
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
    def _match(self, value: Value) -> bool:
        if type(self.value) is not type(value):
            return False
        if isinstance(value, Property):
            fr_prop, prop = cast(Property, self.value), value
            if fr_prop.iri != prop.iri:
                return False
            if fr_prop.range is not None and fr_prop.range != prop.range:
                return False
        elif not isinstance(value, DeepDataValue):
            if self.value != value:
                return False
        elif isinstance(value, Quantity):
            fr_qt = cast(Quantity, self.value)
            qt = value
            if (fr_qt.amount != qt.amount
                or (fr_qt.unit is not None
                    and fr_qt.unit != qt.unit)
                or (fr_qt.lower_bound is not None
                    and fr_qt.lower_bound != qt.lower_bound)
                or (fr_qt.upper_bound is not None
                    and fr_qt.upper_bound != qt.upper_bound)):
                return False
        elif isinstance(value, Time):
            fr_tm, tm = cast(Time, self.value), value
            fr_tm_time, tm_time = fr_tm.time, tm.time
            if fr_tm_time.tzinfo is None:
                tm_time = tm_time.replace(tzinfo=None)
            if (fr_tm_time != tm_time
                or (fr_tm.precision is not None
                    and fr_tm.precision != tm.precision)
                or (fr_tm.timezone is not None
                    and fr_tm.timezone != tm.timezone)
                or (fr_tm.calendar is not None
                    and fr_tm.calendar != tm.calendar)):
                return False
        else:
            raise self._should_not_get_here()
        return True


class FullFingerprint(AtomicFingerprint):
    """The full fingerprint (matches anything)."""

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
        elif bool(arg):
            return cls()
        else:
            raise cls._check_error(arg, function, name, position, ValueError)

    def __init__(self):
        super().__init__()

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
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif not bool(arg):
            return cls()
        else:
            raise cls._check_error(arg, function, name, position, ValueError)

    def __init__(self):
        super().__init__()

    @override
    def _match(self, value: Value) -> bool:
        return False
