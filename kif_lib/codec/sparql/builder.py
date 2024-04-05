# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# RDFLib-based SPARQL query builder.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

import datetime
import decimal
from abc import ABC, abstractmethod
from collections.abc import Generator, Iterator, MutableSequence, Sequence
from copy import deepcopy
from functools import cache
from itertools import chain
from typing import Any, cast, Final, Optional, TypeVar, Union

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


# == Prelude ===============================================================

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


class Symbol:
    """Symbol table."""

    AND: Final[str] = '&&'
    AS: Final[str] = 'AS'
    ASK: Final[str] = 'ASK'
    BIND: Final[str] = 'BIND'
    DISTINCT: Final[str] = 'DISTINCT'
    EQUAL: Final[str] = '='
    FILTER: Final[str] = 'FILTER'
    GREATER_THAN: Final[str] = '>'
    GREATER_THAN_OR_EQUAL: Final[str] = '>='
    INDENT: Final[str] = '  '
    LESS_THAN: Final[str] = '<'
    LESS_THAN_OR_EQUAL: Final[str] = '<='
    NOT_EQUAL: Final[str] = '!='
    OPTIONAL: Final[str] = 'OPTIONAL'
    OR: Final[str] = '||'
    SELECT: Final[str] = 'SELECT'
    STR: Final[str] = 'STR'
    UNDEF: Final[str] = 'UNDEF'
    UNION: Final[str] = 'UNION'
    VALUES: Final[str] = 'VALUES'
    WHERE: Final[str] = 'WHERE'


class Coerce:
    """Type-checking and coercion functions."""

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


# == Expression ============================================================

class Expression(Encodable):
    """Abstract base class for expressions."""


class BooleanExpression(Expression):
    """Abstract base class for boolean expressions."""


# -- Logic expression ------------------------------------------------------

class LogicExpression(BooleanExpression):
    """Abstract base class for logic expressions."""

    operator: str
    args: Sequence[BooleanExpression]

    def __init__(self, arg: BooleanExpression, *args: BooleanExpression):
        self.args = (arg, *args)

    @override
    def iterencode(self) -> TGenStr:
        if len(self.args) == 0:
            yield ''
        elif len(self.args) == 1:
            yield self.args[0].encode()
        else:
            yield '('
            yield f' {self.operator} '.join(map(Encodable.encode, self.args))
            yield ')'


class Or(LogicExpression):
    operator: str = Symbol.OR


class And(LogicExpression):
    operator: str = Symbol.AND


# -- Relational expression -------------------------------------------------

class RelationalExpression(BooleanExpression):
    """Abstract base class for relational expressions."""

    operator: str
    args: tuple['NumericExpression', 'NumericExpression']

    def __init__(self, arg1: TNumericExpression, arg2: TNumericExpression):
        self.args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2))

    @override
    def iterencode(self) -> TGenStr:
        yield '('
        yield self.args[0].encode()
        yield ' '
        yield self.operator
        yield ' '
        yield self.args[1].encode()
        yield ')'


class Equal(RelationalExpression):
    operator: str = Symbol.EQUAL


class NotEqual(RelationalExpression):
    operator: str = Symbol.NOT_EQUAL


class LessThan(RelationalExpression):
    operator: str = Symbol.LESS_THAN


class LessThanOrEqual(RelationalExpression):
    operator: str = Symbol.LESS_THAN_OR_EQUAL


class GreaterThan(RelationalExpression):
    operator: str = Symbol.GREATER_THAN


class GreaterThanOrEqual(RelationalExpression):
    operator: str = Symbol.GREATER_THAN_OR_EQUAL


# -- Numeric expression ----------------------------------------------------

class NumericExpression(BooleanExpression):
    """Abstract base class for numeric expressions."""


class BuiltInCall(NumericExpression):
    """Abstract base class for built-in calls."""

    operator: str
    args: Sequence[NumericExpression]

    @override
    def iterencode(self) -> TGenStr:
        yield self.operator
        yield '('
        yield ', '.join(map(Encodable.encode, self.args))
        yield ')'


class UnaryBuiltInCall(BuiltInCall):
    """Abstract base class for 1-ary built-in calls."""

    def __init__(self, arg: TNumericExpression):
        self.args = (Coerce.numeric_expression(arg),)


class BinaryBuiltInCall(BuiltInCall):
    """Abstract base class for 2-ary built-in calls."""

    def __init__(self, arg1: TNumericExpression, arg2: TNumericExpression):
        self.args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2))


class STR(UnaryBuiltInCall):
    operator: str = 'str'


class STRSTARTS(BinaryBuiltInCall):
    operator: str = 'strstarts'


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

    clause: 'Clause'
    parent: Optional['GraphPattern']

    def __init__(
            self,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        self.clause = clause
        self.parent = parent


# -- Bind ------------------------------------------------------------------

class Bind(Pattern):
    """Bind pattern."""

    expression: Expression
    variable: Variable

    def __init__(
            self,
            expression: TExpression,
            variable: TVariable,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.expression = Coerce.expression(expression)
        self.variable = Coerce.variable(variable)

    @override
    def iterencode(self) -> TGenStr:
        yield Symbol.BIND
        yield ' ('
        yield self.expression.encode()
        yield ' '
        yield Symbol.AS
        yield ' '
        yield from self._n3(self.variable)
        yield ')'


# -- DataBlockLine ---------------------------------------------------------

class DataBlockLine(Pattern):
    """Data block line pattern."""

    args: Sequence[TDataBlockValue]

    def __init__(
            self,
            *args: TDataBlockValue,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.args = tuple(map(Coerce.data_block_value, args))

    @override
    def iterencode(self) -> TGenStr:
        yield '('
        yield ' '.join(map(
            lambda arg: self._n3(arg) if arg is not None else Symbol.UNDEF,
            self.args))
        yield ')'


# -- Filter ----------------------------------------------------------------

class Filter(Pattern):
    """Filter pattern."""

    expression: Expression

    def __init__(
            self,
            expression: TExpression,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.expression = Coerce.expression(expression)

    @override
    def iterencode(self) -> TGenStr:
        yield Symbol.FILTER
        yield ' ('
        yield self.expression.encode()
        yield ')'


# -- Triple ----------------------------------------------------------------

class Triple(Pattern):
    """Triple pattern."""

    subject: TSubject
    predicate: TPredicate
    object: TObject

    def __init__(
            self,
            subject: TSubject,
            predicate: TPredicate,
            object: TObject,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.subject = Coerce.subject(subject)
        self.predicate = Coerce.predicate(predicate)
        self.object = Coerce.object(object)

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

    binds: MutableSequence[Bind]
    filters: MutableSequence[Filter]
    triples: MutableSequence[Triple]
    children: MutableSequence['GraphPattern']

    def __init__(
            self,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.binds = list()
        self.filters = list()
        self.triples = list()
        self.children = list()

    def __enter__(self):
        return self.clause._begin(self)

    def __exit__(self, err_type, err_val, err_bt):
        if err_val is None:
            self.clause._end()
        else:
            raise err_val

    def add_bind(self, bind: Bind) -> Bind:
        return cast(Bind, self._add(bind, self.binds))

    def add_filter(self, filter: Filter) -> Filter:
        return cast(Filter, self._add(filter, self.filters))

    def add_triple(self, triple: Triple) -> Triple:
        return cast(Triple, self._add(triple, self.triples))

    def add_child(self, child: 'GraphPattern') -> 'GraphPattern':
        return cast(GraphPattern, self._add(child, self.children))

    def _add(self, child: Pattern, dest: MutableSequence[Any]) -> Pattern:
        assert child.clause == self.clause
        assert child.parent is None
        child.parent = self
        dest.append(child)
        return child

    def _subs(self) -> Iterator[Pattern]:
        return chain(
            self.triples,
            self.children,
            self.binds,
            self.filters)

    @override
    def iterencode(self) -> TGenStr:
        yield from self._iterencode(0)

    def _iterencode(self, n: int) -> TGenStr:
        yield self._indent(n)
        yield from self._iterencode_start(n)
        for i, sub in enumerate(self._subs(), 1):
            if i > 1:
                yield from self._iterencode_sub_sep(sub, i, n)
            yield from self._iterencode_sub_start(sub, i, n)
            if isinstance(sub, GraphPattern):
                yield from sub._iterencode(n + 1)
            elif isinstance(sub, Pattern):
                yield self._indent(n + 1)
                yield from sub.iterencode()
            else:
                raise RuntimeError('should not get here')
            yield from self._iterencode_sub_end(sub, i, n)
        yield self._indent(n)
        yield from self._iterencode_end(n)

    @cache
    def _indent(self, n: int) -> str:
        return Symbol.INDENT * n

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
    """OPTIONAL graph pattern."""

    @override
    def _iterencode_start(self, n: int) -> TGenStr:
        yield Symbol.OPTIONAL
        yield ' {\n'


# -- Union graph pattern ---------------------------------------------------

class UnionGraphPattern(GraphPattern):
    """UNION graph pattern."""

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
    """VALUES graph pattern."""

    variables: Sequence[Variable]
    lines: MutableSequence[DataBlockLine]

    def __init__(
            self,
            variable: TVariable,
            *variables: TVariable,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.variables = tuple(map(
            Coerce.variable, chain((variable,), variables)))
        self.lines = list()

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

    def add_line(self, line: DataBlockLine) -> DataBlockLine:
        if len(line.args) < len(self.variables):
            raise ValueError('bad values line (too many values)')
        elif len(line.args) > len(self.variables):
            raise ValueError('bad values line (not enough values)')
        return cast(DataBlockLine, self._add(line, self.lines))

    def _subs(self) -> Iterator[Pattern]:
        return iter(self.lines)

    @override
    def _iterencode_start(self, n: int) -> TGenStr:
        yield Symbol.VALUES
        yield ' ('
        yield ' '.join(map(self._n3, self.variables))
        yield ') {\n'


# == Clause ================================================================

class Clause(Encodable):
    """Abstract base class for clauses."""

    root: GraphPattern
    current: GraphPattern

    def __init__(self):
        self.root = GroupGraphPattern(self)
        self.current = self.root

    def _begin(self, pattern: GraphPattern) -> GraphPattern:
        self.current.add_child(pattern)
        self.current = pattern
        return pattern

    def _end(self) -> GraphPattern:
        saved_current = self.current
        if self.current != self.root:
            assert self.current.parent is not None
            self.current = self.current.parent
        return saved_current


class AskClause(Clause):
    """ASK clause."""

    @override
    def iterencode(self):
        yield Symbol.ASK


class SelectClause(Clause):
    """SELECT clause."""

    @override
    def iterencode(self):
        yield Symbol.SELECT


class WhereClause(Clause):
    """WHERE clause."""

    root: GroupGraphPattern

    @override
    def iterencode(self) -> TGenStr:
        yield Symbol.WHERE
        yield '\n'
        yield self.root.encode()


# == Query =================================================================

class Query(Encodable):
    """Abstract base class for queries."""

    where: WhereClause          # WHERE clause
    clause: Clause              # currently targeted clause


# -- Term constructors -----------------------------------------------------


    def uri(self, content: T_URI) -> URIRef:
        """Constructs :class:`URIRef`.

        Parameters:
           content: URI content.

        Returns:
           :class:`URIRef`.
        """
        return Coerce.uri(content)

    def bnode(self) -> BNode:
        """Constructs :class:`BNode`.

        Returns:
           :class:`BNode`.
        """
        return BNode()

    def var(self, name: TVariable) -> Variable:
        """Constructs :class:`Variable`.

        Returns:
           :class:`Variable`.
        """
        return Coerce.variable(name)

# -- Non-graph patterns ----------------------------------------------------

    def triple(
            self,
            subject: TSubject,
            predicate: TPredicate,
            object: TObject
    ) -> 'Query':
        """Pushes triple pattern.

        Parameters:
           subject: Subject.
           predicate: Predicate.
           object: Object.

        Returns:
           :class:`Query`.
        """
        self.clause.current.add_triple(
            Triple(subject, predicate, object, self.clause))
        return self

    def triples(self, *triples: TTriple) -> 'Query':
        """Pushes triple patterns.

        Parameters:
           triples: Triples.

        Returns:
           :class:`Query`.
        """
        for triple in triples:
            self.triple(*Coerce.triple(triple))
        return self

    def bind(self, expression: TExpression, variable: TVariable) -> 'Query':
        """Pushes BIND.

        Parameters:
           expression: Expression.
           variable: Variable.

        Returns:
           :class:`Query`.
        """
        self.clause.current.add_bind(Bind(expression, variable, self.clause))
        return self

    def filter(self, expression: TExpression) -> 'Query':
        """Pushes FILTER.

        Parameters:
           expression: Expression.

        Returns:
           :class:`Query`.
        """
        self.clause.current.add_filter(Filter(expression, self.clause))
        return self

# -- Graph patterns --------------------------------------------------------

    def group(self) -> GroupGraphPattern:
        """Constructs group graph pattern.

        Returns:
           :class:`GroupGraphPattern` owned by clause.
        """
        return GroupGraphPattern(self.clause)

    def optional(self) -> OptionalGraphPattern:
        """Constructs OPTIONAL graph pattern.

        Returns:
           :class:`OptionalGraphPattern` owned by clause.
        """
        return OptionalGraphPattern(self.clause)

    def union(self) -> UnionGraphPattern:
        """Constructs UNION graph pattern.

        Returns:
           :class:`UnionGraphPattern` owned by clause.
        """
        return UnionGraphPattern(self.clause)

    def values(self, *variables: TVariable) -> ValuesGraphPattern:
        """Constructs VALUES graph pattern.

        Parameters:
           variables: Variables.

        Returns:
           :class:`ValuesGraphPattern` owned by clause.
        """
        return ValuesGraphPattern(*variables, clause=self.clause)

    def begin_group(self) -> GroupGraphPattern:
        """Pushes group graph pattern.

        Returns:
           :class:`GroupGraphPattern`.
        """
        return cast(GroupGraphPattern, self.clause._begin(self.group()))

    def end_group(self) -> GroupGraphPattern:
        """Pops group graph pattern.

        Returns:
           :class:`GroupGraphPattern`.
        """
        assert isinstance(self.clause.current, GroupGraphPattern)
        return cast(GroupGraphPattern, self.clause._end())

    def begin_optional(self) -> OptionalGraphPattern:
        """Pushes OPTIONAL graph pattern.

        Returns:
           :class:`OptionalGraphPattern`.
        """
        return cast(OptionalGraphPattern, self.clause._begin(self.optional()))

    def end_optional(self) -> OptionalGraphPattern:
        """Pops OPTIONAL graph pattern.

        Returns:
           :class:`OptionalGraphPattern`.
        """
        assert isinstance(self.clause.current, OptionalGraphPattern)
        return cast(OptionalGraphPattern, self.clause._end())

    def begin_union(self) -> UnionGraphPattern:
        """Pushes UNION graph pattern.

        Returns:
           :class:`UnionGraphPattern`.
        """
        return cast(UnionGraphPattern, self.clause._begin(self.union()))

    def end_union(self) -> UnionGraphPattern:
        """Pops UNION graph pattern.

        Returns:
           :class:`UnionGraphPattern`.
        """
        assert isinstance(self.clause.current, UnionGraphPattern)
        return cast(UnionGraphPattern, self.clause._end())

    def begin_values(self, *variables: TVariable) -> ValuesGraphPattern:
        """Pushes VALUES graph pattern.

        Parameters:
           variables: Variables.

        Returns:
           :class:`ValuesGraphPattern`.
        """
        return cast(
            ValuesGraphPattern, self.clause._begin(self.values(*variables)))

    def line(self, *values: TDataBlockValue) -> 'Query':
        """Pushes VALUES line.

        Parameters:
           values: Line values.

        Returns:
           :class:`Query`.
        """
        assert isinstance(self.clause.current, ValuesGraphPattern)
        pattern = cast(ValuesGraphPattern, self.clause.current)
        pattern.add_line(DataBlockLine(*values, clause=self.clause))
        return self

    def lines(self, *lines: TDataBlockLine) -> 'Query':
        """Pushes VALUES lines.

        Parameters:
           lines: Lines.

        Returns:
           :class:`Query`.
        """
        for line in lines:
            self.line(*Coerce.data_block_line(line))
        return self

    def end_values(self) -> ValuesGraphPattern:
        """Pops VALUES graph pattern.

        Returns:
           :class:`ValuesGraphPattern`.
        """
        assert isinstance(self.clause.current, ValuesGraphPattern)
        return cast(ValuesGraphPattern, self.clause._end())

# -- Query conversion ------------------------------------------------------

    def ask(self, deepcopy=True) -> 'AskQuery':
        """Converts query to an ASK query.

        Parameters:
           deepcopy: Whether to deep-copy the common clauses.

        Returns:
           :class:`AskQuery`.
        """
        return AskQuery(where=self._deepcopy(deepcopy, self.where))

    def select(self, deepcopy=True) -> 'SelectQuery':
        """Converts query to a SELECT query.

        Parameters:
           deepcopy: Whether to deep-copy the common clauses.

        Returns:
           :class:`SelectQuery`.
        """
        return SelectQuery(where=self._deepcopy(deepcopy, self.where))

    def _deepcopy(self, do_it: bool, v: T) -> T:
        return deepcopy(v) if do_it else v


# == Concrete query classes ================================================

class AskQuery(Query):
    """ASK query."""

    _ask: AskClause

    def __init__(self, where: Optional[WhereClause] = None):
        self._ask = AskClause()
        self.where = where if where is not None else WhereClause()
        self.clause = self.where

    @override
    def iterencode(self) -> TGenStr:
        yield self._ask.encode()
        yield ' '
        yield self.where.encode()


class SelectQuery(Query):
    """SELECT query."""

    _select: SelectClause

    def __init__(
            self,
            select: Optional[SelectClause] = None,
            where: Optional[WhereClause] = None
    ):
        self._select = select if select is not None else SelectClause()
        self.where = where if where is not None else WhereClause()
        self.clause = self.where

    @override
    def iterencode(self) -> TGenStr:
        yield self._select.encode()
        yield ' '
        yield self.where.encode()
