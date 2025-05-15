# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import asyncio
import dataclasses
import functools
import pathlib

from ... import itertools
from ...model import Filter
from ...model import Graph as KIF_Graph
from ...model import KIF_Object, Statement, TGraph
from ...typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Callable,
    cast,
    Iterable,
    Iterator,
    override,
    TextIO,
    TypeAlias,
    Union,
)
from ..abc import Store

T: TypeAlias = Any


class Reader(
        Store,
        store_name='reader',
        store_description='Reader'
):
    """Base class for readers.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       parse: Input parsing function.
       kwargs: Other keyword arguments.
    """

    @dataclasses.dataclass
    class Source(abc.ABC):
        """Abstract base class for input sources."""

    @dataclasses.dataclass
    class Location(Source):
        """Location source."""

        location: pathlib.PurePath | str

    @dataclasses.dataclass
    class File(Source):
        """File source."""

        file: BinaryIO | TextIO

    @dataclasses.dataclass
    class Data(Source):
        """Data source."""

        data: bytes | str

    @dataclasses.dataclass
    class Graph(Source):
        """Graph source."""

        graph: KIF_Graph

    #: Type alias for reader arguments.
    Args: TypeAlias =\
        Union[BinaryIO, TextIO, str, bytes, pathlib.PurePath, Statement]

    #: Type alias for input parsing function.
    ParseFn: TypeAlias = Callable[[T], Iterable[Statement]]

    __slots__ = (
        '_args',
        '_kwargs',
        '_parse_fn',
    )

    #: Input sources.
    _args: list[Source]

    #: Other keyword arguments.
    _kwargs: Any

    #: Parsing function.
    _parse_fn: ParseFn

    def __init__(
            self,
            store_name: str,
            *args: Args,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            parse: ParseFn | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(store_name)
        self._args = []
        self._kwargs = kwargs

        def push(name: str | None, f: Callable[[T], None], x: T) -> None:
            try:
                f(x)
            except Exception as err:
                raise KIF_Object._arg_error(
                    str(err), type(self), name,
                    exception=self.Error) from err
        if location is not None:
            push('location', self._push_location, location)
        if file is not None:
            push('file', self._push_file, file)
        if data is not None:
            push('data', self._push_data, data)
        if graph is not None:
            push('graph', self._push_graph, KIF_Graph.check(
                graph, type(self), 'graph'))
        other, stmts = map(list, itertools.partition(
            lambda s: isinstance(s, Statement), args))
        if stmts:
            push('graph', self._push_graph, KIF_Graph(
                *cast(Iterable[Statement], stmts)))
        for src in other:
            push('args', self._push_arg, src)
        if parse is None:
            self._parse_fn = self._parse
        else:
            self._parse_fn = parse

    def _push_arg(self, arg: Any) -> None:
        if isinstance(arg, (pathlib.PurePath, str)):
            self._push_location(arg)
        elif isinstance(arg, (BinaryIO, TextIO)):
            self._push_file(arg)
        elif isinstance(arg, bytes):
            self._push_data(arg)
        elif isinstance(arg, KIF_Graph):
            self._push_graph(arg)
        else:
            self._push_arg_unknown(arg)

    def _push_arg_unknown(self, arg: Any) -> None:
        raise TypeError(
            f'{type(self).__qualname__} does not support '
            f'{type(arg).__qualname__}')

    def _push_location(self, location: pathlib.PurePath | str) -> None:
        self._args.append(self.Location(location))

    def _push_file(self, file: BinaryIO | TextIO) -> None:
        self._args.append(self.File(file))

    def _push_data(self, data: bytes | str) -> None:
        self._args.append(self.Data(data))

    def _push_graph(self, graph: KIF_Graph) -> None:
        self._args.append(self.Graph(graph))

    def _load(self, file: TextIO) -> Iterable[T]:
        return file

    def _parse(self, input: T) -> Iterable[Statement]:
        assert isinstance(input, str)
        yield Statement.from_json(input, **self._kwargs)

    @override
    def _filter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Statement]:
        parse = functools.partial(self._filter_parse_arg, filter, options)
        return itertools.mix(
            itertools.chain(*map(parse, self._args)),
            distinct=options.distinct, limit=options.limit)

    def _filter_parse_arg(
            self,
            filter: Filter,
            options: Store.Options,
            arg: Source
    ) -> Iterator[Statement]:
        import io

        parse = functools.partial(self._filter_parse, filter, options)
        wrap = functools.partial(self._filter_parse_wrap, filter, options)

        if isinstance(arg, self.Location):
            with open(arg.location, encoding='utf-8') as fp:
                yield from wrap(parse(fp))
        elif isinstance(arg, self.File):
            if isinstance(arg.file, TextIO):
                yield from wrap(parse(arg.file))
            else:
                yield from wrap(parse(io.TextIOWrapper(
                    arg.file, encoding='utf-8')))
        elif isinstance(arg, self.Data):
            if isinstance(arg.data, bytes):
                yield from wrap(parse(io.StringIO(
                    arg.data.decode('utf-8'))))
            else:
                yield from wrap(parse(io.StringIO(arg.data)))
        elif isinstance(arg, self.Graph):
            yield from wrap(iter(arg.graph))
        else:
            raise self._should_not_get_here()

    def _filter_parse_wrap(
            self,
            filter: Filter,
            options: Store.Options,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        if filter.annotated:
            it = map(lambda stmt: stmt.annotate(), it)
        if options.limit is not None:
            it = itertools.islice(it, options.limit)
        return it

    def _filter_parse(
            self,
            filter: Filter,
            options: Store.Options,
            file: TextIO
    ) -> Iterator[Statement]:
        return itertools.chain(*map(self._parse_fn, self._load(file)))

    @override
    async def _afilter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Statement]:
        limit =\
            options.limit if options.limit is not None else options.max_limit
        parse = functools.partial(self._filter_parse_arg, filter, options)

        async def task(arg):
            return await asyncio.to_thread(lambda: list(parse(arg)))

        its = await asyncio.gather(*map(task, self._args))
        for stmt in itertools.mix(
                *its, distinct=options.distinct, limit=limit):
            yield stmt


class JSONL_Reader(
        Reader,
        store_name='jsonl-reader',
        store_description='JSON lines reader'
):
    """JSON lines reader.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       parse: Input parsing function.
       kwargs: Other keyword arguments.
    """
