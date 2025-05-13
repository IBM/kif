# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import collections
import dataclasses
import pathlib

from ... import itertools
from ...model import Filter, Graph, KIF_Object, Statement, TGraph
from ...typing import (
    Any,
    BinaryIO,
    Callable,
    cast,
    Iterable,
    Iterator,
    override,
    TextIO,
    TypeAlias,
    TypeVar,
    Union,
)
from ..abc import Store

T = TypeVar('T')


class Reader(
        Store,
        store_name='reader',
        store_description='Statement reader'
):
    """Statement reader.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       parse: Input parsing function.
       read: Input reading function.
       kwargs: Other keyword arguments.
    """

    @dataclasses.dataclass
    class Input(abc.ABC):
        """Abstract base class for input queue data."""

    @dataclasses.dataclass
    class LocationInput(Input):
        """Location input."""

        location: pathlib.PurePath | str

    @dataclasses.dataclass
    class FileInput(Input):
        """File input."""

        file: BinaryIO | TextIO

    @dataclasses.dataclass
    class DataInput(Input):
        """Data input."""

        data: bytes | str

    @dataclasses.dataclass
    class GraphInput(Input):
        """Graph input."""

        graph: Graph

    #: Type alias for reader arguments.
    Args: TypeAlias =\
        Union[BinaryIO, TextIO, str, bytes, pathlib.PurePath, Statement]

    #: Type alias for input parsing function.
    ParseFunction: TypeAlias = Callable[[T], Iterable[Statement]]

    #: Type alias for input reading function.
    ReadFunction: TypeAlias = Callable[[Input], Iterable[T | Statement]]

    __slots__ = (
        '_input',
        '_parse_fn',
        '_read_fn',
    )

    #: Input queue.
    _input: collections.deque[Input]

    #: Input parsing function.
    _parse_fn: ParseFunction

    #: Input reading function.
    _read_fn: ReadFunction

    def __init__(
            self,
            store_name: str,
            *args: Args,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            parse: ParseFunction | None = None,
            read: ReadFunction | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(store_name)
        self._input = collections.deque()

        def put(name: str | None, f: Callable[[T], None], x: T) -> None:
            try:
                f(x)
            except Exception as err:
                raise KIF_Object._arg_error(
                    str(err), type(self), name,
                    exception=self.Error) from err
        if location is not None:
            put('location', self._put_location, location)
        if file is not None:
            put('file', self._put_file, file)
        if data is not None:
            put('data', self._put_data, data)
        if graph is not None:
            put('graph', self._put_graph,
                Graph.check(graph, type(self), 'graph'))
        other, stmts = map(list, itertools.partition(
            lambda s: isinstance(s, Statement), args))
        if stmts:
            put('graph', self._put_graph,
                Graph(*cast(Iterable[Statement], stmts)))
        for src in other:
            put('args', self._put_arg, src)
        if parse is None:
            self._parse_fn = self._parse
        else:
            self._parse_fn = parse
        if read is None:
            self._read_fn = self._read
        else:
            self._read_fn = read

    def _put_arg(self, arg: Any) -> None:
        if isinstance(arg, (pathlib.PurePath, str)):
            self._put_location(arg)
        elif isinstance(arg, (BinaryIO, TextIO)):
            self._put_file(arg)
        elif isinstance(arg, bytes):
            self._put_data(arg)
        elif isinstance(arg, Graph):
            self._put_graph(arg)
        else:
            self._put_arg_unknown(arg)

    def _put_arg_unknown(self, arg: Any) -> None:
        raise TypeError(
            f'{type(self).__qualname__} does not support '
            f'{type(arg).__qualname__}')

    def _put_location(self, location: pathlib.PurePath | str) -> None:
        self._input.append(self.LocationInput(location))

    def _put_file(self, file: BinaryIO | TextIO) -> None:
        self._input.append(self.FileInput(file))

    def _put_data(self, data: bytes | str) -> None:
        self._input.append(self.DataInput(data))

    def _put_graph(self, graph: Graph) -> None:
        self._input.append(self.GraphInput(graph))

    def _parse(self, input: str) -> Iterable[Statement]:
        yield Statement.from_json(input)

    def _read(self, input: Input) -> Iterable[str | Statement]:
        if isinstance(input, self.LocationInput):
            with open(input.location, encoding='utf-8') as fp:
                yield from fp
        elif isinstance(input, self.FileInput):
            if isinstance(input.file, TextIO):
                yield from input.file
            else:
                import io
                yield from io.TextIOWrapper(input.file, encoding='utf-8')
        elif isinstance(input, self.DataInput):
            if isinstance(input.data, bytes):
                data: str = input.data.decode('utf-8')
            else:
                data = input.data
            yield from data.splitlines()
        elif isinstance(input, self.GraphInput):
            yield from input.graph
        else:
            raise self._should_not_get_here()

    @override
    def _filter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Statement]:
        it = self._iterate_input()
        if options.distinct:
            it = itertools.uniq(it)
        if options.limit is not None:
            limit = options.limit
        else:
            limit = options.max_limit
        count = 0
        while count < limit:
            try:
                stmt = next(it)
                if filter.annotated:
                    yield stmt.annotate()
                else:
                    yield stmt
                count += 1
            except StopIteration:
                break

    def _iterate_input(self) -> Iterator[Statement]:
        while self._input:
            input = self._input.popleft()
            for chunk in self._read(input):
                if isinstance(chunk, Statement):
                    yield chunk
                else:
                    yield from self._parse(chunk)
