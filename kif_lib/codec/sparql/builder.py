# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# RDFLib-based SPARQL builder.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

import decimal
import datetime

from abc import ABC, abstractmethod
from collections.abc import Generator, Iterator, MutableSequence, Sequence
from itertools import chain
from typing import Any, cast, Optional, Union, TypeVar

from rdflib import BNode, Literal, URIRef, Variable
from typing_extensions import override, TypeAlias

T = TypeVar('T')
TGenStr: TypeAlias = Generator[str, None, None]

T_URI: TypeAlias = Union[URIRef, str]
TBNode: TypeAlias = BNode
TLiteral: TypeAlias = Union[
    Literal, bool, datetime.datetime, decimal.Decimal, float, int, str]
TVariable: TypeAlias = Union[Variable, str]

TNumericLiteralContent: TypeAlias = Union[URIRef, TLiteral, Variable]
TNumericLiteral: TypeAlias = Union[
    'NumericLiteral', URIRef, TLiteral, Variable]
TNumericExpression: TypeAlias = Union['NumericExpression', TNumericLiteral]
TExpression: TypeAlias = Union['Expression', TNumericExpression]


TSubject: TypeAlias = Union[URIRef, BNode, Variable]
TPredicate: TypeAlias = TSubject
TObject: TypeAlias = Union[TSubject, Literal]
TTriple: TypeAlias = tuple[TSubject, TPredicate, TObject]

TDataBlockValue: TypeAlias = Optional[Union[URIRef, Literal]]
TDataBlockLine: TypeAlias = Sequence[TDataBlockValue]


class Coerce:

    @classmethod
    def _check(
            cls,
            value: T,
            ty: Union[type, tuple[type, ...]]
    ) -> T:
        if isinstance(value, ty):
            return value
        else:
            if isinstance(ty, tuple):
                expected = ' or '.join(sorted(map(
                    lambda t: t.__qualname__, ty)))
            else:
                expected = ty.__qualname__
            got = type(value).__qualname__
            raise TypeError(f'expected {expected}, got {got}')

    @classmethod
    def uri(cls, v: T_URI) -> URIRef:
        return cls._check(URIRef(v) if isinstance(v, str) else v, URIRef)

    @classmethod
    def bnode(cls, v: TBNode) -> BNode:
        return cls._check(v, BNode)

    @classmethod
    def literal(cls, v: TLiteral) -> Literal:
        return Literal(cls._check(v, (
            Literal, bool, datetime.datetime, decimal.Decimal,
            float, int, str)))

    @classmethod
    def variable(cls, v: TVariable) -> Variable:
        return cls._check(Variable(v) if isinstance(v, str) else v, Variable)

    @classmethod
    def expression(cls, v: TExpression) -> 'Expression':
        if isinstance(v, Expression):
            return v
        else:
            return cls.numeric_expression(v)

    @classmethod
    def numeric_expression(cls, v: TNumericExpression) -> 'NumericExpression':
        if isinstance(v, NumericExpression):
            return v
        else:
            return cls.numeric_literal(v)

    @classmethod
    def numeric_literal(cls, v: TNumericLiteral) -> 'NumericLiteral':
        if isinstance(v, NumericLiteral):
            return v
        else:
            return NumericLiteral(cls.numeric_literal_content(v))

    @classmethod
    def numeric_literal_content(
            cls,
            v: TNumericLiteralContent
    ) -> Union[URIRef, Literal, Variable]:
        if isinstance(v, (URIRef, Literal, Variable)):
            return v
        else:
            return cls.literal(v)

    @classmethod
    def subject(cls, v: TSubject, explain: str = 'bad subject') -> TSubject:
        return cls._check(v, (URIRef, BNode, Variable))

    @classmethod
    def predicate(cls, v: TPredicate) -> TPredicate:
        return cls.subject(v)

    @classmethod
    def object(cls, v: TObject) -> TObject:
        return cls._check(v, (URIRef, BNode, Literal, Variable))

    @classmethod
    def triple(cls, v: TTriple) -> TTriple:
        return cls._check(v, Sequence)

    @classmethod
    def data_block_value(cls, v: TDataBlockValue) -> TDataBlockValue:
        return cls._check(v, (URIRef, Literal, type(None)))

    @classmethod
    def data_block_line(cls, v: TDataBlockLine) -> TDataBlockLine:
        return cls._check(v, Sequence)


class Symbol:
    AND = '&&'
    AS = 'AS'
    BIND = 'BIND'
    DISTINCT = '!='
    EQUAL = '='
    FILTER = 'FILTER'
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='
    INDENT = '  '
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    OPTIONAL = 'OPTIONAL'
    OR = '||'
    STR = 'STR'
    UNDEF = 'UNDEF'
    UNION = 'UNION'
    VALUES = 'VALUES'


class Encodable(ABC):
    """Abstract base class for "encodable" objects."""

    @classmethod
    def _n3(cls, v: Union[URIRef, BNode, Literal, Variable]) -> str:
        if isinstance(v, Literal):
            return v._literal_n3(use_plain=True)
        else:
            return v.n3()

    def __str__(self):
        return self.encode()

    def encode(self) -> str:
        return ''.join(self.iterencode())

    @abstractmethod
    def iterencode(self) -> TGenStr:
        raise NotImplementedError


# == Expression ============================================================

class Expression(Encodable):
    """Abstract base class for expressions."""


class BooleanExpression(Expression):
    """Abstract base class for boolean expressions."""


# -- Logic expression ------------------------------------------------------

class LogicExpression(BooleanExpression):
    """Abstract base class for logic expressions."""

    _connective: str
    _args: Sequence[BooleanExpression]

    __slots__ = (
        '_connective',
        '_args',
    )

    def __init__(self, arg: BooleanExpression, *args: BooleanExpression):
        self._args = (arg, *args)

    @property
    def connective(self) -> str:
        return self.get_connective()

    def get_connective(self) -> str:
        return self._connective

    @property
    def args(self) -> Sequence[BooleanExpression]:
        return self.get_args()

    def get_args(self) -> Sequence[BooleanExpression]:
        return self._args

    @override
    def iterencode(self) -> TGenStr:
        if len(self.args) == 0:
            yield ''
        elif len(self.args) == 1:
            yield from self.args[0].iterencode()
        else:
            yield '('
            for i, arg in enumerate(self.args, 1):
                if i > 1:
                    yield ' '
                    yield self._connective
                    yield ' '
                yield from arg.iterencode()
            yield ')'


class Or(LogicExpression):
    _connective: str = Symbol.OR


class And(LogicExpression):
    _connective: str = Symbol.AND


# -- Relational expression -------------------------------------------------

class RelationalExpression(BooleanExpression):
    """Abstract base class for relational expressions."""

    _relation: str
    _args: tuple['NumericExpression', 'NumericExpression']

    __slots__ = (
        '_relation',
        '_args',
    )

    def __init__(self, arg1: TNumericExpression, arg2: TNumericExpression):
        self._args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2))

    @property
    def relation(self) -> str:
        return self.get_relation()

    def get_relation(self) -> str:
        return self._relation

    @property
    def args(self) -> tuple['NumericExpression', 'NumericExpression']:
        return self.get_args()

    def get_args(self) -> tuple['NumericExpression', 'NumericExpression']:
        return self._args

    @override
    def iterencode(self) -> TGenStr:
        yield '('
        yield from self.args[0].iterencode()
        yield ' '
        yield self.relation
        yield ' '
        yield from self.args[1].iterencode()
        yield ')'


class Equal(RelationalExpression):
    _relation: str = Symbol.EQUAL


class Distinct(RelationalExpression):
    _relation: str = Symbol.DISTINCT


class LessThan(RelationalExpression):
    _relation: str = Symbol.LESS_THAN


class LessThanOrEqual(RelationalExpression):
    _relation: str = Symbol.LESS_THAN_OR_EQUAL


class GreaterThan(RelationalExpression):
    _relation: str = Symbol.GREATER_THAN


class GreaterThanOrEqual(RelationalExpression):
    _relation: str = Symbol.GREATER_THAN_OR_EQUAL


# -- Numeric expression ----------------------------------------------------

class NumericExpression(Expression):
    """Abstract base class for numeric expressions."""


class BuiltInCall(NumericExpression):
    """Abstract base class for built-in calls."""

    _function: str
    _args: Sequence[NumericExpression]

    __slots__ = (
        '_function',
        '_args',
    )

    @property
    def function(self) -> str:
        return self.get_function()

    def get_function(self) -> str:
        return self._function

    @property
    def args(self) -> Sequence[NumericExpression]:
        return self.get_args()

    def get_args(self) -> Sequence[NumericExpression]:
        return self._args

    @override
    def iterencode(self) -> TGenStr:
        yield self.function
        yield '('
        for arg in self.args:
            yield from arg.iterencode()
        yield ')'


class UnaryBuiltInCall(BuiltInCall):
    """Abstract base class for 1-ary built-in calls."""

    def __init__(self, arg: NumericExpression):
        self._args = (arg,)


class BinaryBuiltInCall(BuiltInCall):
    """Abstract base class for 2-ary built-in calls."""

    def __init__(self, arg1: NumericExpression, arg2: NumericExpression):
        self._args = (arg1, arg2)


class STR(UnaryBuiltInCall):
    _function: str = 'str'


class NumericLiteral(NumericExpression):
    """Numeric literal."""

    _value: Union[URIRef, Literal, Variable]

    def __init__(self, value: TNumericLiteralContent):
        self._value = Coerce.numeric_literal_content(value)

    @property
    def value(self):
        return self.get_value()

    def get_value(self):
        return self._value

    @override
    def iterencode(self) -> TGenStr:
        yield self._n3(self.value)


# == Pattern ===============================================================

class Pattern(Encodable):
    """Abstract base class for patterns."""

    _query: 'Query'
    _parent: Optional['GraphPattern']

    __slots__ = (
        '_query',
        '_parent',
        '_level',
    )

    def __init__(
            self,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        self._query = query
        self._parent = parent

    @property
    def query(self) -> 'Query':
        return self.get_query()

    def get_query(self) -> 'Query':
        return self._query

    @property
    def parent(self) -> Optional['GraphPattern']:
        return self.get_parent()

    def get_parent(
            self,
            default: Optional['GraphPattern'] = None
    ) -> Optional['GraphPattern']:
        return self._parent if self._parent is not None else default


# -- Bind ------------------------------------------------------------------

class Bind(Pattern):
    """Bind pattern."""

    _expression: Expression
    _variable: Variable

    __slots__ = (
        '_expression',
        '_variable',
    )

    def __init__(
            self,
            expression: TExpression,
            variable: TVariable,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._expression = Coerce.expression(expression)
        self._variable = Coerce.variable(variable)

    @property
    def expression(self) -> Expression:
        return self.get_expression()

    def get_expression(self) -> Expression:
        return self._expression

    @property
    def variable(self) -> Variable:
        return self.get_variable()

    def get_variable(self) -> Variable:
        return self._variable

    @override
    def iterencode(self) -> TGenStr:
        yield Symbol.BIND
        yield ' ('
        yield from self.expression.iterencode()
        yield ' '
        yield Symbol.AS
        yield ' '
        yield from self._n3(self.variable)
        yield ')'


# -- DataBlockLine ---------------------------------------------------------

class DataBlockLine(Pattern):
    """Data block line pattern."""

    _args: Sequence[TDataBlockValue]

    __slots__ = (
        '_args',
    )

    def __init__(
            self,
            *args: TDataBlockValue,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._args = tuple(map(Coerce.data_block_value, args))

    @property
    def args(self) -> Sequence[TDataBlockValue]:
        return self.get_args()

    def get_args(self) -> Sequence[TDataBlockValue]:
        return self._args

    @override
    def iterencode(self) -> TGenStr:
        yield '('
        for i, value in enumerate(self.args, 1):
            if i > 1:
                yield ' '
            if value is None:
                yield Symbol.UNDEF
            else:
                yield self._n3(value)
        yield ')'


# -- Filter ----------------------------------------------------------------

class Filter(Pattern):
    """Filter pattern."""

    _expression: Expression

    __slots__ = (
        '_expression',
    )

    def __init__(
            self,
            expression: TExpression,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._expression = Coerce.expression(expression)

    @property
    def expression(self) -> Expression:
        return self.get_expression()

    def get_expression(self) -> Expression:
        return self._expression

    @override
    def iterencode(self) -> TGenStr:
        yield Symbol.FILTER
        yield ' ('
        yield from self.expression.iterencode()
        yield ')'


# -- Triple ----------------------------------------------------------------

class Triple(Pattern):
    """Triple pattern."""

    _subject: TSubject
    _predicate: TPredicate
    _object: TObject

    __slots__ = (
        '_subject',
        '_predicate',
        '_object',
    )

    def __init__(
            self,
            subject: TSubject,
            predicate: TPredicate,
            object: TObject,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._subject = Coerce.subject(subject)
        self._predicate = Coerce.predicate(predicate)
        self._object = Coerce.object(object)

    @property
    def subject(self) -> TSubject:
        return self.get_subject()

    def get_subject(self) -> TSubject:
        return self._subject

    @property
    def predicate(self) -> TPredicate:
        return self.get_predicate()

    def get_predicate(self) -> TPredicate:
        return self._predicate

    @property
    def object(self) -> TObject:
        return self.get_object()

    def get_object(self) -> TObject:
        return self._object

    @override
    def iterencode(self) -> TGenStr:
        yield self._n3(self.subject)
        yield ' '
        yield self._n3(self.predicate)
        yield ' '
        yield self._n3(self.object)
        yield ' .'


# == Graph pattern =========================================================

class GraphPattern(Pattern):
    """Abstract base class for graph patterns."""

    _binds: MutableSequence[Bind]
    _filters: MutableSequence[Filter]
    _triples: MutableSequence[Triple]
    _children: MutableSequence['GraphPattern']

    __slots__ = (
        '_binds',
        '_filters',
        '_triples',
        '_children',
    )

    def __init__(
            self,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._binds = list()
        self._filters = list()
        self._triples = list()
        self._children = list()

    def __enter__(self):
        return self.query._begin(self)

    def __exit__(self, err_type, err_val, err_bt):
        if err_val is None:
            self.query._end()
        else:
            raise err_val

    @property
    def binds(self) -> Sequence[Bind]:
        return self.get_binds()

    def get_binds(self) -> Sequence[Bind]:
        return self._binds

    def add_bind(self, bind: Bind) -> Bind:
        return cast(Bind, self._add(bind, self._binds))

    @property
    def filters(self) -> Sequence[Filter]:
        return self.get_filters()

    def get_filters(self) -> Sequence[Filter]:
        return self._filters

    def add_filter(self, filter: Filter) -> Filter:
        return cast(Filter, self._add(filter, self._filters))

    @property
    def triples(self) -> Sequence[Triple]:
        return self.get_triples()

    def get_triples(self) -> Sequence[Triple]:
        return self._triples

    def add_triple(self, triple: Triple) -> Triple:
        return cast(Triple, self._add(triple, self._triples))

    @property
    def children(self) -> Sequence['GraphPattern']:
        return self.get_children()

    def get_children(self) -> Sequence['GraphPattern']:
        return self._children

    def add_child(self, child: 'GraphPattern') -> 'GraphPattern':
        return cast(GraphPattern, self._add(child, self._children))

    def _add(self, child: Pattern, dest: MutableSequence[Any]) -> Pattern:
        assert child.query == self.query
        assert child.parent is None
        child._parent = self
        dest.append(child)
        return child

    def _subs(self) -> Iterator[Pattern]:
        return chain(self.triples, self.children, self.binds, self.filters)

    @override
    def iterencode(self) -> TGenStr:
        yield from self._iterencode(0)

    def _iterencode(self, n: int) -> TGenStr:
        yield from self._indent(n)
        yield from self._iterencode_start(n)
        for i, sub in enumerate(self._subs(), 1):
            if i > 1:
                yield from self._iterencode_sub_sep(sub, i, n)
            yield from self._iterencode_sub_start(sub, i, n)
            if isinstance(sub, GraphPattern):
                yield from sub._iterencode(n + 1)
            elif isinstance(sub, Pattern):
                yield from self._indent(n + 1)
                yield from sub.iterencode()
            else:
                raise RuntimeError('should not get here')
            yield from self._iterencode_sub_end(sub, i, n)
        yield from self._indent(n)
        yield from self._iterencode_end(n)

    def _indent(self, n: int) -> TGenStr:
        yield Symbol.INDENT * n

    def _iterencode_start(self, n: int) -> TGenStr:
        yield '{\n'

    def _iterencode_end(self, n: int) -> TGenStr:
        yield '}'

    def _iterencode_sub_start(
            self,
            child: Pattern,
            i: int,
            n: int,
    ) -> TGenStr:
        yield ''

    def _iterencode_sub_sep(
            self,
            child: Pattern,
            i: int,
            n: int,
    ) -> TGenStr:
        yield ''

    def _iterencode_sub_end(
            self,
            pattern: Pattern,
            i: int,
            n: int,
    ) -> TGenStr:
        yield '\n'


# -- Group graph pattern ---------------------------------------------------

class GroupGraphPattern(GraphPattern):
    """Group graph pattern."""


# -- Optional graph pattern ------------------------------------------------

class OptionalGraphPattern(GraphPattern):
    """Optional graph pattern."""

    @override
    def _iterencode_start(self, n: int) -> TGenStr:
        yield Symbol.OPTIONAL
        yield ' {\n'


# -- Union graph pattern ---------------------------------------------------

class UnionGraphPattern(GraphPattern):
    """Union graph pattern."""

    @override
    def add_triple(self, triple: Triple) -> Triple:
        raise SyntaxError('cannot add triples here')

    @override
    def add_child(self, child: GraphPattern) -> GraphPattern:
        assert isinstance(child, GroupGraphPattern)
        return super().add_child(child)

    @override
    def _iterencode_sub_sep(
            self,
            pattern: Pattern,
            i: int,
            n: int
    ) -> TGenStr:
        if isinstance(pattern, GroupGraphPattern):
            yield from self._indent(n)
            yield Symbol.UNION
            yield '\n'


# -- Values pattern --------------------------------------------------------

class ValuesGraphPattern(GraphPattern):
    """Values graph pattern."""

    _variables: Sequence[Variable]
    _data_block_lines: MutableSequence[DataBlockLine]

    __slots__ = (
        '_variables',
        '_data_block_lines',
    )

    def __init__(
            self,
            variable: TVariable,
            *variables: TVariable,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._variables = tuple(map(
            Coerce.variable, chain((variable,), variables)))
        self._data_block_lines = list()

    @override
    def add_bind(self, bind: Bind) -> Bind:
        raise SyntaxError('cannot add child binds here')

    @override
    def add_filter(self, filter: Filter) -> Filter:
        raise SyntaxError('cannot add filters here')

    @override
    def add_triple(self, triple: Triple) -> Triple:
        raise SyntaxError('cannot add triples here')

    @override
    def add_child(self, child: GraphPattern) -> GraphPattern:
        raise SyntaxError('cannot add child patterns here')

    @property
    def variables(self) -> Sequence[Variable]:
        return self.get_variables()

    def get_variables(self) -> Sequence[Variable]:
        return self._variables

    @property
    def data_block_lines(self) -> Sequence[DataBlockLine]:
        return self.get_data_block_lines()

    def get_data_block_lines(self) -> Sequence[DataBlockLine]:
        return self._data_block_lines

    def add_data_block_line(self, line: DataBlockLine) -> DataBlockLine:
        if len(line.args) < len(self.variables):
            raise ValueError('bad values line (too many values)')
        elif len(line.args) > len(self.variables):
            raise ValueError('bad values line (not enough values)')
        return cast(DataBlockLine, self._add(line, self._data_block_lines))

    def _subs(self) -> Iterator[Pattern]:
        return iter(self.data_block_lines)

    @override
    def _iterencode_start(self, n: int) -> TGenStr:
        yield Symbol.VALUES
        yield ' ('
        yield ' '.join(map(self._n3, self.variables))
        yield ') {\n'


# == Query =================================================================

class Query(Encodable):
    """SPARQL builder.

    See <https://www.w3.org/TR/sparql11-query/#grammar>.
    """

    _root: GroupGraphPattern
    _current: GraphPattern

    __slots__ = (
        '_root',
        '_current',
    )

    def __init__(self):
        self._root = GroupGraphPattern(self)
        self._current = self.root

    @property
    def root(self) -> GroupGraphPattern:
        return self.get_root()

    def get_root(self) -> GroupGraphPattern:
        return self._root

    @property
    def current(self) -> GraphPattern:
        return self.get_current()

    def get_current(self) -> GraphPattern:
        return self._current

    def uri(self, content: T_URI) -> URIRef:
        return Coerce.uri(content)

    def bnode(self) -> BNode:
        return BNode()

    def var(self, name: TVariable) -> Variable:
        return Coerce.variable(name)

    def triple(self, s: TSubject, p: TPredicate, o: TObject) -> 'Query':
        self.current.add_triple(Triple(s, p, o, self))
        return self

    def triples(self, *triples: TTriple) -> 'Query':
        for triple in triples:
            self.triple(*Coerce.triple(triple))
        return self

    def bind(self, expression: TExpression, variable: TVariable) -> 'Query':
        self.current.add_bind(Bind(expression, variable, self))
        return self

    def filter(self, expression: TExpression) -> 'Query':
        self.current.add_filter(Filter(expression, self))
        return self

    def group(self) -> GroupGraphPattern:
        return GroupGraphPattern(self)

    def optional(self) -> OptionalGraphPattern:
        return OptionalGraphPattern(self)

    def union(self) -> UnionGraphPattern:
        return UnionGraphPattern(self)

    def values(self, *vars: TVariable) -> ValuesGraphPattern:
        return ValuesGraphPattern(*vars, query=self)

    def begin_group(self) -> GroupGraphPattern:
        return cast(GroupGraphPattern, self._begin(self.group()))

    def end_group(self) -> GroupGraphPattern:
        assert isinstance(self.current, GroupGraphPattern)
        return cast(GroupGraphPattern, self._end())

    def begin_optional(self) -> OptionalGraphPattern:
        return cast(OptionalGraphPattern, self._begin(self.optional()))

    def end_optional(self) -> OptionalGraphPattern:
        assert isinstance(self.current, OptionalGraphPattern)
        return cast(OptionalGraphPattern, self._end())

    def begin_union(self) -> UnionGraphPattern:
        return cast(UnionGraphPattern, self._begin(self.union()))

    def end_union(self) -> UnionGraphPattern:
        assert isinstance(self.current, UnionGraphPattern)
        return cast(UnionGraphPattern, self._end())

    def begin_values(self, *vars: TVariable) -> ValuesGraphPattern:
        return cast(ValuesGraphPattern, self._begin(self.values(*vars)))

    def line(self, *values: TDataBlockValue) -> 'Query':
        assert isinstance(self.current, ValuesGraphPattern)
        current = cast(ValuesGraphPattern, self.current)
        current.add_data_block_line(DataBlockLine(*values, query=self))
        return self

    def lines(self, *lines: TDataBlockLine) -> 'Query':
        for line in lines:
            self.line(*Coerce.data_block_line(line))
        return self

    def end_values(self) -> ValuesGraphPattern:
        assert isinstance(self.current, ValuesGraphPattern)
        return cast(ValuesGraphPattern, self._end())

    def _begin(self, pattern: GraphPattern) -> GraphPattern:
        self.current.add_child(pattern)
        self._current = pattern
        return pattern

    def _end(self) -> GraphPattern:
        saved_current = self.current
        if self.current != self.root:
            assert self.current.parent is not None
            self._current = self.current.parent
        return saved_current

    @override
    def iterencode(self) -> TGenStr:
        yield from self.root.iterencode()
