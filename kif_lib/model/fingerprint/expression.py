# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc

from ... import itertools
from ...typing import (
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
from ..kif_object import KIF_Object
from ..set import SnakSet
from ..snak import Snak, TSnak
from ..value import DeepDataValue, Property, Quantity, Time, TValue, Value
from .entity_fingerprint import EntityFingerprint
from .fingerprint import Fingerprint
from .property_fingerprint import PropertyFingerprint

TFp: TypeAlias =\
    Union['Fp', 'TAtomicFp',
          Fingerprint, EntityFingerprint, PropertyFingerprint]
TAtomicFp: TypeAlias =\
    Union['AtomicFp', 'TSnakFp', 'TValueFp', 'TFullFp', 'TEmptyFp']
TSnakFp: TypeAlias = Union['SnakFp', TSnak]
TValueFp: TypeAlias = Union['ValueFp', TValue]
TFullFp: TypeAlias = Union['FullFp', bool, Literal[None]]
TEmptyFp: TypeAlias = Union['EmptyFp', bool]


class Fp(KIF_Object):
    """Abstract base class for fingerprint expressions."""

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
        elif isinstance(arg, Fingerprint):
            return cls.check(arg[0], function, name, position)
        elif isinstance(arg, (list, Set, SnakSet)):
            return cast(Self, AndFp(*arg))
        elif isinstance(arg, (tuple, Snak)):
            return cast(Self, SnakFp.check(
                arg, function or cls.check, name, position))
        elif isinstance(arg, bool):
            return cast(Self, (FullFp if arg else EmptyFp)())
        elif arg is None:
            return cast(Self, FullFp())
        else:
            return cast(Self, ValueFp.check(
                arg, function or cls.check, name, position))

    def __and__(self, other: TFp) -> 'Fp':
        return AndFp(self, other)

    def __rand__(self, other: TFp) -> 'Fp':
        return AndFp(other, self)

    def __or__(self, other: TFp) -> 'Fp':
        return OrFp(self, other)

    def __ror__(self, other: TFp) -> 'Fp':
        return OrFp(self, other)

    def is_full(self) -> bool:
        """Tests whether fingerprint expression is full.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return isinstance(self, FullFp)

    def is_empty(self) -> bool:
        """Tests whether fingerprint expression is empty.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return isinstance(self, EmptyFp)

    def match(self, value: TValue) -> bool:
        """Tests whether fingerprint expression shallow-matches value.

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

    def normalize(self, value_class: type[Value] = Value) -> 'Fp':
        """Reduce fingerprint expression to a normal form.

        Produces a normal fingerprint expression that does *not* match
        values of a type different from `value_class`.

        Parameters:
           value_class: Value class.

        Returns:
           Normal fingerprint expression.

        """
        if isinstance(self, ValueFp):
            if isinstance(self.value, value_class):
                return self
            else:
                return EmptyFp()
        elif isinstance(self, AtomicFp):
            return self
        else:
            args = list(itertools.unique_everseen(
                self._normalize_args(value_class, iter(self.args))))
            if len(args) == 0:
                return FullFp()
            if len(args) == 1:
                return args[0].normalize(value_class)
            if (isinstance(self, AndFp)
                and (EmptyFp() in args or len(itertools.take(2, filter(
                    lambda fp: isinstance(fp, ValueFp), args))) > 1)):
                return EmptyFp()
            elif isinstance(self, OrFp) and FullFp() in args:
                return FullFp()
            else:
                return self.__class__(*args)

    def _normalize_args(
            self,
            value_class: type[Value],
            it: Iterator['Fp']
    ) -> Iterator['Fp']:
        while True:
            try:
                arg = next(it)
            except StopIteration:
                break
            arg = arg.normalize(value_class)
            if isinstance(arg, type(self)):
                it = itertools.chain(arg.args, it)
                continue
            elif isinstance(arg, FullFp):
                if isinstance(self, AndFp):
                    continue    # skip full
                elif isinstance(self, OrFp):
                    yield FullFp()
                    break
                else:
                    raise self._should_not_get_here()
            elif isinstance(arg, EmptyFp):
                if isinstance(self, OrFp):
                    continue    # skip empty
                elif isinstance(self, AndFp):
                    yield EmptyFp()
                    break
                else:
                    raise self._should_not_get_here()
            else:
                yield arg


class CompoundFp(Fp):
    """Compound fingerprint expression."""

    def __init__(self, *fps: TFp):
        super().__init__(*fps)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Fp.check(arg, type(self), None, i)


class AndFp(CompoundFp):
    """Conjunction of fingerprint expressions."""

    @override
    def _match(self, value: Value) -> bool:
        return all(map(lambda fp: fp._match(value), self.args))


class OrFp(CompoundFp):
    """Disjunction of fingerprint expressions."""

    @override
    def _match(self, value: Value) -> bool:
        return any(map(lambda fp: fp._match(value), self.args))


class AtomicFp(Fp):
    """Atomic fingerprint expression."""


class SnakFp(AtomicFp):
    """Snak fingerprint expression."""

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
        return Snak.check(arg, type(self), None, i)

    @property
    def snak(self) -> Snak:
        """The snak of fingerprint expression."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets the snak of fingerprint expression.

        Returns:
           Snak.
        """
        return self.args[0]

    @override
    def _match(self, value: Value) -> bool:
        return True


class ValueFp(AtomicFp):
    """Value fingerprint expression."""

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
        """The value of fingerprint expression."""
        return self.get_value()

    def get_value(self) -> Value:
        """Gets the value of fingerprint expression.

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


class FullFp(AtomicFp):
    """The full fingerprint expression (matches anything)."""

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


class EmptyFp(AtomicFp):
    """The empty fingerprint expression (matches nothing)."""

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
