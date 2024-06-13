# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
import enum
import functools
import json

from ..itertools import chain
from ..typing import (
    Any,
    Callable,
    cast,
    Iterator,
    Optional,
    override,
    TypeAlias,
    Union,
)
from . import object

Datetime = datetime.datetime
Decimal = decimal.Decimal
UTC = datetime.timezone.utc

Codec = object.Codec
CodecError = object.CodecError
Decoder = object.Decoder
DecoderError = object.DecoderError
Encoder = object.Encoder
EncoderError = object.EncoderError
Error = object.Error
MustBeImplementedInSubclass = object.MustBeImplementedInSubclass
Nil = object.Nil
Object = object.Object
ShouldNotGetHere = object.ShouldNotGetHere

TArgs: TypeAlias = object.TArgs
TCallable: TypeAlias = object.TFun
TDatetime: TypeAlias = Union[Datetime, str]
TDecimal: TypeAlias = Union[Decimal, float, int, str]
TDetails: TypeAlias = object.TDet
TLocation: TypeAlias = object.TLoc
TNil: TypeAlias = object.TNil

KIF_ObjectClass: TypeAlias = type['KIF_Object']


# == KIF Object ============================================================

class KIF_Object(object.Object):
    """Abstract base class for KIF objects."""

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if 'template_class' in kwargs:
            from .template import Template
            from .variable import Variable
            assert not issubclass(cls, (Template, Variable))
            cls.template_class = kwargs['template_class']
            assert issubclass(cls.template_class, Template)
            cls.template_class.object_class = cls  # pyright: ignore
        if 'variable_class' in kwargs:
            from .template import Template
            from .variable import Variable
            assert not issubclass(cls, (Template, Variable))
            cls.variable_class = kwargs['variable_class']
            assert issubclass(cls.variable_class, Variable)
            cls.variable_class.object_class = cls  # pyright: ignore

    def __new__(cls, *args, **kwargs):
        has_tpl_or_var_arg = any(map(
            cls._isinstance_template_or_variable,
            chain(args, kwargs.values())))
        if hasattr(cls, 'template_class') and has_tpl_or_var_arg:
            return cls.template_class(*args, **kwargs)
        elif (cls._issubclass_template(cls)
              and hasattr(cls, 'object_class') and not has_tpl_or_var_arg):
            return cls.object_class(*args, **kwargs)  # pyright: ignore
        else:
            return super().__new__(cls)

    @classmethod
    def _issubclass_template(cls, arg: Any) -> bool:
        from .template import Template
        return issubclass(arg, Template)

    @classmethod
    def _isinstance_template_or_variable(cls, arg: Any) -> bool:
        from .template import Template
        from .variable import Variable
        return isinstance(arg, (Template, Variable))

# -- datetime --------------------------------------------------------------

    @classmethod
    def _check_arg_datetime(
            cls,
            arg: TDatetime,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Datetime:
        arg = cls._check_arg_isinstance(
            arg, (Datetime, str), function, name, position)
        if isinstance(arg, str):
            if arg[0] == '+' or arg[0] == '-':
                ###
                # FIXME: Python's fromisoformat() does not support the +/-
                # sign used by Wikidata at the start of date-time literals.
                ###
                arg = arg[1:]
            try:
                dt = Datetime.fromisoformat(arg)
                if dt.tzinfo is None:
                    ###
                    # IMPORTANT: If no timezone is given, we assume UTC.
                    ###
                    return dt.replace(tzinfo=UTC)
                else:
                    return dt
            except Exception as err:
                raise cls._arg_error(
                    f'expected {Datetime.__qualname__}',
                    function, name, position, ValueError) from err
        elif isinstance(arg, Datetime):
            return arg
        else:
            raise cls._should_not_get_here()

    @classmethod
    def _check_optional_arg_datetime(
            cls,
            arg: Optional[TDatetime],
            default: Optional[Datetime] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Datetime]:
        if arg is None:
            return default
        else:
            return cls._check_arg_datetime(arg, function, name, position)

    @classmethod
    def _preprocess_arg_datetime(
            cls,
            arg: TDatetime,
            i: int,
            function: Optional[TLocation] = None
    ) -> Datetime:
        return cls._check_arg_datetime(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_datetime(
            cls,
            arg: Optional[TDatetime],
            i: int,
            default: Optional[Datetime] = None,
            function: Optional[TLocation] = None
    ) -> Optional[Datetime]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_datetime(arg, i, function)

# -- decimal ---------------------------------------------------------------

    @classmethod
    def _check_arg_decimal(
            cls,
            arg: TDecimal,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Decimal:
        arg = cls._check_arg_isinstance(
            arg, (Decimal, float, int, str), function, name, position)
        try:
            return Decimal(arg)
        except decimal.InvalidOperation as err:
            raise cls._arg_error(
                f'expected {Decimal.__qualname__}',
                function, name, position, ValueError) from err

    @classmethod
    def _check_optional_arg_decimal(
            cls,
            arg: Optional[TDecimal],
            default: Optional[Decimal] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Decimal]:
        if arg is None:
            return default
        else:
            return cls._check_arg_decimal(arg, function, name, position)

    @classmethod
    def _preprocess_arg_decimal(
            cls,
            arg: TDecimal,
            i: int,
            function: Optional[TLocation] = None
    ) -> Decimal:
        return cls._check_arg_decimal(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_decimal(
            cls,
            arg: Optional[TDecimal],
            i: int,
            default: Optional[Decimal] = None,
            function: Optional[TLocation] = None
    ) -> Optional[Decimal]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_decimal(arg, i, function)

# -- misc ------------------------------------------------------------------

    def _repr_markdown_(self) -> str:
        return self.to_markdown()  # pyright: ignore

    _traverse_default_filter = (lambda _: True)
    _traverse_default_visit = (lambda _: True)

    def traverse(
        self,
        filter: Optional[Callable[[Any], bool]] = None,
        visit: Optional[Callable[[Any], bool]] = None
    ) -> Iterator[Any]:
        """Traverses KIF object-tree recursively.

        Parameters:
           filter: Predicate indicating KIF objects or values to yield.
           visit: Predicate indicating KIF objects to visit.

        Returns:
           An iterator of KIF objects and values.
        """
        filter = self._check_optional_arg_callable(
            filter, self.__class__._traverse_default_filter,
            self.traverse, 'filter', 1)
        visit = self._check_optional_arg_callable(
            visit, self.__class__._traverse_default_visit,
            self.traverse, 'visit', 2)
        assert filter is not None
        assert visit is not None
        return self._traverse(filter, visit)

    def _traverse(
            self,
            filter: Callable[[Any], bool],
            visit: Callable[[Any], bool]
    ) -> Iterator[Any]:
        if visit(self):
            if filter(self):
                yield self
            for arg in self.args:
                if isinstance(arg, KIF_Object):
                    yield from arg._traverse(filter, visit)
                elif filter(arg):
                    yield arg


# == Codecs ================================================================

class KIF_JSON_Encoder(
        object.JSON_Encoder, format='json', description='JSON encoder'):
    """KIF JSON encoder."""

    class Encoder(object.JSON_Encoder.Encoder):
        """The underlying JSON encoder."""

        @override
        def default(self, o: Any) -> Any:
            if isinstance(o, Object):
                obj = cast(Object, o)
                return {
                    'class': obj.__class__.__qualname__,
                    'args': obj.args,
                }
            elif isinstance(o, (Datetime, Decimal)):
                return str(o)
            elif isinstance(o, enum.Enum):
                return str(o.value)
            else:
                try:
                    return json.JSONEncoder.default(self, o)
                except TypeError as err:
                    raise EncoderError(str(err)) from None


class KIF_ReprDecoder(
        object.ReprDecoder, format='repr', description='Repr. decoder'):
    """KIF repr. decoder."""

    @classmethod
    @functools.cache
    def _globals(cls) -> dict[str, Any]:
        return {'Decimal': Decimal, 'datetime': datetime, **super()._globals()}


class KIF_ReprEncoder(
        object.ReprEncoder, format='repr', description='Repr. encoder'):
    """KIF repr. encoder."""

    @override
    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0
    ) -> Iterator[str]:
        if isinstance(v, (Datetime, Decimal)):
            yield from self._indent(n, indent)
            yield repr(v)
        elif isinstance(v, enum.Enum):
            yield from self._indent(n, indent)
            yield repr(v.value)
        else:
            yield from super()._iterencode(v, n, indent)


class KIF_SExpEncoder(
        object.SExpEncoder, format='sexp', description='S-expression encoder'):
    """KIF S-expression encoder."""

    @override
    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0
    ) -> Iterator[str]:
        if isinstance(v, (Datetime, Decimal)):
            yield from self._indent(n, indent)
            yield str(v)
        elif isinstance(v, enum.Enum):
            yield from self._indent(n, indent)
            yield str(v.value)
        else:
            yield from super()._iterencode(v, n, indent)
