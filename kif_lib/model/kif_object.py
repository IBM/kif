# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
import json
from enum import Enum
from functools import cache

from ..itertools import chain
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
            from .template import Template
            from .variable import Variable
            assert not issubclass(cls, (Template, Variable))
            cls.template_class = kwargs['template_class']
            assert issubclass(cls.template_class, Template)
            cls.template_class.object_class = cls
        if 'variable_class' in kwargs:
            from .template import Template
            from .variable import Variable
            assert not issubclass(cls, (Template, Variable))
            cls.variable_class = kwargs['variable_class']
            assert issubclass(cls.variable_class, Variable)
            cls.variable_class.object_class = cls

    def __new__(cls, *args, **kwargs):
        has_tpl_or_var_arg = any(map(
            cls._isinstance_template_or_variable,
            chain(args, kwargs.values())))
        if hasattr(cls, 'template_class') and has_tpl_or_var_arg:
            return cls.template_class(*args, **kwargs)
        elif (cls._issubclass_template(cls)
              and hasattr(cls, 'object_class') and not has_tpl_or_var_arg):
            return cls.object_class(*args, **kwargs)
        else:
            return super().__new__(cls)

    @classmethod
    def _issubclass_template(cls, arg):
        from .template import Template
        return issubclass(arg, Template)

    @classmethod
    def _isinstance_template_or_variable(cls, arg):
        from .template import Template
        from .variable import Variable
        return isinstance(arg, (Template, Variable))

# -- datetime --------------------------------------------------------------

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

# -- decimal ---------------------------------------------------------------

    @classmethod
    def _check_arg_decimal(
            cls, arg, function=None, name=None, position=None):
        arg = cls._check_arg_isinstance(
            arg, (Decimal, float, int, str), function, name, position)
        try:
            return Decimal(arg)
        except decimal.InvalidOperation:
            raise cls._arg_error(
                f'expected {Decimal.__qualname__}',
                function, name, position, ValueError)

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

# -- misc ------------------------------------------------------------------

    def _repr_markdown_(self):
        return self.to_markdown()

    _traverse_default_filter = (lambda _: True)
    _traverse_default_visit = (lambda _: True)

    def traverse(
            self,
            filter=None,
            visit=None,
    ):
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

    def _traverse(self, filter, visit):
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
