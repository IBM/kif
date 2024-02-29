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


# -- KIF Object ------------------------------------------------------------

class KIF_Object(object.Object):
    """Abstract base class for KIF objects."""

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
                ###
                # IMPORTANT: Do not forget to reset tzinfo to UTC.
                # In KIF, the actual timezone is stored in the Time object.
                ###
                return Datetime.fromisoformat(arg).replace(tzinfo=UTC)
            except Exception:
                raise cls._arg_error(
                    f'expected {Datetime.__qualname__}',
                    function, name, position, ValueError)
        elif isinstance(arg, Datetime):
            return arg.replace(tzinfo=UTC)
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


# -- Codecs ----------------------------------------------------------------

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
