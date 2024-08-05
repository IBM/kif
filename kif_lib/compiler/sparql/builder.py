# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# RDFLib-based SPARQL query builder.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

import datetime
import decimal
import itertools
from abc import ABC, abstractmethod
from collections.abc import Iterator, MutableSequence, Sequence

from rdflib import BNode, Literal, URIRef, Variable
from typing_extensions import (
    Any,
    cast,
    Final,
    Optional,
    override,
    TypeAlias,
    TypeVar,
    Union,
)

_str = str
T = TypeVar('T')

T_URI: TypeAlias = Union[URIRef, str]
TBNode: TypeAlias = BNode
TLiteral: TypeAlias =\
    Union[Literal, bool, datetime.datetime, decimal.Decimal, float, int, str]
TVariable: TypeAlias = Union[Variable, str]

TNumericLiteralContent: TypeAlias = Union[URIRef, TLiteral, Variable]
TNumericLiteral: TypeAlias =\
    Union['NumericLiteral', URIRef, TLiteral, Variable]
TNumericExpression: TypeAlias = Union['NumericExpression', TNumericLiteral]
TNumExpr: TypeAlias = TNumericExpression
TExpression: TypeAlias = Union['Expression', TNumericExpression]

TComment: TypeAlias = Union['Comment', str]

TSubject: TypeAlias = Union[URIRef, BNode, Variable]
TPredicate: TypeAlias = TSubject
TObject: TypeAlias = Union[TSubject, Literal]
TTriple: TypeAlias = Union['Triple', tuple[TSubject, TPredicate, TObject]]

TValuesValue: TypeAlias = Optional[Union[URIRef, Literal]]
TValuesLine: TypeAlias = Union['ValuesLine', Sequence[TValuesValue]]

TInlineBind: TypeAlias = tuple[TExpression, TVariable]


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
    def iterencode(self) -> Iterator[str]:
        raise NotImplementedError


class Symbol:
    """Symbol table."""

    AND: Final[str] = '&&'
    AS: Final[str] = 'AS'
    ASK: Final[str] = 'ASK'
    BIND: Final[str] = 'BIND'
    BOUND: Final[str] = 'BOUND'
    COMMENT: Final[str] = '#'
    COUNT: Final[str] = 'COUNT'
    DISTINCT: Final[str] = 'DISTINCT'
    DOT: Final[str] = '.'
    EQUAL: Final[str] = '='
    FILTER: Final[str] = 'FILTER'
    FILTER_NOT_EXISTS: Final[str] = 'FILTER NOT EXISTS'
    GREATER_THAN: Final[str] = '>'
    GREATER_THAN_OR_EQUAL: Final[str] = '>='
    IF: Final[str] = 'IF'
    INDENT: Final[str] = '  '
    IS_BLANK: Final[str] = 'isBlank'
    IS_URI: Final[str] = 'isURI'
    LANG: Final[str] = 'LANG'
    LESS_THAN: Final[str] = '<'
    LESS_THAN_OR_EQUAL: Final[str] = '<='
    LIMIT: Final[str] = 'LIMIT'
    NOT: Final[str] = '!'
    NOT_EQUAL: Final[str] = '!='
    OFFSET: Final[str] = 'OFFSET'
    OPTIONAL: Final[str] = 'OPTIONAL'
    OR: Final[str] = '||'
    REDUCED: Final[str] = 'REDUCED'
    SELECT: Final[str] = 'SELECT'
    STAR: Final[str] = '*'
    STR: Final[str] = 'STR'
    STRLANG: Final[str] = 'STRLANG'
    STRSTARTS: Final[str] = 'STRSTARTS'
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
    def literal(cls, v: TLiteral, lang: Optional[str] = None) -> Literal:
        return Literal(cls._check(v, (
            Literal, bool, datetime.datetime, decimal.Decimal,
            float, int, str)), lang=lang)

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
    def numeric_expression(cls, v: TNumExpr) -> 'NumericExpression':
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
    def comment(
            cls,
            v: TComment,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ) -> 'Comment':
        if isinstance(v, Comment):
            text = v.text
        else:
            text = v
        return Comment(text, clause=clause, parent=parent)

    @classmethod
    def triple(
            cls,
            v: TTriple,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ) -> 'Triple':
        if isinstance(v, Triple):
            args = v.args
        else:
            args = v
        return Triple(*args, clause=clause, parent=parent)

    @classmethod
    def values_value(cls, v: TValuesValue) -> TValuesValue:
        return cls._check(v, (URIRef, Literal, type(None)))

    @classmethod
    def values_line(
            cls,
            v: TValuesLine,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ) -> 'ValuesLine':
        if isinstance(v, ValuesLine):
            args = v.args
        else:
            args = v
        return ValuesLine(*args, clause=clause, parent=parent)


# == Expression ============================================================

class Expression(Encodable):
    """Abstract base class for expressions."""

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return str(self)


class BooleanExpression(Expression):
    """Abstract base class for boolean expressions."""

    def __invert__(self):
        return Not(self)

    def __or__(self, other):
        return Or(self, other)

    def __and__(self, other):
        return And(self, other)


# -- Logic expression ------------------------------------------------------

class LogicExpression(BooleanExpression):
    """Abstract base class for logic expressions."""

    operator: str
    args: Sequence[BooleanExpression]

    def __init__(self, arg: BooleanExpression, *args: BooleanExpression):
        self.args = (arg, *args)

    def __eq__(self, other):
        return (type(self) is type(other)
                and self.operator == other.operator
                and self.args == other.args)

    @override
    def iterencode(self) -> Iterator[str]:
        if len(self.args) == 0:
            yield ''
        elif len(self.args) == 1:
            yield self.args[0].encode()
        else:
            yield '('
            yield f' {self.operator} '.join(map(Encodable.encode, self.args))
            yield ')'


class Not(LogicExpression):
    """Negation."""
    operator: str = Symbol.NOT

    def __init__(self, arg: BooleanExpression):
        super().__init__(arg)

    @override
    def iterencode(self) -> Iterator[str]:
        assert len(self.args) == 1
        yield f'{self.operator}('
        yield self.args[0].encode()
        yield ')'


class Or(LogicExpression):
    """Disjunction."""
    operator: str = Symbol.OR


class And(LogicExpression):
    """Conjunction."""
    operator: str = Symbol.AND


# -- Relational expression -------------------------------------------------

class RelationalExpression(BooleanExpression):
    """Abstract base class for relational expressions."""

    operator: str
    args: tuple['NumericExpression', 'NumericExpression']

    def __init__(self, arg1: TNumExpr, arg2: TNumExpr):
        self.args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2))

    def __eq__(self, other):
        return (type(self) is type(other)
                and self.operator == other.operator
                and self.args == other.args)

    @override
    def iterencode(self) -> Iterator[str]:
        yield '('
        yield self.args[0].encode()
        yield ' '
        yield self.operator
        yield ' '
        yield self.args[1].encode()
        yield ')'


class Equal(RelationalExpression):
    """Equality test."""
    operator: str = Symbol.EQUAL


class NotEqual(RelationalExpression):
    """Not-equal test."""
    operator: str = Symbol.NOT_EQUAL


class LessThan(RelationalExpression):
    """Less-than test."""
    operator: str = Symbol.LESS_THAN


class LessThanOrEqual(RelationalExpression):
    """Less-than-or-equal test."""
    operator: str = Symbol.LESS_THAN_OR_EQUAL


class GreaterThan(RelationalExpression):
    """Greater-than test."""
    operator: str = Symbol.GREATER_THAN


class GreaterThanOrEqual(RelationalExpression):
    """Greater-than-or-equal test."""
    operator: str = Symbol.GREATER_THAN_OR_EQUAL


# -- Numeric expression ----------------------------------------------------

class NumericExpression(BooleanExpression):
    """Abstract base class for numeric expressions."""


class NumericLiteral(NumericExpression):
    """Numeric literal."""

    value: Union[URIRef, Literal, Variable]

    def __init__(self, value: TNumericLiteralContent):
        self.value = Coerce.numeric_literal_content(value)

    def __eq__(self, other):
        return (type(self) is type(other) and self.value == other.value)

    @override
    def iterencode(self) -> Iterator[str]:
        yield self._n3(self.value)


class Call(NumericExpression):
    """Abstract base class for function calls."""

    operator: Any
    args: Sequence[NumericExpression]

    def __eq__(self, other):
        return (type(self) is type(other)
                and self.operator == other.operator
                and self.args == other.args)

    @override
    def iterencode(self) -> Iterator[str]:
        yield '('
        yield ', '.join(map(Encodable.encode, self.args))
        yield ')'


class URI_Call(Call):
    """URI function call."""

    operator: URIRef

    def __init__(self, uri: T_URI, *args: TNumExpr):
        self.operator = Coerce.uri(uri)
        self.args = tuple(map(Coerce.numeric_expression, args))

    @override
    def iterencode(self) -> Iterator[str]:
        yield self._n3(self.operator)
        yield from super().iterencode()


class BuiltInCall(Call):
    """Abstract base class for built-in function calls."""

    operator: str

    @override
    def iterencode(self) -> Iterator[str]:
        yield self.operator
        yield from super().iterencode()


class UnaryBuiltInCall(BuiltInCall):
    """Abstract base class for 1-ary built-in calls."""

    def __init__(self, arg: TNumExpr):
        self.args = (Coerce.numeric_expression(arg),)


class Aggregate(UnaryBuiltInCall):
    """Abstract base class for aggregates."""


class BinaryBuiltInCall(BuiltInCall):
    """Abstract base class for 2-ary built-in calls."""

    def __init__(self, arg1: TNumExpr, arg2: TNumExpr):
        self.args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2))


class TernaryBuiltInCall(BuiltInCall):
    """Abstract base class for 3-ary built-in calls."""

    def __init__(self, arg1: TNumExpr, arg2: TNumExpr, arg3: TNumExpr):
        self.args = (
            Coerce.numeric_expression(arg1),
            Coerce.numeric_expression(arg2),
            Coerce.numeric_expression(arg3))


class BOUND(UnaryBuiltInCall):
    """The BOUND built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-bound>.
    """
    operator: str = Symbol.BOUND


class COUNT(Aggregate):
    """The COUNT aggregate built-in."""

    operator: str = Symbol.COUNT


class COUNT_STAR(COUNT):
    """The COUNT aggregate built-in with argument set to star (*)."""

    def __init__(self):
        self.args = ()

    @override
    def iterencode(self) -> Iterator[str]:
        yield self.operator
        yield '('
        yield '*'
        yield ')'


class IF(TernaryBuiltInCall):
    """The IF built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-if>.
    """
    operator: str = Symbol.IF


class IsBlank(UnaryBuiltInCall):
    """The isURI built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-isBlank>.
    """
    operator: str = Symbol.IS_BLANK


class IsURI(UnaryBuiltInCall):
    """The isURI built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-isIRI>.
    """
    operator: str = Symbol.IS_URI


class LANG(UnaryBuiltInCall):
    """The LANG built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-lang>.
    """
    operator: str = Symbol.LANG


class STR(UnaryBuiltInCall):
    """The STR built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-str>.
    """
    operator: str = Symbol.STR


class STRSTARTS(BinaryBuiltInCall):
    """The STRSTARTS built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-strstarts>.
    """
    operator: str = Symbol.STRSTARTS


class STRLANG(BinaryBuiltInCall):
    """The STRLANG built-in.

    See <https://www.w3.org/TR/sparql11-query/#func-strlang>.
    """
    operator: str = Symbol.STRLANG


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
    def iterencode(self) -> Iterator[str]:
        yield from self._iterencode()

    def _iterencode(self, omit_bind_symbol: bool = False) -> Iterator[str]:
        if not omit_bind_symbol:
            yield Symbol.BIND
            yield ' '
        yield '('
        yield self.expression.encode()
        yield ' '
        yield Symbol.AS
        yield ' '
        yield self._n3(self.variable)
        yield ')'


# -- Comment ---------------------------------------------------------------

class Comment(Pattern):
    """Comment pattern."""

    text: str

    def __init__(
            self,
            text: str,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.text = text

    @override
    def iterencode(self) -> Iterator[str]:
        for line in self.text.splitlines():
            yield f'{Symbol.COMMENT} {line}\n'


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
    def iterencode(self) -> Iterator[str]:
        yield Symbol.FILTER
        yield ' ('
        yield self.expression.encode()
        yield ')'


# -- Triple ----------------------------------------------------------------

class Triple(Pattern):
    """Triple pattern."""

    args: tuple[TSubject, TPredicate, TObject]

    def __init__(
            self,
            subject: TSubject,
            predicate: TPredicate,
            object: TObject,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.args = (
            Coerce.subject(subject),
            Coerce.predicate(predicate),
            Coerce.object(object))

    @override
    def iterencode(self) -> Iterator[str]:
        yield ' '.join(map(self._n3, self.args))
        yield ' '
        yield Symbol.DOT


# -- Values line -----------------------------------------------------------

class ValuesLine(Pattern):
    """Values line pattern."""

    args: Sequence[TValuesValue]

    def __init__(
            self,
            *args: TValuesValue,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.args = tuple(map(Coerce.values_value, args))

    @override
    def iterencode(self) -> Iterator[str]:
        yield '('
        yield ' '.join(map(
            lambda arg: self._n3(arg) if arg is not None else Symbol.UNDEF,
            self.args))
        yield ')'


# == Graph pattern =========================================================

class GraphPattern(Pattern):
    """Abstract base class for graph patterns."""

    def __enter__(self):
        return self.clause._begin(self)

    def __exit__(self, err_type, err_val, err_bt):
        if err_val is None:
            self.clause._end()
        else:
            raise err_val

    def _add(self, child: Pattern, dest: MutableSequence[Any]) -> Pattern:
        assert child.clause == self.clause
        assert child.parent is None
        child.parent = self
        dest.append(child)
        return child

    def _add_error(
            self,
            obj: Pattern, _f=lambda x: x.__class__.__qualname__
    ) -> SyntaxError:
        return SyntaxError(f'cannot add {_f(obj)} to {_f(self)}')

    @override
    def iterencode(self) -> Iterator[str]:
        yield from self._iterencode(0)

    @abstractmethod
    def _iterencode(self, n: int) -> Iterator[str]:
        raise NotImplementedError

    def _indent(self, n: int) -> str:
        return Symbol.INDENT * n


# -- Atomic graph pattern --------------------------------------------------

class AtomicGraphPattern(GraphPattern):
    """Abstract base class for atomic graph patterns."""

    @abstractmethod
    def _push(self, pattern: Pattern) -> 'AtomicGraphPattern':
        raise NotImplementedError


# -- Comments block --------------------------------------------------------

class CommentsBlock(AtomicGraphPattern):
    """Comments block."""

    comments: MutableSequence[Comment]

    def __init__(
            self,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.comments = []

    def __call__(self, *comments: TComment) -> 'CommentsBlock':
        with self:
            return self.push(*comments)

    def add_comment(self, comment: Comment) -> Comment:
        return cast(Comment, self._add(comment, self.comments))

    def _push(self, pattern: Pattern) -> 'CommentsBlock':
        self.add_comment(cast(Comment, pattern))
        return self

    def push(self, *comments: TComment) -> 'CommentsBlock':
        for comment in comments:
            self._push(Coerce.comment(comment, clause=self.clause))
        return self

    def _iterencode(self, n: int) -> Iterator[str]:
        for comment in self.comments:
            for line in comment.iterencode():
                yield self._indent(n)
                yield line


# -- Triples block ---------------------------------------------------------

class TriplesBlock(AtomicGraphPattern):
    """Triple block."""

    triples: MutableSequence[Triple]

    def __init__(
            self,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.triples = []

    def __call__(self, *triples: TTriple) -> 'TriplesBlock':
        with self:
            return self.push(*triples)

    def add_triple(self, triple: Triple) -> Triple:
        return cast(Triple, self._add(triple, self.triples))

    def _push(self, pattern: Pattern) -> 'TriplesBlock':
        self.add_triple(cast(Triple, pattern))
        return self

    def push(self, *triples: TTriple) -> 'TriplesBlock':
        for triple in triples:
            self._push(Coerce.triple(triple, clause=self.clause))
        return self

    def _iterencode(self, n: int) -> Iterator[str]:
        for triple in self.triples:
            yield self._indent(n)
            yield from triple.iterencode()
            yield '\n'


# -- Values pattern --------------------------------------------------------

class ValuesBlock(GraphPattern):
    """VALUES block."""

    variables: Sequence[Variable]
    lines: MutableSequence[ValuesLine]

    def __init__(
            self,
            variable: TVariable,
            *variables: TVariable,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.variables = tuple(map(
            Coerce.variable, itertools.chain((variable,), variables)))
        self.lines = []

    def __call__(self, *lines: TValuesLine) -> 'ValuesBlock':
        with self:
            return self.push(*lines)

    def add_line(self, line: ValuesLine) -> ValuesLine:
        if len(line.args) < len(self.variables):
            raise ValueError('bad values line (too many values)')
        if len(line.args) > len(self.variables):
            raise ValueError('bad values line (not enough values)')
        return cast(ValuesLine, self._add(line, self.lines))

    def _push(self, line: Pattern) -> 'ValuesBlock':
        self.add_line(cast(ValuesLine, line))
        return self

    def push(self, *lines: TValuesLine) -> 'ValuesBlock':
        for line in lines:
            self._push(Coerce.values_line(line, clause=self.clause))
        return self

    def _iterencode(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield Symbol.VALUES
        yield ' ('
        yield ' '.join(map(self._n3, self.variables))
        yield ')'
        yield ' {\n'
        for line in self.lines:
            yield self._indent(n + 1)
            yield from line.iterencode()
            yield '\n'
        yield self._indent(n)
        yield '}\n'


# -- Compound graph pattern ------------------------------------------------

class CompoundGraphPattern(GraphPattern):
    """Abstract base class for compound graph patterns."""

    binds: MutableSequence[Bind]
    filters: MutableSequence[Filter]
    children: MutableSequence['GraphPattern']
    stashed_children: MutableSequence['GraphPattern']
    _stashing: bool

    def __init__(
            self,
            clause: 'Clause',
            parent: Optional['GraphPattern'] = None
    ):
        super().__init__(clause, parent)
        self.binds = []
        self.filters = []
        self.children = []
        self.stash_drop()

    def add_bind(self, bind: Bind) -> Bind:
        return cast(Bind, self._add(bind, self.binds))

    def add_filter(self, filter: Filter) -> Filter:
        return cast(Filter, self._add(filter, self.filters))

    def add_child(self, child: 'GraphPattern') -> 'GraphPattern':
        if self._stashing:
            return cast(GraphPattern, self._add(child, self.stashed_children))
        else:
            return cast(GraphPattern, self._add(child, self.children))

    def stash_begin(self):
        self._stashing = True

    def stash_end(self):
        self._stashing = False

    def stash_pop(self):
        self.children += self.stashed_children
        self.stash_drop()

    def stash_drop(self):
        self.stashed_children = []
        self._stashing = False

    def _iterencode(self, n: int) -> Iterator[str]:
        yield from self._iterencode_begin(n)
        for pat in itertools.chain(self.children, self.binds, self.filters):
            if isinstance(pat, GraphPattern):
                yield from self._iterencode_graph_pattern(pat, n + 1)
            elif isinstance(pat, Pattern):
                yield from self._iterencode_pattern(pat, n + 1)
            else:
                raise RuntimeError('should not get here')
        yield from self._iterencode_end(n)

    def _iterencode_begin(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield '{\n'

    def _iterencode_graph_pattern(
            self,
            pat: GraphPattern,
            n: int
    ) -> Iterator[str]:
        yield from pat._iterencode(n)

    def _iterencode_pattern(self, pat: Pattern, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield from pat.iterencode()
        yield '\n'

    def _iterencode_end(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield '}\n'


# -- Group graph pattern ---------------------------------------------------

class GroupGraphPattern(CompoundGraphPattern):
    """Group graph pattern."""

    @override
    def _iterencode_begin(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        if isinstance(self.parent, UnionGraphPattern):
            for child in self.parent.children:
                if isinstance(child, CommentsBlock):
                    continue
                assert isinstance(child, GroupGraphPattern)
                if self != child:
                    yield Symbol.UNION
                    yield ' '
                break
        yield '{\n'


# -- Filter-not-exists graph pattern ---------------------------------------

class FilterNotExistsGraphPattern(CompoundGraphPattern):
    """FILTER NOT EXISTS graph pattern."""

    def _iterencode_begin(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield Symbol.FILTER_NOT_EXISTS
        yield ' {\n'


# -- Optional graph pattern ------------------------------------------------

class OptionalGraphPattern(CompoundGraphPattern):
    """OPTIONAL graph pattern."""

    def _iterencode_begin(self, n: int) -> Iterator[str]:
        yield self._indent(n)
        yield Symbol.OPTIONAL
        yield ' {\n'


# -- Union graph pattern ---------------------------------------------------

class UnionGraphPattern(CompoundGraphPattern):
    """UNION graph pattern."""

    @override
    def add_child(self, child: GraphPattern) -> GraphPattern:
        if not isinstance(child, (CommentsBlock, GroupGraphPattern)):
            raise self._add_error(child)
        return super().add_child(child)


# == Clause ================================================================

class Clause(Encodable):
    """Abstract base class for clauses."""

    root: GraphPattern
    current: GraphPattern

    def __init__(self):
        self.root = GroupGraphPattern(self)
        self.current = self.root

    def _begin(self, pattern: GraphPattern) -> GraphPattern:
        if not isinstance(self.current, CompoundGraphPattern):
            raise self.current._add_error(pattern)
        self.current.add_child(pattern)
        self.current = pattern
        return pattern

    def _end(self) -> GraphPattern:
        saved_current = self.current
        if self.current != self.root:
            assert self.current.parent is not None
            self.current = self.current.parent
        return saved_current

    def stash_begin(self):
        assert isinstance(self.current, CompoundGraphPattern)
        self.current.stash_begin()

    def stash_end(self):
        assert isinstance(self.current, CompoundGraphPattern)
        self.current.stash_end()

    def stash_pop(self):
        assert isinstance(self.current, CompoundGraphPattern)
        self.current.stash_pop()

    def stash_drop(self):
        assert isinstance(self.current, CompoundGraphPattern)
        self.current.stash_drop()


class AskClause(Clause):
    """ASK clause."""

    @override
    def iterencode(self):
        yield Symbol.ASK


class SelectClause(Clause):
    """SELECT clause."""

    variables: Sequence[Union[Variable, Bind]]
    distinct: bool
    reduced: bool

    def __init__(
            self,
            *variables: Union[TVariable, TInlineBind],
            distinct: Optional[bool] = None,
            reduced: Optional[bool] = None
    ):
        super().__init__()
        self.variables = tuple(map(
            lambda v: Bind(*v, self)
            if isinstance(v, tuple) else Coerce.variable(v),
            variables))
        self.distinct = distinct if distinct is not None else False
        self.reduced = reduced if reduced is not None else False

    @override
    def iterencode(self):
        yield Symbol.SELECT
        if self.distinct:
            yield ' '
            yield Symbol.DISTINCT
        elif self.reduced:
            yield ' '
            yield Symbol.REDUCED
        if not self.variables:
            yield ' '
            yield Symbol.STAR
        else:
            for var in self.variables:
                yield ' '
                if isinstance(var, Variable):
                    yield self._n3(var)
                elif isinstance(var, Bind):
                    yield from var._iterencode(omit_bind_symbol=True)
                else:
                    raise RuntimeError('should not get here')


class WhereClause(Clause):
    """WHERE clause."""

    @override
    def iterencode(self) -> Iterator[str]:
        yield Symbol.WHERE
        yield ' '
        yield self.root.encode()


class LimitClause(Clause):
    """LIMIT clause."""

    limit: Optional[int]

    def __init__(self, limit: Optional[int] = None):
        super().__init__()
        self.limit = limit

    @override
    def iterencode(self):
        if self.limit is not None:
            yield Symbol.LIMIT
            yield ' '
            yield str(self.limit)


class OffsetClause(Clause):
    """OFFSET clause."""

    offset: Optional[int]

    def __init__(self, offset: Optional[int] = None):
        super().__init__()
        self.offset = offset

    @override
    def iterencode(self):
        if self.offset is not None:
            yield Symbol.OFFSET
            yield ' '
            yield str(self.offset)


# == Query =================================================================

class Query(Encodable):
    """Abstract base class for queries."""

    _mk_bnode: Final[type[BNode]] = BNode
    _mk_literal: Final[type[Literal]] = Literal
    _mk_uri: Final[type[URIRef]] = URIRef
    _mk_variable: Final[type[Variable]] = Variable

    BNode: TypeAlias = BNode
    Literal: TypeAlias = Literal
    URI: TypeAlias = URIRef
    Variable: TypeAlias = Variable

    TVariable: TypeAlias = Union[Variable, _str]

    VLiteral: TypeAlias = Union[Literal, Variable]
    VTerm: TypeAlias = Union[URIRef, Literal, Variable]
    V_URI: TypeAlias = Union[URIRef, Variable]

    #: Currently targeted clause.
    clause: Clause

    #: Where clause.
    where: WhereClause

    #: Limit clause.
    _limit: LimitClause

    #: Offset clause.
    _offset: OffsetClause

    #: Default fresh variable prefix.
    _fresh_var_default_prefix: _str = '_v'

    #: Fresh variable prefix.
    _fresh_var_prefix: _str

    #: Fresh variable counter.
    _fresh_var_counter: int

    def __init__(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            where: Optional[WhereClause] = None,
            fresh_var_prefix: Optional[str] = None,
            fresh_var_counter: Optional[int] = None,
    ):
        self.where = where if where is not None else WhereClause()
        self.clause = self.where
        self._limit = LimitClause(limit)
        self._offset = OffsetClause(offset)
        self._fresh_var_prefix = (
            fresh_var_prefix if fresh_var_prefix is not None
            else self._fresh_var_default_prefix)
        self._fresh_var_counter = (
            fresh_var_counter if fresh_var_counter is not None else 0)

    @override
    def iterencode(self) -> Iterator[str]:
        yield self.where.encode()
        for s in filter(bool, map(
                Encodable.encode, (self._limit, self._offset))):
            yield s
            yield '\n'

# -- Static analysis -------------------------------------------------------

    def where_is_empty(self) -> bool:
        """Tests whether the WHERE clause of query is empty.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        assert isinstance(self.where.root, GroupGraphPattern)
        return not bool(self.where.root.children)

# -- Stashing --------------------------------------------------------------

    def stash_begin(self) -> 'Query':
        self.clause.stash_begin()
        return self

    def stash_end(self) -> 'Query':
        self.clause.stash_end()
        return self

    def stash_pop(self) -> 'Query':
        self.clause.stash_pop()
        return self

    def stash_drop(self) -> 'Query':
        self.clause.stash_drop()
        return self

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

    def literal(
            self,
            content: TLiteral,
            language: Optional[str] = None
    ) -> Literal:
        """Constructs :class:`Literal`.

        Parameters:
           content: Literal content.
           language: Literal language.

        Returns:
           :class:`Literal`.
        """
        return Coerce.literal(content, language)

    def var(self, name: TVariable) -> Variable:
        """Constructs :class:`Variable`.

        Parameters:
           name: Variable name.

        Returns:
           :class:`Variable`.
        """
        return Coerce.variable(name)

    def vars(self, name: TVariable, *names: TVariable) -> Iterator[Variable]:
        """Constructs one or more variables.

        Parameter:
           name: Variable name.
           names: Variable names.

        Returns:
           Iterator of :class:`Variable`.
        """
        return map(self.var, itertools.chain((name,), names))

    def fresh_var(self) -> Variable:
        """Construct fresh variable.

        Returns:
           :class:`Variable`.
        """
        name = f'{self._fresh_var_prefix}{self._fresh_var_counter}'
        self._fresh_var_counter += 1
        return self.var(name)

    def fresh_vars(self, n: int) -> Iterator[Variable]:
        """Constructs one or more fresh variables.

        Parameters:
           n: The number of fresh variables to construct.

        Returns:
           Iterator of :class:`Variable`.
        """
        return map(lambda x: self.fresh_var(), range(n))

# -- Relational operators --------------------------------------------------

    def eq(self, arg1: TNumExpr, arg2: TNumExpr) -> Equal:
        return Equal(arg1, arg2)

# -- Functions -------------------------------------------------------------

    def bound(self, arg1: TNumExpr) -> BOUND:
        return BOUND(arg1)

    def call(self, op: T_URI, *args: TNumExpr) -> URI_Call:
        return URI_Call(op, *args)

    def count(self, arg1: Optional[TNumExpr] = None) -> COUNT:
        if arg1 is None:
            return COUNT_STAR()
        else:
            return COUNT(arg1)

    def if_(
            self,
            arg1: TNumExpr,
            arg2: TNumExpr,
            arg3: TNumExpr
    ) -> IF:
        return IF(arg1, arg2, arg3)

    def lang(self, arg: TNumExpr) -> LANG:
        return LANG(arg)

    def str(self, arg: TNumExpr) -> STR:
        return STR(arg)

    def strlang(self, arg1: TNumExpr, arg2: TNumExpr) -> STRLANG:
        return STRLANG(arg1, arg2)

    def strstarts(self, arg1: TNumExpr, arg2: TNumExpr) -> STRSTARTS:
        return STRSTARTS(arg1, arg2)

    def is_blank(self, arg: TNumExpr) -> IsBlank:
        return IsBlank(arg)

    def is_uri(self, arg: TNumExpr) -> IsURI:
        return IsURI(arg)

# -- Non-graph patterns ----------------------------------------------------

    def bind(self, expression: TExpression, variable: TVariable) -> 'Query':
        """Pushes BIND.

        Parameters:
           expression: Expression.
           variable: Variable.

        Returns:
           :class:`Query`.
        """
        bind = Bind(expression, variable, self.clause)
        if not isinstance(self.clause.current, CompoundGraphPattern):
            raise self.clause.current._add_error(bind)
        assert isinstance(self.clause.current, CompoundGraphPattern)
        self.clause.current.add_bind(bind)
        return self

    def filter(self, expression: TExpression) -> 'Query':
        """Pushes FILTER.

        Parameters:
           expression: Expression.

        Returns:
           :class:`Query`.
        """
        filter = Filter(expression, self.clause)
        if not isinstance(self.clause.current, CompoundGraphPattern):
            raise self.clause.current._add_error(filter)
        assert isinstance(self.clause.current, CompoundGraphPattern)
        self.clause.current.add_filter(filter)
        return self

# -- Atomic graph patterns -------------------------------------------------

    def comments(self) -> CommentsBlock:
        """Constructs comments block.

        Returns:
           :class:`CommentsBlock` owned by clause.
        """
        return CommentsBlock(self.clause)

    def triples(self) -> TriplesBlock:
        """Constructs triples block.

        Returns:
           :class:`TriplesBlock` owned by clause.
        """
        return TriplesBlock(self.clause)

    def values(self, *variables: TVariable) -> ValuesBlock:
        """Constructs VALUES block

        Parameters:
           variables: Variables.

        Returns:
           :class:`ValuesBlock` owned by clause.
        """
        return ValuesBlock(*variables, clause=self.clause)

# -- Compound graph patterns -----------------------------------------------

    def group(self) -> GroupGraphPattern:
        """Constructs group graph pattern.

        Returns:
           :class:`GroupGraphPattern` owned by clause.
        """
        return GroupGraphPattern(self.clause)

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

    def filter_not_exists(self) -> FilterNotExistsGraphPattern:
        """Constructs FILTER NOT EXISTS graph pattern.

        Returns:
           :class:`FilterNotExistsGraphPattern` owned by clause.
        """
        return FilterNotExistsGraphPattern(self.clause)

    def begin_filter_not_exists(self) -> FilterNotExistsGraphPattern:
        """Pushes FILTER NOT EXISTS graph pattern.

        Returns:
           :class:`FilterNotExistsGraphPattern`.
        """
        return cast(FilterNotExistsGraphPattern, self.clause._begin(
            self.filter_not_exists()))

    def end_filter_not_exists(self) -> FilterNotExistsGraphPattern:
        """Pops FILTER NOT EXISTS graph pattern.

        Returns:
           :class:`FilterNotExistsGraphPattern`.
        """
        assert isinstance(self.clause.current, FilterNotExistsGraphPattern)
        return cast(FilterNotExistsGraphPattern, self.clause._end())

    def optional(self) -> OptionalGraphPattern:
        """Constructs OPTIONAL graph pattern.

        Returns:
           :class:`OptionalGraphPattern` owned by clause.
        """
        return OptionalGraphPattern(self.clause)

    def optional_if(
            self,
            condition: bool
    ) -> Union[OptionalGraphPattern, GroupGraphPattern]:
        """Constructs OPTIONAL or graph pattern depending on `condition`.

        Parameters:
           condition: Boolean condition.

        Returns:
           :class:`OptionalGraphPattern` if `condition` is ``True``;
           :class:`GroupGraphPattern` otherwise.
        """
        return self.optional() if condition else self.group()

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

    def union(self) -> UnionGraphPattern:
        """Constructs UNION graph pattern.

        Returns:
           :class:`UnionGraphPattern` owned by clause.
        """
        return UnionGraphPattern(self.clause)

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

# -- Solution modifiers ----------------------------------------------------

    @property
    def limit(self) -> Optional[int]:
        """The LIMIT modifier."""
        return self._limit.limit

    @limit.setter
    def limit(self, limit: Optional[int]):
        self._limit.limit = limit

    @property
    def offset(self) -> Optional[int]:
        """The OFFSET modifier."""
        return self._offset.offset

    @offset.setter
    def offset(self, offset: Optional[int]):
        self._offset.offset = offset

# -- Query conversion ------------------------------------------------------

    def ask(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fresh_var_prefix: Optional[_str] = None,
            fresh_var_counter: Optional[int] = None,
            deepcopy: bool = True
    ) -> 'AskQuery':
        """Converts query to an ASK query.

        Parameters:
           limit: Limit.
           offset: Offset.
           fresh_var_prefix: Prefix of fresh variables.
           deepcopy: Whether to deep-copy the common clauses.

        Returns:
           :class:`AskQuery`.
        """
        return AskQuery(
            limit=limit if limit is not None else self._limit.limit,
            offset=offset if offset is not None else self._offset.offset,
            where=self._deepcopy(deepcopy, self.where),
            fresh_var_prefix=(
                fresh_var_prefix if fresh_var_prefix is not None
                else self._fresh_var_prefix),
            fresh_var_counter=(
                fresh_var_counter if fresh_var_counter is not None
                else self._fresh_var_counter))

    def select(
            self,
            *variables: Union[TVariable, TInlineBind],
            distinct: Optional[bool] = None,
            reduced: Optional[bool] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fresh_var_prefix: Optional[_str] = None,
            fresh_var_counter: Optional[int] = None,
            deepcopy: bool = True,
    ) -> 'SelectQuery':
        """Converts query to a SELECT query.

        Parameters:
           variables: Variables or inline binds.
           distinct: Whether to enable distinct modifier.
           reduced: Whether to enable reduced modifier.
           limit: Limit.
           offset: Offset.
           fresh_var_prefix: Prefix of fresh variables.
           deepcopy: Whether to deep-copy the common clauses.

        Returns:
           :class:`SelectQuery`.
        """
        if isinstance(self, SelectQuery):
            if distinct is None:
                distinct = self._select.distinct
            if reduced is None:
                reduced = self._select.reduced
        return SelectQuery(
            *variables,
            distinct=distinct,
            reduced=reduced,
            limit=limit if limit is not None else self._limit.limit,
            offset=offset if offset is not None else self._offset.offset,
            fresh_var_prefix=(
                fresh_var_prefix if fresh_var_prefix is not None
                else self._fresh_var_prefix),
            fresh_var_counter=(
                fresh_var_counter if fresh_var_counter is not None
                else self._fresh_var_counter),
            where=self._deepcopy(deepcopy, self.where))

    def _deepcopy(self, do_it: bool, v: T) -> T:
        from copy import deepcopy
        return deepcopy(v) if do_it else v


# == Concrete query classes ================================================

class AskQuery(Query):
    """ASK query."""

    _ask: AskClause

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ask = AskClause()

    @override
    def iterencode(self) -> Iterator[str]:
        yield self._ask.encode()
        yield ' '
        yield from super().iterencode()


class SelectQuery(Query):
    """SELECT query."""

    _select: SelectClause

    def __init__(
            self,
            *variables: Union[TVariable, tuple[TExpression, TVariable]],
            distinct: Optional[bool] = None,
            reduced: Optional[bool] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._select = SelectClause(
            *variables, distinct=distinct, reduced=reduced)

    @property
    def distinct(self) -> bool:
        """The DISTINCT modifier."""
        return self._select.distinct

    @distinct.setter
    def distinct(self, distinct: bool):
        self._select.distinct = distinct

    @property
    def reduced(self) -> bool:
        """The REDUCED modifier."""
        return self._select.reduced

    @reduced.setter
    def reduced(self, reduced: bool):
        self._select.reduced = reduced

    @override
    def iterencode(self) -> Iterator[str]:
        yield self._select.encode()
        yield ' '
        yield from super().iterencode()
