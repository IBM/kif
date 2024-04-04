# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# RDFLib-based SPARQL builder.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from abc import ABC, abstractmethod
from collections.abc import Generator, MutableSequence, Sequence
from itertools import chain
from typing import Any, cast, Optional, Union

from rdflib import BNode, Literal, URIRef, Variable
from typing_extensions import override, TypeAlias

TGenStr: TypeAlias = Generator[str, None, None]

TSubject: TypeAlias = Union[URIRef, BNode, Variable]
TPredicate: TypeAlias = TSubject
TObject: TypeAlias = Union[TSubject, Literal]
TTriple: TypeAlias = tuple[TSubject, TPredicate, TObject]

TNumericLiteral: TypeAlias = Union[URIRef, Literal, Variable]


class Encodable(ABC):
    """Abstract base class for "encodable" objects."""

    def __str__(self):
        return self.encode()

    def encode(self) -> str:
        return ''.join(self.iterencode())

    def iterencode(self) -> TGenStr:
        yield from self._iterencode(0)

    @abstractmethod
    def _iterencode(self, n: int) -> TGenStr:
        raise NotImplementedError

    def _indent(self, n: int) -> TGenStr:
        yield '  ' * n


# == Expression ============================================================

class Expression(Encodable):
    """Abstract base class for expressions."""


class BooleanExpression(Expression):
    """Abstract base class for boolean expressions."""


class Or(BooleanExpression):
    """Disjunction."""


class And(BooleanExpression):
    """Conjunction."""


class RelationalExpression(BooleanExpression):
    """Abstract base class for relational expressions."""


class Equal(RelationalExpression):
    """Equality."""


class Distinct(RelationalExpression):
    """Inequality."""


class LessThan(RelationalExpression):
    """Less-than."""


class LessThanOrEqual(RelationalExpression):
    """Less-than or equal."""


class GreaterThan(RelationalExpression):
    """Greater-than."""


class GreaterThanOrEqual(RelationalExpression):
    """Greater-than or equal."""


class NumericExpression(Expression):
    """Abstract base class for numeric expressions."""


class BuiltInCall(NumericExpression):
    """Abstract base class for built-in function calls."""


class STR(BuiltInCall):
    """STR."""


class NumericLiteral(NumericExpression):
    """Numeric literal."""

    _value: TNumericLiteral

    @classmethod
    def _check_numeric_literal(
            cls,
            value: TNumericLiteral
    ) -> TNumericLiteral:
        if isinstance(value, (URIRef, Literal, Variable)):
            return value
        else:
            raise TypeError(f'bad numeric literal: {value}')

    def __init__(self, value: TNumericLiteral):
        self._value = self._check_numeric_literal(value)

    @property
    def value(self):
        return self.get_value()

    def get_value(self):
        return self._value

    @override
    def _iterencode(self, n: int) -> TGenStr:
        yield self.value.n3()


class TrueLiteral(NumericExpression):
    """True."""

    @override
    def _iterencode(self, n: int) -> TGenStr:
        yield 'true'


class FalseLiteral(NumericExpression):
    """False."""

    @override
    def _iterencode(self, n: int) -> TGenStr:
        yield 'false'


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

    @classmethod
    def _check_subject(cls, subject: TSubject) -> TSubject:
        if isinstance(subject, (URIRef, BNode, Variable)):
            return subject
        else:
            raise TypeError(f'bad subject: {subject}')

    @classmethod
    def _check_predicate(cls, predicate: TPredicate) -> TPredicate:
        if isinstance(predicate, (URIRef, BNode, Variable)):
            return predicate
        else:
            raise TypeError(f'bad predicate: {predicate}')

    @classmethod
    def _check_object(cls, object: TObject) -> TObject:
        if isinstance(object, (URIRef, BNode, Literal, Variable)):
            return object
        else:
            raise TypeError(f'bad object: {object}')

    @classmethod
    def _check_triple(cls, triple: TTriple) -> 'TTriple':
        if isinstance(triple, Sequence):
            return triple
        else:
            raise TypeError(f'bad triple: {triple}')

    def __init__(
            self,
            subject: TSubject,
            predicate: TPredicate,
            object: TObject,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._subject = self._check_subject(subject)
        self._predicate = self._check_predicate(predicate)
        self._object = self._check_object(object)

    @property
    def subject(self):
        return self.get_subject()

    def get_subject(self):
        return self._subject

    @property
    def predicate(self):
        return self.get_predicate()

    def get_predicate(self):
        return self._predicate

    @property
    def object(self):
        return self.get_object()

    def get_object(self):
        return self._object

    @override
    def _iterencode(self, n: int) -> TGenStr:
        yield from self._indent(n)
        yield self._subject.n3()
        yield ' '
        yield self._predicate.n3()
        yield ' '
        yield self._object.n3()
        yield ' .'


# -- Graph pattern ---------------------------------------------------------

class GraphPattern(Pattern):
    """Base class for graph patterns."""

    _children: MutableSequence['GraphPattern']
    _triples: MutableSequence[Triple]

    __slots__ = (
        '_children',
        '_triples',
    )

    def __init__(
            self,
            query: 'Query',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(query, parent)
        self._children = list()
        self._triples = list()

    def __enter__(self):
        return self.query._begin(self)

    def __exit__(self, err_type, err_val, err_bt):
        if err_val is None:
            self.query._end()
        else:
            raise err_val

    @property
    def children(self) -> Sequence['GraphPattern']:
        return self.get_children()

    def get_children(self) -> Sequence['GraphPattern']:
        return self._children

    def add_child(self, child: 'GraphPattern') -> 'GraphPattern':
        return cast(GraphPattern, self._add(child, self._children))

    @property
    def triples(self) -> Sequence[Triple]:
        return self.get_triples()

    def get_triples(self) -> Sequence[Triple]:
        return self._triples

    def add_triple(self, triple: Triple) -> Triple:
        return cast(Triple, self._add(triple, self._triples))

    def _add(self, child: Pattern, dest: MutableSequence[Any]) -> Pattern:
        assert child.query == self.query
        assert child.parent is None
        child._parent = self
        dest.append(child)
        return child

    @override
    def _iterencode(self, n: int) -> TGenStr:
        yield from self._indent(n)
        yield from self._iterencode_start(n)
        it = chain(self.triples, self.children)
        for i, sub in enumerate(it, 1):
            if i > 1:
                yield from self._iterencode_sub_sep(sub, i, n)
            yield from self._iterencode_sub_start(sub, i, n)
            yield from sub._iterencode(n + 1)
            yield from self._iterencode_sub_end(sub, i, n)
        yield from self._indent(n)
        yield from self._iterencode_end(n)

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
        yield 'optional {\n'


# -- Union graph pattern ---------------------------------------------------

class UnionGraphPattern(GraphPattern):
    """Union graph pattern."""

    @override
    def add_child(self, child: GraphPattern) -> GraphPattern:
        assert isinstance(child, GroupGraphPattern)
        return super().add_child(child)

    @override
    def add_triple(self, triple: Triple) -> Triple:
        raise SyntaxError('cannot add triples here')

    @override
    def _iterencode_sub_sep(
            self,
            pattern: Pattern,
            i: int,
            n: int
    ) -> TGenStr:
        if isinstance(pattern, GroupGraphPattern):
            yield from self._indent(n)
            yield 'union\n'


# == Query =================================================================

class Query(Encodable):
    """SPARQL query builder.

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

    def triple(self, s: TSubject, p: TPredicate, o: TObject) -> 'Query':
        self.current.add_triple(Triple(s, p, o, self))
        return self

    def triples(self, *triples: TTriple) -> 'Query':
        for triple in triples:
            self.triple(*Triple._check_triple(triple))
        return self

    def group(self) -> GroupGraphPattern:
        return GroupGraphPattern(self)

    def optional(self) -> OptionalGraphPattern:
        return OptionalGraphPattern(self)

    def union(self) -> UnionGraphPattern:
        return UnionGraphPattern(self)

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
    def _iterencode(self, n: int) -> TGenStr:
        yield from self.root.iterencode()
