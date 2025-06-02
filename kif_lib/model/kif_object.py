# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal
import enum
import functools
import json

from ..context import Context
from ..typing import (
    Any,
    Callable,
    cast,
    Iterator,
    Mapping,
    override,
    Self,
    TypeVar,
)
from . import object

Codec = object.Codec
CodecError = object.Codec.Error
Decoder = object.Decoder
DecoderError = object.Decoder.Error
Encoder = object.Encoder
EncoderError = object.Encoder.Error
Error = object.Object.Error

Object = object.Object
ShouldNotGetHere = object.Object.ShouldNotGetHere

T = TypeVar('T')


class KIF_Object(object.Object, metaclass=object.ObjectMeta):
    """Abstract base class for KIF objects."""

    @property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        return Context.top(context)

    @classmethod
    def from_sparql(cls, s: str, **kwargs: Any) -> Self:
        """Decodes string using SPARQL decoder.

        Parameters:
           kwargs: Options to SPARQL decoder.

        Returns:
           KIF object.

        Raises:
           `DecoderError`: Decoder error.
        """
        return cls.loads(s, 'sparql', **kwargs)

    def to_dot(self, **kwargs: Any) -> str:
        """Encodes object using Dot encoder.

        Parameters:
           kwargs: Options to Dot encoder.

        Returns:
           String.

        Raises:
           `EncoderError`: Encoder error.
        """
        return self.dumps('dot', **kwargs)

    def to_markdown(self, **kwargs: Any) -> str:
        """Encodes object using Markdown encoder.

        Parameters:
           kwargs: Options to Markdown encoder.

        Returns:
           String.

        Raises:
           `EncoderError`: Encoder error.
        """
        return self.dumps('markdown', **kwargs)

    def _repr_markdown_(self) -> str:
        return self.to_markdown()  # type: ignore

    def to_rdf(self, **kwargs: Any) -> str:
        """Encodes object using RDF encoder.

        Parameters:
           kwargs: Options to RDF encoder.

        Returns:
           String.

        Raises:
           `EncoderError`: Encoder error.
        """
        return self.dumps('rdf', **kwargs)

    def substitute(
            self,
            sigma: Mapping[Any, Any] | Callable[[Any], Any]
    ) -> Self:
        """Applies substitution `sigma` to KIF object's arguments.

        Parameters:
           sigma: Substitution.

        Returns:
           KIF object.
        """
        return type(self)(*self._substitute(
            (lambda k: sigma.get(k, k))
            if isinstance(sigma, Mapping) else sigma))

    def _substitute(self, sigma: Callable[[Any], Any]) -> Iterator[Any]:
        for x in self.args:
            y = sigma(x)
            if x == y and isinstance(y, KIF_Object):
                yield type(y)(*y._substitute(sigma))
            else:
                yield y

    def traverse(
        self,
        filter: Callable[[Any], bool] | None = None,
        visit: Callable[[Any], bool] | None = None
    ) -> Iterator[Any]:
        """Traverses KIF object-tree recursively.

        Parameters:
           filter: Predicate indicating KIF objects or values to yield.
           visit: Predicate indicating KIF objects to visit.

        Returns:
           An iterator of KIF objects and values.
        """
        filter = self._check_optional_arg_callable(
            filter, type(self)._traverse_default_filter,
            self.traverse, 'filter', 1)
        visit = self._check_optional_arg_callable(
            visit, type(self)._traverse_default_visit,
            self.traverse, 'visit', 2)
        assert filter is not None
        assert visit is not None
        return self._traverse(filter, visit)

    @staticmethod
    def _traverse_default_filter(arg: Any) -> bool:
        return True

    @staticmethod
    def _traverse_default_visit(arg: Any) -> bool:
        return True

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


class KIF_JSON_Encoder(
        object.JSON_Encoder,
        format='json',
        description='JSON encoder'
):
    """KIF JSON encoder."""

    class Encoder(object.JSON_Encoder.Encoder):
        """The underlying JSON encoder."""

        @override
        def default(self, o: Any) -> Any:
            if isinstance(o, Object):
                obj = cast(Object, o)
                return {
                    'class': type(obj).__qualname__,
                    'args': obj.args,
                }
            elif isinstance(o, (datetime.datetime, decimal.Decimal)):
                return str(o)
            elif isinstance(o, enum.Enum):
                return str(o.value)
            else:
                try:
                    return json.JSONEncoder.default(self, o)
                except TypeError as err:
                    raise EncoderError(str(err)) from None


class KIF_ReprDecoder(
        object.ReprDecoder,
        format='repr',
        description='Repr. decoder'
):
    """KIF repr. decoder."""

    @classmethod
    @functools.cache
    def _globals(cls) -> dict[str, Any]:
        return {'Decimal': decimal.Decimal, 'datetime': datetime,
                **super()._globals()}


class KIF_ReprEncoder(
        object.ReprEncoder,
        format='repr',
        description='Repr. encoder'
):
    """KIF repr. encoder."""

    @override
    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0
    ) -> Iterator[str]:
        if isinstance(v, (datetime.datetime, decimal.Decimal)):
            yield from self._indent(n, indent)
            yield repr(v)
        elif isinstance(v, enum.Enum):
            yield from self._indent(n, indent)
            yield repr(v.value)
        else:
            yield from super()._iterencode(v, n, indent)


class KIF_SExpEncoder(
        object.SExpEncoder,
        format='sexp',
        description='S-expression encoder'
):
    """KIF S-expression encoder."""

    @override
    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0
    ) -> Iterator[str]:
        if isinstance(v, (datetime.datetime, decimal.Decimal)):
            yield from self._indent(n, indent)
            yield str(v)
        elif isinstance(v, enum.Enum):
            yield from self._indent(n, indent)
            yield str(v.value)
        else:
            yield from super()._iterencode(v, n, indent)
