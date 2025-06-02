# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import asyncio
import dataclasses
import functools
import logging
import pathlib

from typing_extensions import overload

from ... import itertools
from ...context.registry import EntityRegistry
from ...model import Entity, Filter
from ...model import Graph as KIF_Graph
from ...model import (
    Item,
    KIF_Object,
    Lexeme,
    Property,
    Statement,
    TDatatype,
    TGraph,
    TItem,
    TProperty,
    TText,
)
from ...typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Callable,
    cast,
    Coroutine,
    Final,
    Iterable,
    Iterator,
    override,
    TextIO,
    TypeAlias,
    TypeVar,
    Union,
)
from ..abc import Store

E = TypeVar('E', bound=Entity)
T: TypeAlias = Any

_logger: Final[logging.Logger] = logging.getLogger(__name__)


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
    class Preamble(Source):
        """Preamble source (sentinel)."""

    class Postamble(Source):
        """Postamble source (sentinel)."""

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
        '_registered',
        '_registry',
        '_scheduled',
    )

    #: Input sources.
    _args: list[Source]

    #: Other keyword arguments.
    _kwargs: Any

    #: Parsing function.
    _parse_fn: ParseFn

    #: Registered entities.
    _registered: set[Entity]

    #: Entity registry.
    _registry: EntityRegistry

    #: Scheduled statements.
    _scheduled: set[Statement]

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
        self._push_preamble()
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
        self._push_postamble()
        if parse is None:
            self._parse_fn = self._parse
        else:
            self._parse_fn = parse
        self._registered = set()
        self._registry = EntityRegistry()
        self._scheduled = set()

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

    def _push_preamble(self) -> None:
        self._args.append(self.Preamble())

    def _push_postamble(self) -> None:
        self._args.append(self.Postamble())

    def _push_location(self, location: pathlib.PurePath | str) -> None:
        self._args.append(self.Location(location))

    def _push_file(self, file: BinaryIO | TextIO) -> None:
        self._args.append(self.File(file))

    def _push_data(self, data: bytes | str) -> None:
        self._args.append(self.Data(data))

    def _push_graph(self, graph: KIF_Graph) -> None:
        self._args.append(self.Graph(graph))

    @overload
    def _register(self, entity: Item, **kwargs: Any) -> Item:
        ...

    @overload
    def _register(self, entity: Property, **kwargs: Any) -> Property:
        ...

    @overload
    def _register(self, entity: Lexeme, **kwargs: Any) -> Lexeme:
        ...

    def _register(
            self,
            entity: E,
            label: TText | None = None,
            labels: Iterable[TText] | None = None,
            alias: TText | None = None,
            aliases: Iterable[TText] | None = None,
            description: TText | None = None,
            descriptions: Iterable[TText] | None = None,
            range: TDatatype | None = None,
            inverse: TProperty | None = None,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None,
            **kwargs: Any
    ) -> E:
        self._registered.add(entity)
        return self._registry.register(  # type: ignore
            entity,                      # type: ignore
            label=label,
            labels=labels,
            alias=alias,
            aliases=aliases,
            description=description,
            descriptions=descriptions,
            range=range,
            inverse=inverse,
            lemma=lemma,
            category=category,
            language=language,
            function=self._register,
            **kwargs)

    @overload
    def _register_descriptor(
            self,
            entity: Item,
            descriptor: Item.Descriptor | None = None
    ) -> Item:
        ...

    @overload
    def _register_descriptor(
            self,
            entity: Property,
            descriptor: Property.Descriptor | None = None
    ) -> Property:
        ...

    @overload
    def _register_descriptor(
            self,
            entity: Lexeme,
            descriptor: Lexeme.Descriptor | None = None
    ) -> Lexeme:
        ...

    def _register_descriptor(
            self,
            entity: E,
            descriptor: Item.Descriptor
            | Property.Descriptor | Lexeme.Descriptor | None = None
    ) -> E:
        assert isinstance(entity, (Item, Property, Lexeme))
        if descriptor is None:
            descriptor = entity.describe()
        if descriptor is not None:
            if isinstance(entity, (Item, Property)):
                t = cast(
                    Union[Item.Descriptor, Property.Descriptor], descriptor)
                if 'labels' in t:
                    self._register(entity, labels=t['labels'].values())
                if 'aliases' in t:
                    self._register(
                        entity, aliases=itertools.chain(
                            *t['aliases'].values()))
                if 'description' in t:
                    self._register(
                        entity, description=t['descriptions'].values())
                if isinstance(entity, Property):
                    t = cast(Property.Descriptor, descriptor)
                    if 'range' in t:
                        self._register(entity, range=t['range'])
                    if 'inverse' in t:
                        self._register(entity, inverse=t['inverse'])
            elif isinstance(entity, Lexeme):
                l = cast(Lexeme.Descriptor, descriptor)
                if 'lemma' in l:
                    self._register(entity, lemma=l['lemma'])
                if 'category' in l:
                    self._register(entity, category=l['category'])
                if 'language' in l:
                    self._register(entity, language=l['language'])
        return entity           # type: ignore

    def _schedule(self, statement: Statement) -> None:
        self._scheduled.add(statement)

    def _load(self, file: TextIO) -> Iterable[T]:
        return file

    def _preamble(self) -> Iterable[Statement]:
        return iter(())

    def _describe(self) -> Iterable[Entity]:
        return iter(())

    def _parse(self, input: T) -> Iterable[Statement]:
        assert isinstance(input, str)
        yield Statement.from_json(input, **self._kwargs)

    def _postamble(self) -> Iterable[Statement]:
        return iter(())

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

        if isinstance(arg, self.Preamble):
            yield from wrap(iter(self._preamble()))
            for entity in self._describe():
                assert isinstance(entity, (Item, Property, Lexeme))
                self._register_descriptor(entity)
        elif isinstance(arg, self.Postamble):
            for entity in self._registered:
                f = functools.partial(Statement, entity)
                it = entity.descriptor_to_snaks(  # type: ignore
                    self._registry.describe(entity))  # type: ignore
                yield from wrap(map(f, it))
            yield from wrap(iter(self._scheduled))
            yield from wrap(iter(self._postamble()))
        elif isinstance(arg, self.Location):
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
        else:
            it = map(lambda stmt: stmt.unannotate(), it)
        if options.limit is not None:
            it = itertools.islice(it, options.limit)
        return it

    def _filter_parse(
            self,
            filter: Filter,
            options: Store.Options,
            file: TextIO
    ) -> Iterator[Statement]:
        for t in self._load(file):
            yield from self._parse_fn(t)

    @override
    def _afilter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Statement]:
        distinct = options.distinct
        limit =\
            options.limit if options.limit is not None else options.max_limit
        parse = functools.partial(self._filter_parse_arg, filter, options)

        async def task(
                it: Iterator[Statement]
        ) -> tuple[Iterator[Statement], list[Statement]]:
            _logger.debug(
                '%s():reading %d statements asynchronously',
                task.__qualname__, options.page_size)
            return await asyncio.to_thread(
                lambda: (it, itertools.take(options.page_size, it)))

        assert len(self._args) >= 3
        pre, mid, pos = (self._args[0],), self._args[1:-1], (self._args[-1],)
        f = (lambda it: self._afilter_helper(list(map(parse, it)), task))
        return itertools.amix(
            f(pre), f(mid), f(pos),
            distinct=distinct, limit=limit, method='chain')

    async def _afilter_helper(
            self,
            its: list[Iterator[Statement]],
            task: Callable[[Iterator[Statement]], Coroutine[
                None, None, tuple[Iterator[Statement], list[Statement]]]]
    ) -> AsyncIterator[Statement]:
        while its:
            for it, batch in await asyncio.gather(*map(task, its)):
                if batch:
                    for stmt in batch:
                        yield stmt
                else:
                    its.remove(it)


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
