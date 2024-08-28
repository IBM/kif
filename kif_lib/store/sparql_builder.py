# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import decimal
from collections.abc import Mapping, Sequence

from .. import itertools
from ..model import IRI, Value
from ..typing import (
    Any,
    Hashable,
    Iterable,
    Iterator,
    override,
    Self,
    TracebackType,
    TypeAlias,
)
from ..typing import Union as Uni

# See <http://www.w3.org/TR/sparql11-query/#grammar>.


class SPARQL_Builder(Sequence):
    """Legacy SPARQL builder."""

    class Term:
        """SPARQL builder term."""

        def __init__(self, id: Hashable) -> None:
            self._id = id

        def __eq__(self, other) -> bool:
            return type(self) is type(other) and self._id == other._id

        def __hash__(self) -> int:
            return hash(self._id)

        def __str__(self) -> str:
            return str(self._id)

        @property
        def id(self) -> Hashable:
            return self.get_id()

        def get_id(self) -> Hashable:
            return self._id

        @abc.abstractmethod
        def n3(self) -> str:
            raise NotImplementedError

    class BNode(Term):
        """SPARQL builder blank node."""

        def n3(self) -> str:
            return f'_:b{self.id}'

    class Variable(Term):
        """SPARQL builder variable."""

        def n3(self) -> str:
            return f'?{self.id}'

    TTrm: TypeAlias = Uni[Term, Value, int, decimal.Decimal, str]  # term

    class Block:
        """Block within a query."""

        _builder: SPARQL_Builder
        _start_lineno: int | None
        _end_lineno: int | None
        _args: tuple[Any, ...]
        _kwargs: dict[str, Any]
        _cond: bool

        def __init__(
                self,
                builder: SPARQL_Builder,
                *args: Any,
                **kwargs: Any
        ) -> None:
            self._builder = builder
            self._start_lineno = None
            self._end_lineno = None
            self._args = args
            self._kwargs = kwargs
            self._cond = kwargs.get('cond', True)

        @property
        def builder(self) -> SPARQL_Builder:
            return self.get_builder()

        def get_builder(self) -> SPARQL_Builder:
            return self._builder

        @property
        def args(self) -> tuple[Any, ...]:
            return self.get_args()

        def get_args(self) -> tuple[Any, ...]:
            return self._args

        @property
        def kwargs(self) -> dict[str, Any]:
            return self.get_kwargs()

        def get_kwargs(self) -> dict[str, Any]:
            return self._kwargs

        @property
        def enabled(self) -> bool:
            return self._cond

        @property
        def disabled(self) -> bool:
            return not self.enabled

        @property
        def start_lineno(self) -> int | None:
            return self.get_start_lineno()

        def get_start_lineno(self) -> int | None:
            return self._start_lineno

        @property
        def end_lineno(self) -> int | None:
            return self.get_end_lineno()

        def get_end_lineno(self) -> int | None:
            return self._end_lineno

        @abc.abstractmethod
        def _start(self) -> None:
            self._start_lineno = self.builder.current_lineno

        @abc.abstractmethod
        def _end(self) -> None:
            self._end_lineno = self.builder.current_lineno

        def __enter__(self) -> Self:
            if self.enabled:
                self._start()
            return self

        def __exit__(
                self,
                err_type: type[BaseException] | None,
                err_val: BaseException | None,
                err_bt: TracebackType | None
        ) -> None:
            if err_val is None:
                if self.enabled:
                    self._end()
            else:
                raise err_val   # pragma: no cover

    class OnlyIf(Block):
        """Only-if block."""

        def __init__(
                self,
                builder: SPARQL_Builder,
                cond: bool = True
        ) -> None:
            super().__init__(builder, cond=not cond)

        def _start(self) -> None:
            super()._start()
            self.builder.disable()

        def _end(self) -> None:
            self.builder.enable()
            super()._end()

    class SubjectPredicate(Block):
        """Subject-predicate block."""

        def __init__(
                self,
                builder: SPARQL_Builder,
                s: SPARQL_Builder.TTrm,
                p: SPARQL_Builder.TTrm
        ) -> None:
            super().__init__(builder, s, p, builder.bnode())

        @override
        def _start(self) -> None:
            super()._start()
            self.builder.triple(*self.args)

        @override
        def _end(self) -> None:
            super()._end()

        def pair(
                self,
                p: SPARQL_Builder.TTrm,
                o: SPARQL_Builder.TTrm
        ) -> SPARQL_Builder.SubjectPredicate:
            self.builder.triple(self.args[2], p, o)
            return self

        def pairs(
                self,
                *ps: tuple[SPARQL_Builder.TTrm, SPARQL_Builder.TTrm],
        ) -> SPARQL_Builder.SubjectPredicate:
            for p in ps:
                self.pair(*p)
            return self

    class Where(Block):
        """WHERE block."""

        def _start(self) -> None:
            super()._start()
            self.builder.where_start()

        def _end(self) -> None:
            self.builder.where_end()
            super()._end()

    class Group(Block):
        """Group (curly-braces) block."""

        def _start(self) -> None:
            super()._start()
            self.builder.group_start()

        def _end(self) -> None:
            self.builder.group_end()
            super()._end()

    class Optional(Block):
        """OPTIONAL block."""

        def _start(self) -> None:
            super()._start()
            self.builder.optional_start()

        def _end(self) -> None:
            self.builder.optional_end()
            super()._end()

    class Union(Block):
        """UNION block."""

        def __init__(
                self,
                builder: SPARQL_Builder,
                **kwargs: Any
        ) -> None:
            super().__init__(builder, **kwargs)

        def _start(self) -> None:
            self.builder.union_start()
            super()._start()

        def branch(self) -> None:
            if (self.enabled and self.start_lineno is not None
                    and self.start_lineno < self.builder.current_lineno):
                self.builder.union_branch()

        def _end(self) -> None:
            self.builder.union_end()
            super()._end()

    class Values(Block):
        """VALUES block."""

        def __init__(
                self,
                builder: SPARQL_Builder,
                x: SPARQL_Builder.TTrm,
                *xs: SPARQL_Builder.TTrm,
                **kwargs: Any
        ) -> None:
            super().__init__(builder, x, *xs, **kwargs)

        def _start(self) -> None:
            super()._start()
            self.builder.values_start(*self.args)

        def push(
                self,
                x: SPARQL_Builder.TTrm,
                *xs: SPARQL_Builder.TTrm
        ) -> None:
            if self.enabled:
                self.builder.values_push(x, *xs)

        def _end(self) -> None:
            self.builder.values_end()
            super()._end()

    __slots__ = (
        '_status',
        '_lines',
        '_level',
        '_curlv',
        '_tbstr',
        '_bcnt',
        '_bnodes',
        '_vcnt',
        '_vars',
        '_vals',
    )

    _status: bool               # whether builder is accepting pushes
    _lines: list[str]           # line buffer
    _level: list[int]           # indent level buffer
    _curlv: int                 # current level
    _tbstr: str                 # indent (tab) string
    _bcnt: int                  # bnode counter
    _bnodes: set[BNode]         # bnodes seen
    _vcnt: int                  # fresh var counter
    _vars: set[Variable]        # variables seen
    _vals: set[Value]           # values seen

    def __init__(self, indent: int | str = 2) -> None:
        self._status = True
        self._lines = []
        self._level = []
        self._curlv = 0
        self._tbstr = indent * ' ' if isinstance(indent, int) else indent
        self._bcnt = 0
        self._bnodes = set()
        self._vcnt = 0
        self._vars = set()
        self._vals = set()

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, key: Any) -> str:
        return self._lines[key]

    @property
    def status(self) -> bool:
        return self.get_status()

    def get_status(self) -> bool:
        return self._status

    @property
    def current_lineno(self) -> int:
        return self.get_current_lineno()

    def get_current_lineno(self) -> int:
        return len(self._lines)

    @property
    def current_level(self) -> int:
        return self.get_current_level()

    def get_current_level(self) -> int:
        return self._curlv

    def enable(self) -> None:
        self._status = True

    def disable(self) -> None:
        self._status = False

    def _push(self, line: str, indent: int = 0) -> SPARQL_Builder:
        if not self._status:
            return self         # nothing to do
        self._lines.append(line)
        if indent < 0:
            self._curlv += indent
        self._level.append(self._curlv)
        if indent > 0:
            self._curlv += indent
        return self

    def _lbrace(self, prefix: str = '') -> SPARQL_Builder:
        return self._push(prefix + '{', 1)

    def _rbrace(self) -> SPARQL_Builder:
        return self._push('}', -1)

    def bnode(self) -> BNode:
        name = self._bcnt
        self._bcnt += 1
        return self.BNode(name)

    def bnodes(self, n: int) -> Iterable[BNode]:
        for _ in range(n):
            yield self.bnode()

    def var(self, name: str | None = None) -> Variable:
        if name is None:
            name = f'_v{self._vcnt}'
            self._vcnt += 1
        return self.Variable(name)

    def vars(self, name: str, *names: str) -> Iterable[Variable]:
        return map(self.Variable, itertools.chain([name], names))

    def vars_dict(self, name: str, *names: str) -> Mapping[str, Variable]:
        return dict(zip(
            itertools.chain([name], names), self.vars(name, *names)))

    def has_bnode(self, bnode: BNode) -> bool:
        return bnode in self._bnodes

    def has_variable(self, var: Variable) -> bool:
        return var in self._vars

    def has_value(self, value: Value) -> bool:
        return value in self._vals

    def _n3(self, v: TTrm) -> str:
        if isinstance(v, self.BNode):
            self._bnodes.add(v)
        elif isinstance(v, self.Variable):
            self._vars.add(v)
        elif isinstance(v, Value):
            self._vals.add(v)
        if isinstance(v, int):
            return f'"{v}"^^<http://www.w3.org/2001/XMLSchema#integer>'
        elif isinstance(v, decimal.Decimal):
            return f'"{v}"^^<http://www.w3.org/2001/XMLSchema#decimal>'
        elif hasattr(v, 'n3'):
            return v.n3()       # pyright: ignore
        else:
            return str(v)

    @property
    def UNDEF(self) -> str:
        return 'UNDEF'

    # -- Typesetting -------------------------------------------------------

    def construct(
            self,
            order_by: TTrm | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> str:
        return ' '.join(self._construct(order_by, limit, offset))

    def _construct(
            self,
            order_by: TTrm | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Iterator[str]:
        yield 'construct'
        yield self.typeset()
        yield from self._select_tail(order_by, limit, offset)

    def select(
            self,
            *args: TTrm | tuple[TTrm, TTrm],
            distinct: bool = False,
            order_by: TTrm | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> str:
        return ' '.join(self._select(
            *args, distinct=distinct, order_by=order_by,
            limit=limit, offset=offset))

    def _select(
            self,
            *args: TTrm | tuple[TTrm, TTrm],
            distinct: bool = False,
            order_by: TTrm | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Iterator[str]:
        yield 'select'
        if distinct:
            yield 'distinct'
        if not args or args == ('*',):
            yield '*'
        else:
            for v in args:
                if isinstance(v, self.Variable):
                    if not self.has_variable(v):
                        raise ValueError(f"no such variable '{self._n3(v)}'")
                    yield self._n3(v)
                elif isinstance(v, tuple):
                    exp, var = v
                    yield f'({self._n3(exp)} as {self._n3(var)})'
                else:
                    yield str(v)
        yield self.typeset()
        yield from self._select_tail(order_by, limit, offset)

    def _select_tail(
            self,
            order_by: TTrm | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Iterator[str]:
        if order_by is not None:
            yield f'order by {self._n3(order_by)}'
        if limit is not None and limit >= 0:
            yield f'limit {limit}'
        if offset is not None and offset >= 0:
            yield f'offset {offset}'

    def typeset(self) -> str:
        return '\n'.join(self._typeset())

    def _typeset(self) -> Iterator[str]:
        for i in range(len(self)):
            yield self._typeset_line(i)

    def _typeset_line(self, i: int) -> str:
        return self._tbstr * self._level[i] + self._lines[i]

    # -- Clauses -----------------------------------------------------------

    def from_(self, iri: IRI) -> SPARQL_Builder:
        return self._push(f'from {self._n3(iri)}')

    # -- Patterns ----------------------------------------------------------

    def bind(self, term: TTrm, var: TTrm) -> SPARQL_Builder:
        """Binds term to variable.

        Parameters:
           term: Term.
           var: Variable.

        Returns:
           `self`.
        """
        assert isinstance(var, self.Variable)
        return self._push(f'bind({self._n3(term)} as {self._n3(var)})')

    def filter(self, val: TTrm) -> SPARQL_Builder:
        return self._push(f'filter({self._n3(val)})')

    def triple(self, s: TTrm, p: TTrm, o: TTrm) -> SPARQL_Builder:
        return self._push(f'{self._n3(s)} {self._n3(p)} {self._n3(o)} .')

    def triples(self, *ts: tuple[TTrm, TTrm, TTrm]) -> SPARQL_Builder:
        for t in ts:
            self.triple(*t)
        return self

    # -- Blocks ------------------------------------------------------------

    def only_if(self, cond: bool = True, **kwargs: Any) -> OnlyIf:
        return self.OnlyIf(self, cond=cond, **kwargs)

    def sp(self, s: TTrm, p: TTrm, **kwargs: Any) -> SubjectPredicate:
        return self.subject_predicate(s, p, **kwargs)

    def subject_predicate(
            self,
            s: TTrm,
            p: TTrm,
            **kwargs: Any
    ) -> SubjectPredicate:
        return self.SubjectPredicate(self, s, p, **kwargs)

    def where(self, **kwargs) -> Where:
        return self.Where(self, **kwargs)

    def where_start(self) -> SPARQL_Builder:
        return self._lbrace('where ')

    def where_end(self) -> SPARQL_Builder:
        return self._rbrace()

    def group(self, **kwargs) -> Group:
        return self.Group(self, **kwargs)

    def group_start(self) -> SPARQL_Builder:
        return self._lbrace()

    def group_end(self) -> SPARQL_Builder:
        return self._rbrace()

    def optional(self, **kwargs) -> Optional:
        return self.Optional(self, **kwargs)

    def optional_start(self) -> SPARQL_Builder:
        return self._lbrace('optional ')

    def optional_end(self) -> SPARQL_Builder:
        return self._rbrace()

    def union(self, **kwargs) -> Union:
        return self.Union(self, **kwargs)

    def union_start(self) -> SPARQL_Builder:
        return self._lbrace()

    def union_branch(self) -> SPARQL_Builder:
        self._rbrace()
        return self._lbrace('union ')

    def union_end(self) -> SPARQL_Builder:
        return self._rbrace()

    def values(self, x: TTrm, *xs: TTrm, **kwargs) -> Values:
        return self.Values(self, x, *xs, **kwargs)

    def values_start(self, x: TTrm, *xs: TTrm) -> SPARQL_Builder:
        return self._lbrace('values ' + self._brace(x, *xs) + ' ')

    def values_push(self, x: TTrm, *xs: TTrm) -> SPARQL_Builder:
        return self._push(self._brace(x, *xs))

    def values_end(self) -> SPARQL_Builder:
        return self._rbrace()

    # -- Builtin calls -----------------------------------------------------

    def _app(self, x: TTrm, *xs: TTrm) -> str:
        return self._n3(x) + self._brace(*xs, sep=', ')

    def _brace(self, x: TTrm, *xs: TTrm, sep=' ') -> str:
        return f'({self._join(x, *xs, sep=sep)})'

    def _join(self, *xs: TTrm, sep=' ') -> str:
        return sep.join(map(self._n3, xs))

    def _infix(self, op: str, x: TTrm, y: TTrm, *xs: TTrm) -> str:
        return self._brace(*map(
            self._brace, itertools.chain([x, y], xs)), sep=op)

    def and_(self, x: TTrm, y: TTrm, *xs: TTrm) -> str:
        return self._infix(' && ', x, y, *xs)

    def concat(self, x: TTrm, y: TTrm, *xs: TTrm) -> str:
        return self._app('concat', x, y, *xs)

    def eq(self, x: TTrm, y: TTrm) -> str:
        return self._infix(' = ', x, y)

    def isBlank(self, v: TTrm) -> str:
        return self._app('isBlank', v)

    def isURI(self, v: TTrm) -> str:
        return self._app('isURI', v)

    def lang(self, v: TTrm) -> str:
        return self._app('lang', v)

    def md5(self, v: TTrm) -> str:
        return self._app('md5', v)

    def not_(self, v: TTrm) -> str:
        return self._app('!', v)

    def or_(self, x: TTrm, y: TTrm, *xs: TTrm) -> str:
        return self._infix(' || ', x, y, *xs)

    def str_(self, v: TTrm) -> str:
        return self._app('str', v)

    def strdt(self, x: TTrm, y: TTrm) -> str:
        return self._app('strdt', x, y)

    def strlang(self, x: TTrm, y: TTrm) -> str:
        return self._app('strlang', x, y)

    def struuid(self) -> str:
        return self._app('struuid')

    def strstarts(self, x: TTrm, y: TTrm) -> str:
        return self._app('strstarts', x, y)

    def substr(self, v: TTrm, start: int, length: int | None = None) -> str:
        if length is not None:
            return self._app('substr', v, str(start), str(length))
        else:
            return self._app('substr', v, str(start))

    def uri(self, v: TTrm) -> str:
        return self._app('uri', v)

    def uuid(self) -> str:
        return self._app('uuid')

    # -- Modifiers ---------------------------------------------------------

    def limit(self, n: int) -> SPARQL_Builder:
        return self._push(f'limit {n}')

    def offset(self, n: int) -> SPARQL_Builder:
        return self._push(f'offset {n}')
