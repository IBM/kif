# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
import json
from enum import Enum
from functools import cache

from ..typing import Any, cast, Generator, override, Union
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
TCallable = object.TFun
TDatetime = Union[Datetime, str]
TDecimal = Union[Decimal, float, int, str]
TNil = object.TNil


# == KIF Object ============================================================

class KIF_Object(object.Object):
    """Abstract base class for KIF objects."""

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if 'template_class' in kwargs:
            from .pattern import Template, Variable
            assert not issubclass(cls, (Template, Variable))
            cls.template_class = kwargs['template_class']
            assert issubclass(cls.template_class, Template)
            cls.template_class.object_class = cls
        if 'variable_class' in kwargs:
            from .pattern import Template, Variable
            assert not issubclass(cls, (Template, Variable))
            cls.variable_class = kwargs['variable_class']
            assert issubclass(cls.variable_class, Variable)
            cls.variable_class.object_class = cls

    def __new__(cls, *args):
        has_tpl_or_var_arg = any(map(
            cls._isinstance_template_or_variable, args))
        if (not cls._issubclass_template_or_variable(cls)
                and hasattr(cls, 'template_class') and has_tpl_or_var_arg):
            return cls.template_class(*args)
        elif (cls._issubclass_template(cls)
              and hasattr(cls, 'object_class') and not has_tpl_or_var_arg):
            return cls.object_class(*args)
        else:
            return super().__new__(cls)

    @classmethod
    def _issubclass_template(cls, arg) -> bool:
        from .pattern import Template
        return issubclass(arg, Template)

    @classmethod
    def _issubclass_template_or_variable(cls, arg) -> bool:
        from .pattern import Template, Variable
        return issubclass(arg, (Template, Variable))

    @classmethod
    def _isinstance_template_or_variable(cls, arg) -> bool:
        from .pattern import Template, Variable
        return isinstance(arg, (Template, Variable))

    def _repr_markdown_(self):
        return self.to_markdown()

    # -- datetime --

    @classmethod
    def _check_arg_datetime(
            cls, arg, function=None, name=None, position=None):
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
            except Exception:
                raise cls._arg_error(
                    f'expected {Datetime.__qualname__}',
                    function, name, position, ValueError)
        elif isinstance(arg, Datetime):
            return arg
        else:
            raise cls._should_not_get_here()

    @classmethod
    def _check_optional_arg_datetime(
            cls, arg, default=None, function=None, name=None, position=None):
        if arg is None:
            return default
        else:
            return cls._check_arg_datetime(arg, function, name, position)

    @classmethod
    def _preprocess_arg_datetime(cls, arg, i, function=None):
        return cls._check_arg_datetime(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_datetime(
            cls, arg, i, default=None, function=None):
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_datetime(arg, i, function)

    # -- decimal --

    @classmethod
    def _check_arg_decimal(
            cls, arg, function=None, name=None, position=None):
        arg = cls._check_arg_isinstance(
            arg, (Decimal, float, int, str), function, name, position)
        try:
            return Decimal(arg)
        except decimal.InvalidOperation:
            raise cls._arg_error(
                'expected decimal', function, name, position, ValueError)

    @classmethod
    def _check_optional_arg_decimal(
            cls, arg, default=None, function=None, name=None, position=None):
        if arg is None:
            return default
        else:
            return cls._check_arg_decimal(arg, function, name, position)

    @classmethod
    def _preprocess_arg_decimal(
            cls, arg, i, function=None):
        return cls._check_arg_decimal(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_decimal(
            cls, arg, i, default=None, function=None):
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_decimal(arg, i, function)


# == Codecs ================================================================

class KIF_JSON_Encoder(
        object.JSON_Encoder, format='json', description='JSON encoder'):

    class Encoder(json.JSONEncoder):

        @override
        def default(self, v: Any) -> Any:
            if isinstance(v, Object):
                obj = cast(Object, v)
                return {
                    'class': obj.__class__.__qualname__,
                    'args': obj.args,
                }
            elif isinstance(v, (Datetime, Decimal)):
                return str(v)
            elif isinstance(v, Enum):
                return str(v.value)
            else:
                try:
                    return json.JSONEncoder.default(self, v)
                except TypeError as err:
                    raise EncoderError(str(err)) from None


class KIF_ReprDecoder(
        object.ReprDecoder, format='repr', description='Repr. decoder'):

    @override
    @cache
    def _globals(self):
        return {'Decimal': Decimal, 'datetime': datetime, **super()._globals()}


class KIF_ReprEncoder(
        object.ReprEncoder, format='repr', description='Repr. encoder'):

    @override
    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0
    ) -> Generator[str, None, None]:
        if isinstance(v, (Datetime, Decimal)):
            yield from self._indent(n, indent)
            yield repr(v)
        elif isinstance(v, Enum):
            yield from self._indent(n, indent)
            yield repr(v.value)
        else:
            yield from super()._iterencode(v, n, indent)


class KIF_SExpEncoder(
        object.SExpEncoder, format='sexp', description='S-expression encoder'):

    @override
    def _iterencode(
            self,
            v: Any, n: int = 0,
            indent: int = 0
    ) -> Generator[str, None, None]:
        if isinstance(v, (Datetime, Decimal)):
            yield from self._indent(n, indent)
            yield str(v)
        elif isinstance(v, Enum):
            yield from self._indent(n, indent)
            yield str(v.value)
        else:
            yield from super()._iterencode(v, n, indent)
