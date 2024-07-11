# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc
import datetime
import decimal
import enum
import functools
import json

from typing_extensions import TYPE_CHECKING

from ..context import Context
from ..itertools import chain
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Iterator,
    Optional,
    override,
    Self,
    TypeVar,
)
from . import object

if TYPE_CHECKING:               # pragma: no cover
    from .template import Template
    from .variable import Variable

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

    #: Template class associated with this object class.
    template_class: ClassVar[type['Template']]

    #: Variable class associated with this object class.
    variable_class: ClassVar[type['Variable']]

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

    def __new__(cls, *args, **kwargs) -> Self:
        has_tpl_or_var_arg = any(map(
            cls._isinstance_template_or_variable,
            chain(args, kwargs.values())))
        if hasattr(cls, 'template_class') and has_tpl_or_var_arg:
            return cast(Self, cls.template_class(*args, **kwargs))
        elif (cls._issubclass_template(cls)
              and hasattr(cls, 'object_class') and not has_tpl_or_var_arg):
            return cls.object_class(*args, **kwargs)  # type: ignore
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

    __slots__ = (
        '_context',
    )

    _context: Context

    @abc.abstractmethod
    def __init__(self, *args: Any, context: Optional[Context] = None):
        self._context = context if context is not None else Context.top()
        super().__init__(*map(self._copy_in_context, args))

    def _copy_in_context(self, arg: T) -> T:
        if isinstance(arg, KIF_Object):
            assert isinstance(arg, KIF_Object)
            if arg.context != self.context:
                with self.context:
                    return cast(T, arg.replace())
        return arg

    @property
    def context(self) -> Context:
        """The associated KIF context."""
        return self.get_context()

    def get_context(self) -> Context:
        """Gets the associated KIF context.

        Returns:
           Context.
        """
        return self._context

    @classmethod
    def from_sparql(cls, s: str, **kwargs: Any) -> Self:
        """Decodes string using SPARQL decoder.

        Parameters:
           kwargs: Options to SPARQL decoder.

        Returns:
           The resulting object.

        Raises:
           `DecoderError`: Decoder error.
        """
        return cls.loads(s, 'sparql', **kwargs)

    def to_markdown(self, **kwargs: Any) -> str:
        """Encodes object using Markdown encoder.

        Parameters:
           kwargs: Options to Markdown encoder.

        Returns:
           The resulting string.

        Raises:
           `EncoderError`: Encoder error.
        """
        return self.dumps('markdown', **kwargs)

    def _repr_markdown_(self) -> str:
        return self.to_markdown()  # type: ignore

    @staticmethod
    def _traverse_default_filter(arg: Any) -> bool:
        return True

    @staticmethod
    def _traverse_default_visit(arg: Any) -> bool:
        return True

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
                    'class': obj.__class__.__qualname__,
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
