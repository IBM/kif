# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import logging
import pathlib
import sys

import httpx

from ... import itertools
from ... import namespace as NS
from ...compiler.sparql.builder import SelectQuery
from ...model import Datatype, Item, Property
from ...typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    cast,
    Collection,
    Final,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
    TextIO,
    TypeAlias,
    TypedDict,
    TypeVar,
)
from .prelude import _get_item_cache, _get_property_cache

QueryResults: TypeAlias = dict[str, Any]
T = TypeVar('T')

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class ItemEntry(TypedDict):
    item: Item | None
    label: str | None


class PropertyEntry(TypedDict):
    property: Property | None
    datatype_uri: str | None
    label: str | None
    inverse_uri: str | None


class Downloader:
    """Entity downloader."""

    class Options(TypedDict, total=False):
        """Downloader options."""

        #: Address of the Wikidata SPARQL endpoint.
        wikidata_uri: str

        #: HTTP headers.
        http_headers: dict[str, str]

        #: Results limit.
        limit: int

        #: Page size.
        page_size: int

        #: Maximum number of simultaneous async requests.
        max_requests: int

        #: Maximum number of retries for a same failed request.
        max_retries: int

        #: Request timeout (in seconds).
        timeout: int

        #: Path to output dir.
        output_dir: pathlib.Path

        #: Whether to open output files in append mode.
        append: bool

        #: QIDs of the item types to consider.
        item_types: Collection[str]

    #: Default options.
    default_options: Final[Options] = {
        'wikidata_uri': 'https://query.wikidata.org/sparql',
        'http_headers': {
            'Accept': 'application/sparql-results+json;charset=utf-8',
            'Content-Type': 'application/sparql-query;charset=utf-8',
            'User-Agent': 'CoolBot/0.0',
        },
        'limit': sys.maxsize,
        'page_size': 5000,
        'max_requests': 2,
        'max_retries': 2,
        'timeout': 60,
        'output_dir': pathlib.Path('.').absolute(),
        'append': False,
        'item_types': (),
    }

    __slots__ = (
        '_options',
    )

    #: The downloader options.
    _options: Options

    def __init__(self, options: Options | None = None) -> None:
        self._options = cast(Downloader.Options, dict(self.default_options))
        if options:
            self._options.update(options)

    @property
    def options(self) -> Options:
        """The downloader options."""
        return self.get_options()

    def get_options(self) -> Options:
        """Gets the downloader options.

        Returns:
           Options.
        """
        return self._options

    def fetch_properties(self, path: pathlib.Path | None = None) -> None:
        """Fetches property data.

        Parameters:
           path: Path.
        """
        def write(fp: TextIO, entry: PropertyEntry) -> None:
            assert 'append' in self.options
            append = self.options['append']
            assert entry['property'] is not None
            prop = entry['property']
            uri = entry['property'].iri.content
            pid = int(NS.Wikidata.get_wikidata_name(uri)[1:])
            assert prop.range is not None
            datatype_uri = str(prop.range._to_rdflib())
            inverse_uri = entry['inverse_uri'] or ''
            label = entry['label'] or ''
            if not append:
                print(
                    pid, uri, datatype_uri, label, inverse_uri,
                    sep='\t', file=fp)
        if path is None:
            path = _get_property_cache()
        assert path is not None
        self._download_helper(
            path, write, self._eval_query(
                self._generate_properties_query(),
                self._parse_properties_query_results))

    def _generate_properties_query(self) -> SelectQuery:
        q = SelectQuery(distinct=True)
        v_property, v_datatype, v_label, v_inverse = q.vars(
            'property', 'datatype', 'label', 'inverse')
        q.triples()(
            (v_property, NS.RDF.type, NS.WIKIBASE.Property),
            (v_property, NS.WIKIBASE.propertyType, v_datatype),
            (v_property, NS.RDFS.label, v_label))
        with q.optional():
            q.triples()((v_property, NS.WDT['P1696'], v_inverse))
        q.filter(q.eq(q.lang(v_label), q.literal('en')))
        return q

    def _parse_properties_query_results(
            self,
            results: QueryResults
    ) -> Iterator[PropertyEntry]:
        for t in results['results']['bindings']:
            if not ('property' in t and 'value' in t['property']):
                continue
            if not ('datatype' in t and 'value' in t['datatype']):
                continue
            try:
                datatype_uri = t['datatype']['value']
                datatype = Datatype._from_rdflib(datatype_uri)
            except TypeError:
                continue
            property = Property(t['property']['value'], datatype)
            if 'label' in t and 'value' in t['label']:
                label = t['label']['value'].strip()
            else:
                label = None
            if 'inverse' in t and t['inverse']['value']:
                inverse_uri = t['inverse']['value']
            else:
                inverse_uri = None
            yield {
                'property': property,
                'datatype_uri': datatype_uri,
                'label': label,
                'inverse_uri': inverse_uri,
            }

    def fetch_items(self, path: pathlib.Path | None = None) -> None:
        """Fetches item data.

        Parameters:
           path: Path.
        """
        def write(fp: TextIO, entry: ItemEntry) -> None:
            assert 'append' in self.options
            append = self.options['append']
            assert entry['item'] is not None
            uri = entry['item'].iri.content
            qid = int(NS.Wikidata.get_wikidata_name(uri)[1:])
            label = entry['label'] or ''
            if not append:
                print(qid, uri, label, sep='\t', file=fp)
        if path is None:
            path = _get_item_cache()
        assert path is not None
        self._download_helper(
            path, write, self._eval_query(
                self._generate_items_query(),
                self._parse_items_query_results))

    def _generate_items_query(self) -> SelectQuery:
        assert 'item_types' in self.options
        types = self.options['item_types']
        q = SelectQuery(distinct=True)
        v_item, v_label, v_type = q.vars('item', 'label', 'type')
        q.triples()(
            (v_item, NS.WIKIBASE.sitelinks, q.bnode()),
            (v_item, NS.RDFS.label, v_label))
        if types:
            with q.union():
                with q.group():
                    q.triples()((v_item, NS.WDT['P31'], v_type))
                with q.group():
                    x = q.fresh_var()
                    q.triples()(
                        (v_type, NS.WDT['P31'], x),
                        (v_item, NS.WDT['P31'], x))
            q.values(v_type)(*map(lambda t: (q.uri(NS.WD[t]),), types))
        q.filter(q.eq(q.lang(v_label), q.literal('en')))
        return q

    def _parse_items_query_results(
            self,
            results: QueryResults
    ) -> Iterator[ItemEntry]:
        for t in results['results']['bindings']:
            if not ('item' in t and 'value' in t['item']):
                continue
            item = Item(t['item']['value'])
            if 'label' in t and 'value' in t['label']:
                label = t['label']['value'].strip()
            else:
                label = None
            yield {
                'item': item,
                'label': label,
            }

    def _download_helper(
            self,
            path: pathlib.Path,
            write_fn: Callable[[TextIO, T], None],
            it: Iterator[T]
    ) -> None:
        if not path.is_absolute():
            assert 'output_dir' in self.options
            path = self.options['output_dir'] / path
        assert 'append' in self.options
        append = self.options['append']
        with open(path, 'a' if append else 'w', encoding='utf-8') as fp:
            for t in it:
                write_fn(fp, t)
                fp.flush()

    def _eval_query(
            self,
            query: SelectQuery,
            parse_fn: Callable[[QueryResults], Iterator[T]]
    ) -> Iterator[T]:
        ###
        # TODO: Is this the best way to do this?
        ###
        it = self._eval_query_async(query, parse_fn)
        loop = asyncio.new_event_loop()
        while True:
            try:
                yield loop.run_until_complete(it.__anext__())
            except StopAsyncIteration:
                break

    async def _eval_query_async(
            self,
            query: SelectQuery,
            parse_fn: Callable[[QueryResults], Iterator[T]]
    ) -> AsyncIterator[T]:
        assert 'limit' in self.options
        assert 'page_size' in self.options
        assert 'max_requests' in self.options
        assert 'max_retries' in self.options
        limit = max(self.options['limit'], 0)
        page_size = max(self.options['page_size'], 0)
        max_requests = max(self.options['max_requests'], 1)
        max_retries = max(self.options['max_retries'], 1)
        if limit == 0 or page_size == 0:
            return              # nothing to do
        assert limit > 0
        assert page_size > 0
        offsets_it = itertools.chain(itertools.count(0, page_size))
        count: int = 0
        retries: dict[int, int] = {}
        retry_pushed: bool
        while count < limit:
            retry_pushed = False
            num_requests = min(
                ((limit - count) // page_size) + 1, max_requests)
            offsets = itertools.take(num_requests, offsets_it)
            pages = await self._do_eval_query_async(query, offsets)
            last_page_seen = False
            for i, page in enumerate(pages, 0):
                if isinstance(page, httpx.RequestError):
                    offset = offsets[i]
                    _logger.warning('request with offset %d failed', offset)
                    if str(page):
                        _logger.warning(str(page))
                    if offset not in retries:
                        retries[offset] = 0
                    retries[offset] += 1
                    if retries[offset] > max_retries:
                        raise page  # too many retries
                    offsets_it = itertools.chain((offset,), offsets_it)
                    _logger.info(
                        'scheduling retry #%d for request with offset %d',
                        retries[offset], offset)
                    retry_pushed = True
                    continue
                if isinstance(page, BaseException):
                    raise page
                if ('results' not in page
                        or 'bindings' not in page['results']):
                    continue
                if len(page['results']['bindings']) < page_size:
                    last_page_seen = True
                for line in parse_fn(page):
                    yield line
                    count += 1
                    assert count <= limit
                    if count == limit:
                        return
            if last_page_seen and not retry_pushed:
                return          # done

    async def _do_eval_query_async(
            self,
            query: SelectQuery,
            offsets: Sequence[int]
    ) -> Iterable[QueryResults | BaseException]:
        pages = await self._httpx_gather_async(
            map(lambda offset:
                lambda client: self._do_eval_query_helper_async(
                    client, offset, query), offsets))
        return pages

    async def _do_eval_query_helper_async(
            self,
            client: httpx.AsyncClient,
            offset: int,
            query: SelectQuery
    ) -> QueryResults:
        assert 'wikidata_uri' in self.options
        assert 'page_size' in self.options
        query = query.select(offset=offset, limit=self.options['page_size'])
        query_text = str(query)
        _logger.debug(
            '%s():\n%s',
            self._do_eval_query_helper_async.__qualname__, query_text)
        try:
            res = await client.post(
                self.options['wikidata_uri'],
                content=str(query).encode('utf-8'))
            res.raise_for_status()
            return res.json()
        except httpx.RequestError as err:
            raise err

    async def _httpx_gather_async(
        self,
        tasks: Iterable[Callable[[httpx.AsyncClient], Awaitable[T]]],
        headers: Mapping[str, str] | None = None,
    ) -> Sequence[T | BaseException]:
        async with httpx.AsyncClient(
                headers=self.options.get('http_headers'),
                timeout=self.options.get('timeout'),
        ) as client:
            return await asyncio.gather(
                *map(lambda f: f(client), tasks), return_exceptions=True)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--append', action='store_true',
        help='open output files in append mode')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='enable debugging')
    parser.add_argument(
        '-l', '--limit', metavar='N', type=int,
        help='fetch at most N results')
    parser.add_argument(
        '--max-requests', metavar='N', type=int,
        help='make at most N simultaneous requests')
    parser.add_argument(
        '--max-retries', metavar='N', type=int,
        help='retry a failed request at most N times')
    parser.add_argument(
        '-O', '--output-dir', metavar='DIR', type=str,
        help='write output files to DIR')
    parser.add_argument(
        '-P', '--properties', action='store_true',
        help='fetch properties')
    parser.add_argument(
        '-Q', '--items', action='store_true',
        help='fetch items')
    parser.add_argument(
        '-s', '--page-size', metavar='N', type=int,
        help='read at most N results per page')
    parser.add_argument(
        '--show-options', action='store_true',
        help='show options and exit')
    parser.add_argument(
        '--timeout', metavar='N', type=int,
        help='requests timeout (in seconds)')
    parser.add_argument(
        '-t', '--type', metavar='TYPE', action='append', default=[],
        help='fetch only items of TYPE')
    parser.add_argument(
        '-w', '--wikidata', metavar='URL', type=str,
        help='Wikidata query service URL')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    options: Downloader.Options = {}
    if args.append is not None:
        options['append'] = args.append
    if args.limit is not None:
        options['limit'] = args.limit
    if args.max_requests is not None:
        options['max_requests'] = args.max_requests
    if args.max_retries is not None:
        options['max_retries'] = args.max_retries
    if args.output_dir is not None:
        dir = pathlib.Path(args.output_dir)
        dir.mkdir(parents=True, exist_ok=True)
        options['output_dir'] = dir
    if args.page_size is not None:
        options['page_size'] = args.page_size
    if args.timeout is not None:
        options['timeout'] = args.timeout
    if args.type is not None:
        options['item_types'] = list(args.type)
    if args.wikidata is not None:
        options['wikidata_uri'] = args.wikidata
    downloader = Downloader(options)
    if args.show_options:
        for k, v in sorted(downloader.options.items()):
            print(k, ':', v)
        sys.exit(0)
    if args.items or args.properties:
        if args.items:
            downloader.fetch_items()
        if args.properties:
            downloader.fetch_properties()
    else:
        print('Nothing to do.')
        print('Try --help for more information.')
    sys.exit(0)


if __name__ == '__main__':
    main()
