# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import itertools
from ...typing import (
    Any,
    Callable,
    cast,
    Iterator,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..kif_object import KIF_Object
from ..snak import Snak, TSnak
from ..value import TValue, Value

TFp: TypeAlias = Union['Fp', 'TAtomicFp']
TAtomicFp: TypeAlias =\
    Union['AtomicFp', 'TSnakFp', 'TValueFp', 'TFullFp', 'TEmptyFp']
TSnakFp: TypeAlias = Union['SnakFp', TSnak]
TValueFp: TypeAlias = Union['ValueFp', TValue]
TFullFp: TypeAlias = Union['FullFp', bool]
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
        elif isinstance(arg, (tuple, Snak)):
            return cast(Self, SnakFp.check(
                arg, function or cls.check, name, position))
        elif isinstance(arg, bool):
            return cast(Self, (FullFp if arg else EmptyFp)())
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

    def normalize(self) -> 'Fp':
        """Reduce fingerprint expression to a normal form.

        Returns:
           Normal fingerprint expression.
        """
        if isinstance(self, AtomicFp):
            return self
        else:
            args = list(itertools.unique_everseen(
                self._normalize_args(iter(self.args))))
            if len(args) == 0:
                return FullFp()
            elif len(args) == 1:
                return args[0].normalize()
            elif isinstance(self, AndFp) and EmptyFp() in args:
                return EmptyFp()
            elif isinstance(self, OrFp) and FullFp() in args:
                return FullFp()
            else:
                return self.__class__(*args)

    def _normalize_args(self, it: Iterator['Fp']) -> Iterator['Fp']:
        while True:
            try:
                arg = next(it)
            except StopIteration:
                break
            arg = arg.normalize()
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


class OrFp(CompoundFp):
    """Disjunction of fingerprint expressions."""


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
