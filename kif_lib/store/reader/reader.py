# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import asyncio
import contextlib
import dataclasses
import io
import logging
import pathlib

from typing_extensions import overload

from ... import functools, itertools
from ...context.registry import EntityRegistry
from ...model import Entity, Filter
from ...model import Graph as KIF_Graph
from ...model import (
    Item,
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
    ContextManager,
    Coroutine,
    Final,
    Generator,
    Iterable,
    Iterator,
    override,
    TextIO,
    TypeAlias,
    TypeVar,
    Union,
)
from ..abc import Store, TOptions

E = TypeVar('E', bound=Entity)
S = TypeVar('S')
T: TypeAlias = Any

_logger: Final[logging.Logger] = logging.getLogger(__name__)

TData: TypeAlias = Union[bytes, str]
TFile: TypeAlias = Union[BinaryIO, TextIO]
TLocation: TypeAlias = Union[pathlib.PurePath, str]


class Reader(
        Store[TOptions],
        store_name='reader',
        store_description='Reader store'
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

        location: TLocation

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
    Args: TypeAlias = Any

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
            location: TLocation | None = None,
            file: TFile | None = None,
            data: TData | None = None,
            graph: TGraph | None = None,
            parse: ParseFn | None = None,
            **kwargs: Any
    ) -> None:
        super().__init__(store_name)
        self._args = []
        self._kwargs = kwargs

        def push(src: Reader.Source) -> None:
            self._args.append(src)
        push(self.Preamble())
        if location is not None:
            push(self.Location(location))
        if file is not None:
            push(self.File(file))
        if data is not None:
            push(self.Data(data))
        if graph is not None:
            push(self.Graph(KIF_Graph.check(graph, type(self), 'graph')))
        other, stmts = map(list, itertools.partition(
            Statement.test, self._preprocess_args(*args)))
        if stmts:
            push(self.Graph(KIF_Graph(*cast(Iterable[Statement], stmts))))
        for src in other:
            push(self._check_arg(src))
        push(self.Postamble())
        self._parse_fn = parse if parse is not None else self._parse
        self._registered = set()
        self._registry = EntityRegistry()
        self._scheduled = set()

    def _preprocess_args(self, *args: Any) -> Iterator[Any]:
        yield from args

    def _check_arg(self, arg: Any) -> Source:
        if isinstance(arg, self.Source):
            return arg
        if isinstance(arg, (pathlib.PurePath, str)):
            return self.Location(arg)
        elif isinstance(arg, (BinaryIO, TextIO, io.TextIOBase)):
            return self.File(cast(TFile, arg))
        elif isinstance(arg, bytes):
            return self.Data(arg)
        elif isinstance(arg, KIF_Graph):
            return self.Graph(arg)
        else:
            return self._check_unknown_arg(arg)

    def _check_unknown_arg(self, arg: Any) -> Source:
        raise TypeError(
            f'{type(self).__qualname__} does not support '
            f'{type(arg).__qualname__}')

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
                    self._register(
                        entity, labels=t['labels'].values())  # type: ignore
                if 'aliases' in t:
                    self._register(
                        entity, aliases=itertools.chain(  # type: ignore
                            *t['aliases'].values()))
                if 'description' in t:
                    self._register(
                        entity,  # type: ignore
                        description=t['descriptions'].values())
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

    @contextlib.contextmanager
    def _load_location(
            self,
            location: TLocation
    ) -> Generator[Iterable[T], None, None]:
        fp = open(location, encoding='utf-8')
        yield iter(self._load(fp))
        fp.close()

    @contextlib.contextmanager
    def _load_file(
            self,
            file: TFile
    ) -> Generator[Iterable[T], None, None]:
        if not isinstance(file, (TextIO, io.TextIOBase)):
            file = io.TextIOWrapper(file, encoding='utf-8')
        yield iter(self._load(file))

    @contextlib.contextmanager
    def _load_data(
            self,
            data: TData
    ) -> Generator[Iterable[T], None, None]:
        if not isinstance(data, str):
            data = data.decode('utf-8')
        yield iter(self._load(io.StringIO(data)))

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
            options: TOptions
    ) -> Iterator[Statement]:
        parse = functools.partial(self._filter_parse_arg, filter, options)
        return itertools.mix(
            itertools.chain(*map(parse, self._args)),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=options.limit)

    def _filter_parse_arg(
            self,
            filter: Filter,
            options: TOptions,
            arg: Source
    ) -> Iterator[Statement]:
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
            yield from wrap(self._filter_parse_location(
                filter, options, arg.location))
        elif isinstance(arg, self.File):
            yield from wrap(self._filter_parse_file(
                filter, options, arg.file))
        elif isinstance(arg, self.Data):
            yield from wrap(self._filter_parse_data(
                filter, options, arg.data))
        elif isinstance(arg, self.Graph):
            yield from wrap(iter(arg.graph))
        else:
            yield from wrap(self._filter_parse_unknown_arg(
                filter, options, arg))

    def _filter_parse_unknown_arg(
            self,
            filter: Filter,
            options: TOptions,
            arg: Source
    ) -> Iterator[Statement]:
        return iter(())

    def _filter_parse_wrap(
            self,
            filter: Filter,
            options: TOptions,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        if filter.annotated:
            it = map(lambda stmt: stmt.annotate(), it)
        else:
            it = map(lambda stmt: stmt.unannotate(), it)
        if options.limit is not None:
            it = itertools.islice(it, options.limit)
        return itertools.filter(filter.match, it)

    def _filter_parse_location(
            self,
            filter: Filter,
            options: TOptions,
            location: TLocation
    ) -> Iterator[Statement]:
        return self._filter_parse(
            filter, options, self._load_location, location)

    def _filter_parse_file(
            self,
            filter: Filter,
            options: TOptions,
            file: TFile
    ) -> Iterator[Statement]:
        return self._filter_parse(filter, options, self._load_file, file)

    def _filter_parse_data(
            self,
            filter: Filter,
            options: TOptions,
            data: TData
    ) -> Iterator[Statement]:
        return self._filter_parse(filter, options, self._load_data, data)

    def _filter_parse(
            self,
            filter: Filter,
            options: TOptions,
            load_fn: Callable[[S], ContextManager[T]],
            arg: S
    ) -> Iterator[Statement]:
        with load_fn(arg) as it:
            return itertools.chain(*map(self._parse_fn, it))

    @override
    def _afilter(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Statement]:
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        assert limit is not None
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
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=limit, method='chain')

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
        Reader[TOptions],
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
