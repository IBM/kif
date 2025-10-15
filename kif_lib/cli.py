# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import logging
import os
import pathlib
import pprint
import re
import sys

from . import (
    __description__,
    __version__,
    _reset_logging,
    error,
    functools,
    itertools,
)
from .context import Context
from .engine import Engine
from .model import (
    And,
    DataValue,
    DeepDataValue,
    Deprecated,
    Entity,
    ExternalId,
    Filter,
    Fingerprint,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    Quantity,
    ShallowDataValue,
    SnakSet,
    SomeValueSnak,
    String,
    Term,
    Text,
    Value,
    ValueSnak,
)
from .model.object import Decoder, Encoder
from .search import Search
from .store import Store
from .typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    override,
    Self,
    Sequence,
    TypeVar,
    Union,
)
from .vocabulary import db, eu, fg, pc, up, wd

try:
    import click
except ImportError as err:
    raise error.missing_dependency(
        __name__, 'click', 'https://pypi.org/project/click/') from err

try:
    from rich.console import Console
    from rich.markdown import Markdown
except ImportError as err:
    raise error.missing_dependency(
        __name__, 'rich', 'https://github.com/Textualize/rich/') from err

TObj = TypeVar('TObj', bound=KIF_Object)

#: The globals table to be passed to :func:`eval`.
_G: Final[dict[str, Any]] = {}

#: The module logger.
_LOGGER: Final[logging.Logger] = logging.getLogger(__name__)

#: Whether to profile the current command.
_PROFILE: bool = False


@click.group(
    help=f'KIF: {__description__}.',
    epilog='See <https://ibm.github.io/kif/> for more information.')
@click.version_option(version=__version__)
@click.option(
    '--debug',
    '-d',
    is_flag=True,
    default=False,
    help='Enable debug logging.',
    envvar='DEBUG')
@click.option(
    '--info',
    '-i',
    is_flag=True,
    default=False,
    help='Enable info logging.',
    envvar='INFO')
@click.option(
    '--module',
    '-m',
    metavar='MOD',
    multiple=True,
    help='Load module MOD.')
@click.option(
    '--profile',
    is_flag=True,
    default=False,
    help='Profile command using cProfile.')
def cli(
        debug: bool | None = None,
        info: bool | None = None,
        module: Sequence[str] = (),
        profile: bool | None = None
) -> None:
    if debug or info:
        ctx = Context.top()
        ctx.options.search.debug = bool(debug)
        ctx.options.store.debug = bool(debug)
        _reset_logging(debug=bool(debug), info=bool(info))
    if module:
        import importlib
        sys.path.append(os.getcwd())
        for mod in module:
            global _G           # noqa: F824
            _G[mod] = importlib.import_module(mod)
    if profile:
        global _PROFILE
        _PROFILE = True


def _run(command: Callable[[], None]) -> None:
    if _PROFILE:
        import cProfile
        import shutil
        import subprocess
        import tempfile
        prof = cProfile.Profile()
        prof.runcall(command)
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        prof_file, cgraph_file = tmpdir / 'profile', tmpdir / 'callgraph'
        prof.dump_stats(prof_file)
        subprocess.run(['pyprof2calltree', '-k', '-i', prof_file,
                        '-o', cgraph_file], check=True)
        shutil.rmtree(tmpdir)
    else:
        command()


@cli.command(help='Show KIF options and exit.')
@click.argument(
    'name',
    type=str,
    default='kif')
@click.option(
    '--describe',
    '-d',
    'describe',
    is_flag=True,
    default=False,
    help='Show option description.')
def show_options(name: str, describe: bool | None = None) -> None:
    def _show_options() -> None:
        ctx = Context.top()
        if describe:
            click.echo(ctx.get_option_description_by_name(name))
        else:
            click.echo(ctx.get_option_by_name(name))
    _run(_show_options)


@cli.command(help='Show available plugins and exit.')
@click.option(
    '--decoder',
    is_flag=True,
    default=False,
    help='Show decoder plugins.')
@click.option(
    '--encoder',
    is_flag=True,
    default=False,
    help='Show encoder plugins.')
@click.option(
    '--search',
    is_flag=True,
    default=False,
    help='Show search plugins.')
@click.option(
    '--store',
    is_flag=True,
    default=False,
    help='Show store plugins.')
def show_plugins(
        decoder: bool,
        encoder: bool,
        store: bool,
        search: bool
) -> None:
    n = sum(map(int, (decoder, encoder, store, search)))
    if not n:
        n, (decoder, encoder, store, search) = 4, itertools.repeat(True, 4)
    _run(lambda: _echo_lines(_join_name_description_pairs(
        itertools.chain(*itertools.starmap(
            lambda ty, it: ((f'{ty}.{k}' if n != 1 else k, v) for k, v in it),
            (('decoder', _iterate_decoder_plugins() if decoder else ()),
             ('encoder', _iterate_encoder_plugins() if encoder else ()),
             ('search', _iterate_search_plugins() if search else ()),
             ('store', _iterate_store_plugins() if store else ())))))))


def _join_name_description_pairs(
        pairs: Iterable[tuple[str, str]]
) -> Iterator[str]:
    pairs = list(pairs)
    if pairs:
        longest_name_length = max(map(len, map(functools.fst, pairs)))
        for k, v in sorted(pairs):
            yield f'{k:<{longest_name_length}} : {v}'


def _iterate_decoder_plugins() -> Iterator[tuple[str, str]]:
    return ((k, v.description) for k, v in Decoder.registry.items())


def _iterate_encoder_plugins() -> Iterator[tuple[str, str]]:
    return ((k, v.description) for k, v in Encoder.registry.items())


def _iterate_search_plugins() -> Iterator[tuple[str, str]]:
    return ((k, v.search_description) for k, v in Search.registry.items())


def _iterate_store_plugins() -> Iterator[tuple[str, str]]:
    return ((k, v.store_description) for k, v in Store.registry.items())


def _echo_lines(lines: Iterator[str]) -> None:
    for line in lines:
        click.echo(line)


class KIF_ParamType(click.ParamType):

    _instance: ClassVar[Self | None] = None

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    @functools.cache
    def globals(cls) -> dict[str, Any]:
        global _G               # noqa: F824
        return {
            '__builtins__': {},
            'ALIAS': Filter.ALIAS,
            'DATA_VALUE': Filter.DATA_VALUE,
            'DataValue': DataValue,
            'db': db,
            'Decoder': Decoder,
            'DEEP_DATA_VALUE': Filter.DEEP_DATA_VALUE,
            'DeepDataValue': DeepDataValue,
            'Deprecated': Deprecated,
            'DEPRECATED': Filter.DEPRECATED,
            'DESCRIPTION': Filter.DESCRIPTION,
            'Encoder': Encoder,
            'Entity': Entity,
            'ENTITY': Filter.ENTITY,
            'eu': eu,
            'EXTERNAL_ID': Filter.EXTERNAL_ID,
            'ExternalId': ExternalId,
            'fg': fg,
            'Filter': Filter,
            'IRI': IRI,
            'ITEM': Filter.ITEM,
            'Item': Item,
            'LABEL': Filter.LABEL,
            'LANGUAGE': Filter.LANGUAGE,
            'LEMMA': Filter.LEMMA,
            'LEXEME': Filter.LEXEME,
            'Lexeme': Lexeme,
            'LEXICAL_CATEGORY': Filter.LEXICAL_CATEGORY,
            'NO_VALUE_SNAK': Filter.NO_VALUE_SNAK,
            'NORMAL': Filter.NORMAL,
            'Normal': Normal,
            'NoValueSnak': NoValueSnak,
            'pc': pc,
            'PREFERRED': Filter.PREFERRED,
            'Preferred': Preferred,
            'PROPERTY': Filter.PROPERTY,
            'Property': Property,
            'PSEUDO': Filter.PSEUDO,
            'QUANTITY': Filter.QUANTITY,
            'Quantity': Quantity,
            'REAL': Filter.REAL,
            'SHALLOW_DATA_VALUE': Filter.SHALLOW_DATA_VALUE,
            'ShallowDataValue': ShallowDataValue,
            'SOME_VALUE_SNAK': Filter.SOME_VALUE_SNAK,
            'SomeValueSnak': SomeValueSnak,
            'STIRNG': Filter.STRING,
            'Store': Store,
            'STRING': Filter.STRING,
            'String': String,
            'SUBTYPE': Filter.SUBTYPE,
            'TEXT': Filter.TEXT,
            'Text': Text,
            'TYPE': Filter.TYPE,
            'up': up,
            'VALUE': Filter.VALUE,
            'Value': Value,
            'VALUE_SNAK': Filter.VALUE_SNAK,
            'ValueSnak': ValueSnak,
            'wd': wd,
            **_G
        }

    @classmethod
    def eval(cls, value: Any) -> Any:
        if isinstance(value, KIF_Object):
            return value
        else:
            try:
                return eval(value, cls.globals(), {})
            except Exception as err:
                raise ValueError(err) from err


class EncoderParamType(KIF_ParamType):

    name: str = 'encoder'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Encoder:
        if isinstance(value, str):
            try:
                return Encoder._check_format(value)()
            except ValueError:
                pass
        try:
            return KIF_Object._check_arg_isinstance(self.eval(value), Encoder)
        except (ValueError, TypeError) as err:
            return self.fail(str(err), param, ctx)


class EngineParamType(KIF_ParamType):

    constructor: ClassVar[type[Engine]]
    constructor_re: ClassVar[re.Pattern[str]] = re.compile(
        r'^([\w-]+)(?:([@?])(.*))?$')
    name: str = 'engine'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Engine:
        if isinstance(value, str):
            m = self.constructor_re.match(value)
            if m:
                plugin_name, op, args = m.groups()
                if args:
                    if op == '@':
                        return self.constructor(plugin_name, *args.split(';'))
                    if op == '?':
                        exp_args = list(pathlib.Path('.').glob(args))
                        _LOGGER.info(
                            'expanded arguments: %s',
                            ';'.join(map(str, exp_args)))
                        return self.constructor(plugin_name, *exp_args)
                return self.constructor(plugin_name)
        try:
            return KIF_Object._check_arg_isinstance(
                self.eval(value), self.constructor)
        except (ValueError, TypeError) as err:
            return self.fail(str(err), param, ctx)

    @override
    def split_envvar_value(self, rv: str) -> Sequence[str]:  # type: ignore
        return (rv or '').split(';')


class SearchParamType(EngineParamType):

    constructor = Search
    name = 'search'


class StoreParamType(EngineParamType):

    constructor = Store
    name = 'store'


class KIF_ObjectParamType(KIF_ParamType):

    def _convert(
            self,
            kif_object_class: type[TObj],
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> TObj:
        try:
            return kif_object_class.check(self.eval(value))
        except (ValueError, TypeError) as err:
            return self.fail(str(err), param, ctx)


class DatatypeMaskParamType(KIF_ObjectParamType):

    name: str = 'datatype_mask'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Fingerprint:
        return self._convert(
            Filter.DatatypeMask, value, param, ctx)  # type: ignore


class PropertyMaskParamType(KIF_ObjectParamType):

    name: str = 'property_mask'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Fingerprint:
        return self._convert(
            Filter.PropertyMask, value, param, ctx)  # type: ignore


class FingerprintParamType(KIF_ObjectParamType):

    name: str = 'fingerprint'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Fingerprint:
        return self._convert(Fingerprint, value, param, ctx)  # type: ignore


class SnakMaskParamType(KIF_ObjectParamType):

    name: str = 'snak_mask'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Fingerprint:
        return self._convert(
            Filter.SnakMask, value, param, ctx)  # type: ignore


class RankMaskParamType(KIF_ObjectParamType):

    name: str = 'rank_mask'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Fingerprint:
        return self._convert(
            Filter.RankMask, value, param, ctx)  # type: ignore


class FilterParam:
    """Common stuff for filter-like commands."""

    subject = click.argument(
        'subject',
        type=FingerprintParamType.get_instance(),
        required=False,
        envvar='SUBJECT')

    property = click.argument(
        'property',
        type=FingerprintParamType.get_instance(),
        required=False,
        envvar='PROPERTY')

    value = click.argument(
        'value',
        type=FingerprintParamType.get_instance(),
        required=False,
        envvar='VALUE')

    annotated = click.option(
        '--annotated',
        '-a',
        'annotated',
        is_flag=True,
        default=False,
        help='Fetch annotations.',
        envvar='ANNOTATED')

    dry_run = click.option(
        '--dry-run',
        'dry_run',
        is_flag=True,
        default=False,
        help='Dry run.',
        envvar='DRY_RUN')

    encoder = click.option(
        '--encoder',
        'encoder',
        type=EncoderParamType.get_instance(),
        help='Encoder.',
        envvar='ENCODER')

    encoder_dot = click.option(
        '--dot',
        'encoder_dot',
        is_flag=True,
        default=False,
        help='Alias: --encoder=dot.')

    encoder_json = click.option(
        '--json',
        'encoder_json',
        is_flag=True,
        default=False,
        help='Alias: --encoder=json.')

    encoder_markdown = click.option(
        '--markdown',
        'encoder_markdown',
        is_flag=True,
        default=False,
        help='Alias: --encoder=markdown.')

    encoder_rdf = click.option(
        '--rdf',
        'encoder_rdf',
        is_flag=True,
        default=False,
        help='Alias: --encoder=rdf.')

    encoder_repr = click.option(
        '--repr',
        'encoder_repr',
        is_flag=True,
        default=False,
        help='Alias: --encoder=repr.')

    encoder_sexp = click.option(
        '--sexp',
        'encoder_sexp',
        is_flag=True,
        default=False,
        help='Alias: --encoder=sexp.')

    language = click.option(
        '--language',
        'language',
        type=str,
        required=False,
        help='Language tag.',
        envvar='LANGUAGE')

    lookahead = click.option(
        '--lookahead',
        'lookahead',
        type=int,
        required=False,
        help='Number of pages to lookahead asynchronously.',
        envvar='LOOKAHEAD')

    limit = click.option(
        '--limit',
        'limit',
        type=int,
        required=False,
        help='Maximum number of results.',
        envvar='LIMIT')

    async_ = click.option(
        '--async / --no-async',
        'async_',
        is_flag=True,
        default=True,
        help='Use the asynchronous API.',
        envvar='ASYNC')

    distinct = click.option(
        '--distinct / --no-distinct',
        'distinct',
        is_flag=True,
        default=True,
        help='Suppress duplicates.',
        envvar='DISTINCT')

    resolve = click.option(
        '--resolve / --no-resolve',
        'resolve',
        is_flag=True,
        default=True,
        help='Resolve entity labels.',
        envvar='RESOLVE')

    best_ranked = click.option(
        '--best-ranked / --non-best-ranked',
        'best_ranked',
        is_flag=True,
        default=True,
        help='Match best-ranked statements.',
        envvar='BEST_RANKED')

    omega = click.option(
        '--omega',
        'omega',
        type=int,
        required=False,
        help='Maximum number of disjoint subqueries.',
        envvar='OMEGA')

    page_size = click.option(
        '--page-size',
        'page_size',
        type=int,
        required=False,
        help='Size of response pages.',
        envvar='PAGE_SIZE')

    property_option = click.option(
        '--property',
        'property_option',
        type=FingerprintParamType.get_instance(),
        required=False,
        help='Property fingerprint.',
        envvar='PROPERTY')

    property_mask = click.option(
        '--property-mask',
        'property_mask',
        type=PropertyMaskParamType.get_instance(),
        required=False,
        help='Property datatype mask.',
        envvar='PROPERTY_MASK')

    rank_mask = click.option(
        '--rank-mask',
        'rank_mask',
        type=RankMaskParamType.get_instance(),
        required=False,
        help='Rank mask.',
        envvar='RANK_MASK')

    select = click.option(
        '--select',
        'select',
        type=click.Choice(['s', 'p', 'v', 'sp', 'sv', 'pv', 'spv']),
        default='spv',
        help='Projection specification.',
        envvar='SELECT')

    snak_is_no_value = click.option(
        '--snak-is-no-value',
        'snak_is_no_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-mask=NO_VALUE_SNAK.')

    snak_is_some_value = click.option(
        '--snak-is-some-value',
        'snak_is_some_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-mask=SOME_VALUE_SNAK.')

    snak_is_value = click.option(
        '--snak-is-value',
        'snak_is_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-mask=VALUE_SNAK.')

    snak_mask = click.option(
        '--snak-mask',
        'snak_mask',
        type=SnakMaskParamType.get_instance(),
        required=False,
        help='Snak mask.',
        envvar='SNAK_MASK')

    store = click.option(
        '--store',
        '-s',
        'store',
        type=StoreParamType.get_instance(),
        multiple=True,
        help='Target store.',
        envvar='STORE')

    subject_option = click.option(
        '--subject',
        'subject_option',
        type=FingerprintParamType.get_instance(),
        required=False,
        help='Subject fingerprint.')

    subject_is_item = click.option(
        '--subject-is-item',
        'subject_is_item',
        is_flag=True,
        default=False,
        help='Alias: --subject-mask=ITEM.')

    subject_is_property = click.option(
        '--subject-is-property',
        'subject_is_property',
        is_flag=True,
        default=False,
        help='Alias: --subject-mask=PROPERTY.')

    subject_is_lexeme = click.option(
        '--subject-is-lexeme',
        'subject_is_lexeme',
        is_flag=True,
        default=False,
        help='Alias: --subject-mask=LEXEME.')

    subject_mask = click.option(
        '--subject-mask',
        'subject_mask',
        type=DatatypeMaskParamType.get_instance(),
        required=False,
        help='Subject datatype mask.',
        envvar='SUBJECT_MASK')

    timeout = click.option(
        '--timeout',
        'timeout',
        type=float,
        required=False,
        help='Timeout in seconds.',
        envvar='TIMEOUT')

    value_option = click.option(
        '--value',
        'value_option',
        type=FingerprintParamType.get_instance(),
        required=False,
        help='Value fingerprint.',
        envvar='VALUE')

    value_is_data_value = click.option(
        '--value-is-data-value',
        'value_is_data_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=DATA_VALUE.')

    value_is_deep_data_value = click.option(
        '--value-is-deep-data-value',
        'value_is_deep_data_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=DEEP_DATA_VALUE.')

    value_is_entity = click.option(
        '--value-is-entity',
        'value_is_entity',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=ENTITY.')

    value_is_external_id = click.option(
        '--value-is-external-id',
        'value_is_external_id',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=EXTERNAL_ID.')

    value_is_iri = click.option(
        '--value-is-iri',
        'value_is_iri',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=IRI.')

    value_is_item = click.option(
        '--value-is-item',
        'value_is_item',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=ITEM.')

    value_is_lexeme = click.option(
        '--value-is-lexeme',
        'value_is_lexeme',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=LEXEME.')

    value_is_property = click.option(
        '--value-is-property',
        'value_is_property',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=PROPERTY.')

    value_is_quantity = click.option(
        '--value-is-quantity',
        'value_is_quantity',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=QUANTITY.')

    value_is_shallow_data_value = click.option(
        '--value-is-shallow-data-value',
        'value_is_shallow_data_value',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=SHALLOW_DATA_VALUE.')

    value_is_string = click.option(
        '--value-is-string',
        'value_is_string',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=STRING.')

    value_is_text = click.option(
        '--value-is-text',
        'value_is_text',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=TEXT.')

    value_is_time = click.option(
        '--value-is-time',
        'value_is_time',
        is_flag=True,
        default=False,
        help='Alias: --snak-is-value --value-mask=TIME.')

    value_is_value = click.option(
        '--value-is-value',
        'value_is_value',
        is_flag=True,
        help='Alias: --snak-is-value --value-mask=VALUE.')

    value_mask = click.option(
        '--value-mask',
        'value_mask',
        type=DatatypeMaskParamType.get_instance(),
        required=False,
        help='Value datatype mask.',
        envvar='VALUE_MASK')

    vocabulary_dump = click.option(
        '--vocabulary-dump',
        'vocabulary_dump',
        is_flag=True,
        help='Dump entities using vocabulary module format.')

    @classmethod
    def make_context(cls, resolve: bool | None = None) -> Context:
        context = Context.top()
        if resolve is not None:
            context.options.entities.resolve = False
        return context

    @classmethod
    def make_filter(
            cls,
            subject: Fingerprint | None = None,
            subject_option: Fingerprint | None = None,
            property: Fingerprint | None = None,
            property_option: Fingerprint | None = None,
            value: Fingerprint | None = None,
            value_option: Fingerprint | None = None,
            snak_is_no_value: bool | None = None,
            snak_is_some_value: bool | None = None,
            snak_is_value: bool | None = None,
            snak_mask: Filter.SnakMask | None = None,
            subject_is_item: bool | None = None,
            subject_is_lexeme: bool | None = None,
            subject_is_property: bool | None = None,
            subject_mask: Filter.DatatypeMask | None = None,
            property_mask: Filter.PropertyMask | None = None,
            value_is_data_value: bool | None = None,
            value_is_deep_data_value: bool | None = None,
            value_is_entity: bool | None = None,
            value_is_external_id: bool | None = None,
            value_is_iri: bool | None = None,
            value_is_item: bool | None = None,
            value_is_lexeme: bool | None = None,
            value_is_property: bool | None = None,
            value_is_quantity: bool | None = None,
            value_is_shallow_data_value: bool | None = None,
            value_is_string: bool | None = None,
            value_is_text: bool | None = None,
            value_is_time: bool | None = None,
            value_is_value: bool | None = None,
            value_mask: Filter.DatatypeMask | None = None,
            rank_mask: Filter.RankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            dry_run: bool | None = None,
            console: Console | None = None
    ) -> Filter:
        if snak_mask is None and (
                snak_is_no_value
                or snak_is_some_value
                or snak_is_value):
            snak_mask = Filter.SnakMask(0)
            if snak_is_no_value:
                snak_mask |= Filter.NO_VALUE_SNAK
            if snak_is_some_value:
                snak_mask |= Filter.SOME_VALUE_SNAK
            if snak_is_value:
                snak_mask |= Filter.VALUE_SNAK
        if subject_mask is None and (
                subject_is_item
                or subject_is_lexeme
                or subject_is_property):
            subject_mask = Filter.DatatypeMask(0)
            if subject_is_item:
                subject_mask |= Filter.ITEM
            if subject_is_lexeme:
                subject_mask |= Filter.LEXEME
            if subject_is_property:
                subject_mask |= Filter.PROPERTY
        if value_mask is None and (
                value_is_data_value
                or value_is_deep_data_value
                or value_is_entity
                or value_is_external_id
                or value_is_iri
                or value_is_item
                or value_is_lexeme
                or value_is_property
                or value_is_quantity
                or value_is_shallow_data_value
                or value_is_string
                or value_is_text
                or value_is_time
                or value_is_value):
            if snak_mask is None:
                snak_mask = Filter.VALUE_SNAK
            value_mask = Filter.DatatypeMask(0)
            if value_is_data_value:
                value_mask |= Filter.DATA_VALUE
            if value_is_deep_data_value:
                value_mask |= Filter.DEEP_DATA_VALUE
            if value_is_entity:
                value_mask |= Filter.ENTITY
            if value_is_external_id:
                value_mask |= Filter.EXTERNAL_ID
            if value_is_iri:
                value_mask |= Filter.IRI
            if value_is_item:
                value_mask |= Filter.ITEM
            if value_is_lexeme:
                value_mask |= Filter.LEXEME
            if value_is_property:
                value_mask |= Filter.PROPERTY
            if value_is_quantity:
                value_mask |= Filter.QUANTITY
            if value_is_shallow_data_value:
                value_mask |= Filter.SHALLOW_DATA_VALUE
            if value_is_string:
                value_mask |= Filter.STRING
            if value_is_text:
                value_mask |= Filter.TEXT
            if value_is_time:
                value_mask |= Filter.TIME
            if value_is_value:
                value_mask |= Filter.VALUE
        fr = Filter(
            subject=And(subject, subject_option),
            property=And(property, property_option),
            value=And(value, value_option),
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
            best_ranked=best_ranked,
            language=language,
            annotated=annotated,
        ).normalize()
        if dry_run:
            (console or Console()).print(Markdown(fr.to_markdown()))
            sys.exit(0)
        return fr

    @classmethod
    def make_store(
            cls,
            store: Sequence[Store],
            distinct: bool | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None
    ) -> Store:
        target: Store
        if len(store) == 0:
            target = Store('wdqs')
        elif len(store) == 1:
            target = store[0]
        else:
            target = Store('mixer', store)
        if distinct is not None:
            target.set_distinct(distinct)
        if limit is not None:
            target.set_limit(limit)
        if lookahead is not None:
            target.set_lookahead(lookahead)
        if omega is not None:
            target.set_omega(omega)
        if page_size is not None:
            target.set_page_size(page_size)
        if timeout is not None:
            target.set_timeout(timeout)
        return target


@cli.command(help='Tests whether some statement matches filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.async_
@FilterParam.best_ranked
@FilterParam.distinct
@FilterParam.dry_run
@FilterParam.encoder
@FilterParam.language
@FilterParam.omega
@FilterParam.property_mask
@FilterParam.property_option
@FilterParam.rank_mask
@FilterParam.resolve
@FilterParam.snak_is_no_value
@FilterParam.snak_is_some_value
@FilterParam.snak_is_value
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_is_item
@FilterParam.subject_is_lexeme
@FilterParam.subject_is_property
@FilterParam.subject_mask
@FilterParam.subject_option
@FilterParam.timeout
@FilterParam.value_is_data_value
@FilterParam.value_is_deep_data_value
@FilterParam.value_is_entity
@FilterParam.value_is_external_id
@FilterParam.value_is_iri
@FilterParam.value_is_item
@FilterParam.value_is_lexeme
@FilterParam.value_is_property
@FilterParam.value_is_quantity
@FilterParam.value_is_shallow_data_value
@FilterParam.value_is_string
@FilterParam.value_is_text
@FilterParam.value_is_time
@FilterParam.value_is_value
@FilterParam.value_mask
@FilterParam.value_option
def ask(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_is_no_value: bool | None = None,
        snak_is_some_value: bool | None = None,
        snak_is_value: bool | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_is_item: bool | None = None,
        subject_is_lexeme: bool | None = None,
        subject_is_property: bool | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.PropertyMask | None = None,
        value_is_data_value: bool | None = None,
        value_is_deep_data_value: bool | None = None,
        value_is_entity: bool | None = None,
        value_is_external_id: bool | None = None,
        value_is_iri: bool | None = None,
        value_is_item: bool | None = None,
        value_is_lexeme: bool | None = None,
        value_is_property: bool | None = None,
        value_is_quantity: bool | None = None,
        value_is_shallow_data_value: bool | None = None,
        value_is_string: bool | None = None,
        value_is_text: bool | None = None,
        value_is_time: bool | None = None,
        value_is_value: bool | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        best_ranked: bool | None = None,
        language: str | None = None,
        async_: bool | None = None,
        distinct: bool | None = None,
        dry_run: bool | None = None,
        encoder: Encoder | None = None,
        omega: int | None = None,
        resolve: bool | None = None,
        timeout: float | None = None
) -> None:
    def _ask() -> None:
        fr = FilterParam.make_filter(
            subject=subject,
            subject_option=subject_option,
            property=property,
            property_option=property_option,
            value=value,
            value_option=value_option,
            snak_is_no_value=snak_is_no_value,
            snak_is_some_value=snak_is_some_value,
            snak_is_value=snak_is_value,
            snak_mask=snak_mask,
            subject_is_item=subject_is_item,
            subject_is_lexeme=subject_is_lexeme,
            subject_is_property=subject_is_property,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_is_data_value=value_is_data_value,
            value_is_deep_data_value=value_is_deep_data_value,
            value_is_entity=value_is_entity,
            value_is_external_id=value_is_external_id,
            value_is_iri=value_is_iri,
            value_is_item=value_is_item,
            value_is_lexeme=value_is_lexeme,
            value_is_property=value_is_property,
            value_is_quantity=value_is_quantity,
            value_is_shallow_data_value=value_is_shallow_data_value,
            value_is_string=value_is_string,
            value_is_text=value_is_text,
            value_is_time=value_is_time,
            value_is_value=value_is_value,
            value_mask=value_mask,
            rank_mask=rank_mask,
            best_ranked=best_ranked,
            language=language,
            dry_run=dry_run)
        target = FilterParam.make_store(
            store,
            distinct=distinct,
            omega=omega,
            timeout=timeout)
        status: bool
        if async_:
            async def aask():
                return await target.aask(filter=fr)
            status = asyncio.run(aask())
        else:
            status = target.ask(filter=fr)
        if _PROFILE:
            click.echo(status)
        else:
            sys.exit(int(not status))
    _run(_ask)


@cli.command(help='Counts the number of statements matching filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.annotated
@FilterParam.async_
@FilterParam.best_ranked
@FilterParam.distinct
@FilterParam.dry_run
@FilterParam.encoder
@FilterParam.language
@FilterParam.omega
@FilterParam.property_mask
@FilterParam.property_option
@FilterParam.rank_mask
@FilterParam.resolve
@FilterParam.select
@FilterParam.snak_is_no_value
@FilterParam.snak_is_some_value
@FilterParam.snak_is_value
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_is_item
@FilterParam.subject_is_lexeme
@FilterParam.subject_is_property
@FilterParam.subject_mask
@FilterParam.subject_option
@FilterParam.timeout
@FilterParam.value_is_data_value
@FilterParam.value_is_deep_data_value
@FilterParam.value_is_entity
@FilterParam.value_is_external_id
@FilterParam.value_is_iri
@FilterParam.value_is_item
@FilterParam.value_is_lexeme
@FilterParam.value_is_property
@FilterParam.value_is_quantity
@FilterParam.value_is_shallow_data_value
@FilterParam.value_is_string
@FilterParam.value_is_text
@FilterParam.value_is_time
@FilterParam.value_is_value
@FilterParam.value_mask
@FilterParam.value_option
def count(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_is_no_value: bool | None = None,
        snak_is_some_value: bool | None = None,
        snak_is_value: bool | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_is_item: bool | None = None,
        subject_is_lexeme: bool | None = None,
        subject_is_property: bool | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.PropertyMask | None = None,
        value_is_data_value: bool | None = None,
        value_is_deep_data_value: bool | None = None,
        value_is_entity: bool | None = None,
        value_is_external_id: bool | None = None,
        value_is_iri: bool | None = None,
        value_is_item: bool | None = None,
        value_is_lexeme: bool | None = None,
        value_is_property: bool | None = None,
        value_is_quantity: bool | None = None,
        value_is_shallow_data_value: bool | None = None,
        value_is_string: bool | None = None,
        value_is_text: bool | None = None,
        value_is_time: bool | None = None,
        value_is_value: bool | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        best_ranked: bool | None = None,
        language: str | None = None,
        annotated: bool | None = None,
        async_: bool | None = None,
        distinct: bool | None = None,
        dry_run: bool | None = None,
        encoder: Encoder | None = None,
        omega: int | None = None,
        resolve: bool | None = None,
        select: str | None = None,
        timeout: float | None = None
) -> None:
    def _count() -> None:
        fr = FilterParam.make_filter(
            subject=subject,
            subject_option=subject_option,
            property=property,
            property_option=property_option,
            value=value,
            value_option=value_option,
            snak_is_no_value=snak_is_no_value,
            snak_is_some_value=snak_is_some_value,
            snak_is_value=snak_is_value,
            snak_mask=snak_mask,
            subject_is_item=subject_is_item,
            subject_is_lexeme=subject_is_lexeme,
            subject_is_property=subject_is_property,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_is_data_value=value_is_data_value,
            value_is_deep_data_value=value_is_deep_data_value,
            value_is_entity=value_is_entity,
            value_is_external_id=value_is_external_id,
            value_is_iri=value_is_iri,
            value_is_item=value_is_item,
            value_is_lexeme=value_is_lexeme,
            value_is_property=value_is_property,
            value_is_quantity=value_is_quantity,
            value_is_shallow_data_value=value_is_shallow_data_value,
            value_is_string=value_is_string,
            value_is_text=value_is_text,
            value_is_time=value_is_time,
            value_is_value=value_is_value,
            value_mask=value_mask,
            rank_mask=rank_mask,
            best_ranked=best_ranked,
            language=language,
            dry_run=dry_run)
        target = FilterParam.make_store(
            store,
            distinct=distinct,
            omega=omega,
            timeout=timeout)
        n: int
        if async_:
            ac: dict[str, Callable[[], Awaitable[int]]] = {
                's': (lambda: target.acount_s(filter=fr)),
                'p': (lambda: target.acount_p(filter=fr)),
                'v': (lambda: target.acount_v(filter=fr)),
                'sp': (lambda: target.acount_sp(filter=fr)),
                'sv': (lambda: target.acount_sv(filter=fr)),
                'pv': (lambda: target.acount_pv(filter=fr)),
                'spv': (lambda: target.acount(filter=fr))}

            async def acount():
                assert select is not None
                return await ac[select]()
            n = asyncio.run(acount())
        else:
            c: dict[str, Callable[[], int]] = {
                's': (lambda: target.count_s(filter=fr)),
                'p': (lambda: target.count_p(filter=fr)),
                'v': (lambda: target.count_v(filter=fr)),
                'sp': (lambda: target.count_sp(filter=fr)),
                'sv': (lambda: target.count_sv(filter=fr)),
                'pv': (lambda: target.count_pv(filter=fr)),
                'spv': (lambda: target.count(filter=fr))}
            assert select is not None
            n = c[select]()
        click.echo(n)
    _run(_count)


@cli.command(help='Searches for statements matching filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.annotated
@FilterParam.async_
@FilterParam.best_ranked
@FilterParam.distinct
@FilterParam.dry_run
@FilterParam.encoder
@FilterParam.encoder_dot
@FilterParam.encoder_json
@FilterParam.encoder_markdown
@FilterParam.encoder_rdf
@FilterParam.encoder_repr
@FilterParam.encoder_sexp
@FilterParam.language
@FilterParam.limit
@FilterParam.lookahead
@FilterParam.omega
@FilterParam.page_size
@FilterParam.property_mask
@FilterParam.property_option
@FilterParam.rank_mask
@FilterParam.resolve
@FilterParam.select
@FilterParam.snak_is_no_value
@FilterParam.snak_is_some_value
@FilterParam.snak_is_value
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_is_item
@FilterParam.subject_is_lexeme
@FilterParam.subject_is_property
@FilterParam.subject_mask
@FilterParam.subject_option
@FilterParam.timeout
@FilterParam.value_is_data_value
@FilterParam.value_is_deep_data_value
@FilterParam.value_is_entity
@FilterParam.value_is_external_id
@FilterParam.value_is_iri
@FilterParam.value_is_item
@FilterParam.value_is_lexeme
@FilterParam.value_is_property
@FilterParam.value_is_quantity
@FilterParam.value_is_shallow_data_value
@FilterParam.value_is_string
@FilterParam.value_is_text
@FilterParam.value_is_time
@FilterParam.value_is_value
@FilterParam.value_mask
@FilterParam.value_option
@FilterParam.vocabulary_dump
def filter(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_is_no_value: bool | None = None,
        snak_is_some_value: bool | None = None,
        snak_is_value: bool | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_is_item: bool | None = None,
        subject_is_lexeme: bool | None = None,
        subject_is_property: bool | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.PropertyMask | None = None,
        value_is_data_value: bool | None = None,
        value_is_deep_data_value: bool | None = None,
        value_is_entity: bool | None = None,
        value_is_external_id: bool | None = None,
        value_is_iri: bool | None = None,
        value_is_item: bool | None = None,
        value_is_lexeme: bool | None = None,
        value_is_property: bool | None = None,
        value_is_quantity: bool | None = None,
        value_is_shallow_data_value: bool | None = None,
        value_is_string: bool | None = None,
        value_is_text: bool | None = None,
        value_is_time: bool | None = None,
        value_is_value: bool | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        best_ranked: bool | None = None,
        language: str | None = None,
        annotated: bool | None = None,
        async_: bool | None = None,
        distinct: bool | None = None,
        dry_run: bool | None = None,
        encoder: Encoder | None = None,
        encoder_dot: bool | None = None,
        encoder_json: bool | None = None,
        encoder_markdown: bool | None = None,
        encoder_rdf: bool | None = None,
        encoder_repr: bool | None = None,
        encoder_sexp: bool | None = None,
        limit: int | None = None,
        lookahead: int | None = None,
        omega: int | None = None,
        page_size: int | None = None,
        resolve: bool | None = None,
        select: str | None = None,
        timeout: float | None = None,
        vocabulary_dump: bool | None = None
) -> None:
    def _filter() -> None:
        console = Console()
        context = FilterParam.make_context(resolve)
        fr = FilterParam.make_filter(
            subject=subject,
            subject_option=subject_option,
            property=property,
            property_option=property_option,
            value=value,
            value_option=value_option,
            snak_is_no_value=snak_is_no_value,
            snak_is_some_value=snak_is_some_value,
            snak_is_value=snak_is_value,
            snak_mask=snak_mask,
            subject_is_item=subject_is_item,
            subject_is_lexeme=subject_is_lexeme,
            subject_is_property=subject_is_property,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_is_data_value=value_is_data_value,
            value_is_deep_data_value=value_is_deep_data_value,
            value_is_entity=value_is_entity,
            value_is_external_id=value_is_external_id,
            value_is_iri=value_is_iri,
            value_is_item=value_is_item,
            value_is_lexeme=value_is_lexeme,
            value_is_property=value_is_property,
            value_is_quantity=value_is_quantity,
            value_is_shallow_data_value=value_is_shallow_data_value,
            value_is_string=value_is_string,
            value_is_text=value_is_text,
            value_is_time=value_is_time,
            value_is_value=value_is_value,
            value_mask=value_mask,
            rank_mask=rank_mask,
            best_ranked=best_ranked,
            language=language,
            annotated=annotated,
            dry_run=dry_run,
            console=console)
        target = FilterParam.make_store(
            store,
            distinct=distinct,
            limit=limit,
            lookahead=lookahead,
            omega=omega,
            page_size=page_size,
            timeout=timeout)
        nonlocal encoder
        if encoder_dot:
            encoder = Encoder._check_format('dot')()
        elif encoder_json:
            encoder = Encoder._check_format('json')()
        elif encoder_markdown:
            encoder = Encoder._check_format('markdown')()
        elif encoder_rdf:
            encoder = Encoder._check_format('rdf')()
        elif encoder_repr:
            encoder = Encoder._check_format('repr')()
        elif encoder_sexp:
            encoder = Encoder._check_format('sexp')()
        output = functools.partial(
            _output_filter_page,
            console,
            encoder=encoder,
            language=language,
            resolve=resolve,
            vocabulary_dump=vocabulary_dump,
            context=context)
        if async_:
            af: dict[str, Callable[[], AsyncIterator[Term]]] = {
                's': (lambda: target.afilter_s(filter=fr)),
                'p': (lambda: target.afilter_p(filter=fr)),
                'v': (lambda: target.afilter_v(filter=fr)),
                'sp': (lambda: target.afilter_sp(filter=fr)),
                'sv': (lambda: target.afilter_sv(filter=fr)),
                'pv': (lambda: target.afilter_pv(filter=fr)),
                'spv': (lambda: target.afilter(filter=fr))}

            async def afilter():
                assert select is not None
                it, i = af[select](), 1
                while True:
                    page = await itertools.atake(target.page_size, it)
                    if not page:
                        break
                    output(page, i)
                    i += 1
            asyncio.run(afilter())
        else:
            f: dict[str, Callable[[], Iterator[Term]]] = {
                's': (lambda: target.filter_s(filter=fr)),
                'p': (lambda: target.filter_p(filter=fr)),
                'v': (lambda: target.filter_v(filter=fr)),
                'sp': (lambda: target.filter_sp(filter=fr)),
                'sv': (lambda: target.filter_sv(filter=fr)),
                'pv': (lambda: target.filter_pv(filter=fr)),
                'spv': (lambda: target.filter(filter=fr))}
            assert select is not None
            batches = itertools.batched(f[select](), target.page_size)
            for i, page in enumerate(batches, 1):
                output(page, i)
    _run(_filter)


def _output_filter_page(
        console: Console,
        page: Iterable[Term],
        pageno: int,
        encoder: Encoder | None = None,
        language: str | None = None,
        resolve: bool | None = None,
        vocabulary_dump: bool | None = None,
        context: Context | None = None
) -> None:
    _LOGGER.info('outputting page %d', pageno)
    if resolve or vocabulary_dump:
        assert context is not None
        resolved_page = _output_filter_resolve_page(context, page, language)
    else:
        resolved_page = page
    if vocabulary_dump:
        from .str2id import Str2Id
        as_id = Str2Id()
        assert context is not None
        entities = set(itertools.chain(
            *(term.traverse(Entity.test) for term in resolved_page)))
        while True:
            var_entity_pairs = list(
                (as_id(e.label.content), e)
                for e in entities
                if isinstance(e, (Item, Property)) and e.label is not None)
            _LOGGER.info('collected %d var-entity pairs in page %d',
                         len(var_entity_pairs), pageno)
            for var, entity in var_entity_pairs:
                assert isinstance(entity, (Item, Property, Lexeme))
                print(var, '=', entity.describe_using_repr(), flush=True)
                entities.remove(entity)
            if not entities:
                break
            _LOGGER.info('%d unresolved entities, retrying', len(entities))
            entities = set(_output_filter_resolve_page(
                context,
                (e.replace(range=None)
                 if isinstance(e, Property) else e for e in entities),
                language))
    else:
        if encoder is None:
            it = map(Term.to_markdown, resolved_page)
            console.print(Markdown('\n\n'.join(it)))
        else:
            for term in resolved_page:
                print(encoder.encode(term).rstrip(), flush=True)


def _output_filter_resolve_page(
        context: Context,
        page: Iterable[Term],
        language: str | None = None
) -> Iterable[Term]:
    resolved_page: Iterable[Term] = list(context.resolve(
        page,
        batch_size=100,
        language=language,
        label=True,
        aliases=False,
        description=False,
        inverse=True,
        lemma=True,
        category=True,
        lexeme_language=True))
    ###
    # TODO: Make sure we also resolve the category and language of any
    # lexemes occurring in resolved page.  Should Context.resolve()
    # handle this?
    ###
    lexemes = itertools.chain(
        *(x.traverse(Lexeme.test) for x in resolved_page))
    context.resolve(itertools.chain(
        *((x.get_category(resolve=False),
           x.get_language(resolve=False))
          for x in lexemes)),
        language=language, label=True)
    return resolved_page


class SearchParam:
    """Common stuff for search-like commands."""

    text = click.argument(
        'text',
        type=str,
        required=True,
        envvar='TEXT')

    item = click.option(
        '--item',
        'item',
        is_flag=True,
        default=False,
        help='Alias: --type=item',
        envvar='ITEM')

    item_data = click.option(
        '--item-data',
        'item_data',
        is_flag=True,
        default=False,
        help='Alias: --type=item-data',
        envvar='ITEM_DATA')

    item_descriptor = click.option(
        '--item-descriptor',
        'item_descriptor',
        is_flag=True,
        default=False,
        help='Alias: --type=item-descriptor',
        envvar='ITEM_DESCRIPTOR')

    lexeme = click.option(
        '--lexeme',
        'lexeme',
        is_flag=True,
        default=False,
        help='Alias: --type=lexeme',
        envvar='LEXEME')

    lexeme_data = click.option(
        '--lexeme-data',
        'lexeme_data',
        is_flag=True,
        default=False,
        help='Alias: --type=lexeme-data',
        envvar='LEXEME_DATA')

    lexeme_descriptor = click.option(
        '--lexeme-descriptor',
        'lexeme_descriptor',
        is_flag=True,
        default=False,
        help='Alias: --type=lexeme-descriptor',
        envvar='LEXEME_DESCRIPTOR')

    property = click.option(
        '--property',
        'property',
        is_flag=True,
        default=False,
        help='Alias: --type=property',
        envvar='PROPERTY')

    property_data = click.option(
        '--property-data',
        'property_data',
        is_flag=True,
        default=False,
        help='Alias: --type=property-data',
        envvar='PROPERTY_DATA')

    property_descriptor = click.option(
        '--property-descriptor',
        'property_descriptor',
        is_flag=True,
        default=False,
        help='Alias: --type=property-descriptor',
        envvar='PROPERTY_DESCRIPTOR')

    type = click.option(
        '--type',
        'type',
        type=click.Choice([
            'item',
            'item-descriptor',
            'item-data',
            'lexeme',
            'lexeme-descriptor',
            'lexeme-data',
            'property',
            'property-descriptor',
            'property-data',
        ]),
        default='item',
        help='Type specification.',
        envvar='TYPE')

    async_ = FilterParam.async_

    encoder = FilterParam.encoder

    limit = FilterParam.limit

    lookahead = FilterParam.lookahead

    page_size = FilterParam.page_size

    search = click.option(
        '--search',
        '-s',
        'search',
        type=SearchParamType.get_instance(),
        multiple=True,
        help='Target search.',
        envvar='SEARCH')

    resolve = FilterParam.resolve

    timeout = FilterParam.timeout

    @classmethod
    def make_context(cls, resolve: bool | None = None) -> Context:
        return FilterParam.make_context(resolve)

    @classmethod
    def make_search(
            cls,
            search: Sequence[Search],
            limit: int | None = None,
            lookahead: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None
    ) -> Search:
        target: Search
        if len(search) == 0:
            target = Search('wikidata')
        elif len(search) == 1:
            target = search[0]
        else:
            ###
            # TODO: Handle more than one search.
            ###
            target = search[0]
        if limit is not None:
            target.set_limit(limit)
        if lookahead is not None:
            target.set_lookahead(lookahead)
        if page_size is not None:
            target.set_page_size(page_size)
        if timeout is not None:
            target.set_timeout(timeout)
        return target


@cli.command(help='Searches for entities matching text.')
@SearchParam.text
@SearchParam.async_
@SearchParam.encoder
@SearchParam.item
@SearchParam.item_data
@SearchParam.item_descriptor
@SearchParam.lexeme
@SearchParam.lexeme_data
@SearchParam.lexeme_descriptor
@SearchParam.limit
@SearchParam.page_size
@SearchParam.property
@SearchParam.property_data
@SearchParam.property_descriptor
@SearchParam.resolve
@SearchParam.search
@SearchParam.timeout
@SearchParam.type
def search(
        search: Sequence[Search],
        text: str,
        item: bool | None = None,
        item_data: bool | None = None,
        item_descriptor: bool | None = None,
        lexeme: bool | None = None,
        lexeme_data: bool | None = None,
        lexeme_descriptor: bool | None = None,
        property: bool | None = None,
        property_data: bool | None = None,
        property_descriptor: bool | None = None,
        async_: bool | None = None,
        encoder: Encoder | None = None,
        limit: int | None = None,
        lookahead: int | None = None,
        page_size: int | None = None,
        resolve: bool | None = None,
        timeout: float | None = None,
        type: str | None = None
) -> None:
    if item:
        type = 'item'
    if item_descriptor:
        type = 'item-descriptor'
    if item_data:
        type = 'item-data'
    if lexeme:
        type = 'lexeme'
    if lexeme_descriptor:
        type = 'lexeme-descriptor'
    if lexeme_data:
        type = 'lexeme-data'
    if property:
        type = 'property'
    if property_descriptor:
        type = 'property-descriptor'
    if property_data:
        type = 'property-data'

    def _search() -> None:
        target = SearchParam.make_search(
            search,
            limit=limit,
            lookahead=lookahead,
            page_size=page_size,
            timeout=timeout)
        output = functools.partial(
            _output_search_page,
            Console(),
            encoder=encoder,
            resolve=resolve,
            context=SearchParam.make_context(resolve))
        if async_:
            as_: dict[str, Callable[[], Union[
                AsyncIterator[Item],
                AsyncIterator[Lexeme],
                AsyncIterator[Property],
                AsyncIterator[tuple[Item, Item.Descriptor]],
                AsyncIterator[tuple[Lexeme, Lexeme.Descriptor]],
                AsyncIterator[tuple[Property, Property.Descriptor]],
                AsyncIterator[Search.TData]
            ]]] = {
                'item': (lambda: target.aitem(text)),
                'item-descriptor': (lambda: target.aitem_descriptor(text)),
                'item-data': (lambda: target.aitem_data(text)),
                'lexeme': (lambda: target.alexeme(text)),
                'lexeme-descriptor': (lambda: target.alexeme_descriptor(text)),
                'lexeme-data': (lambda: target.alexeme_data(text)),
                'property': (lambda: target.aproperty(text)),
                'property-descriptor': (
                    lambda: target.aproperty_descriptor(text)),
                'property-data': (lambda: target.aproperty_data(text))}

            async def asearch():
                assert type is not None
                it, i = as_[type](), 1
                while True:
                    page = await itertools.atake(target.page_size, it)
                    if not page:
                        break
                    output(type=type, page=page, pageno=i)  # type: ignore
                    i += 1
            asyncio.run(asearch())
        else:
            s: dict[str, Callable[[], Union[
                Iterator[Item],
                Iterator[Lexeme],
                Iterator[Property],
                Iterator[tuple[Item, Item.Descriptor]],
                Iterator[tuple[Lexeme, Lexeme.Descriptor]],
                Iterator[tuple[Property, Property.Descriptor]],
                Iterator[Search.TData]
            ]]] = {
                'item': (lambda: target.item(text)),
                'item-descriptor': (lambda: target.item_descriptor(text)),
                'item-data': (lambda: target.item_data(text)),
                'lexeme': (lambda: target.lexeme(text)),
                'lexeme-descriptor': (lambda: target.lexeme_descriptor(text)),
                'lexeme-data': (lambda: target.lexeme_data(text)),
                'property': (lambda: target.property(text)),
                'property-descriptor': (
                    lambda: target.property_descriptor(text)),
                'property-data': (lambda: target.property_data(text))}
            assert type is not None
            batches = itertools.batched(s[type](), target.page_size)
            for page, i in enumerate(batches, 1):
                output(type=type, page=page, pageno=i)  # type: ignore
    _run(_search)


def _output_search_page(
        console: Console,
        type: str,
        page: Union[
            Iterable[Item],
            Iterable[Lexeme],
            Iterable[Property],
            Iterable[tuple[Item, Item.Descriptor]],
            Iterable[tuple[Lexeme, Lexeme.Descriptor]],
            Iterable[tuple[Property, Property.Descriptor]],
            Iterable[Search.TData]],
        pageno: int,
        encoder: Encoder | None = None,
        resolve: bool | None = None,
        context: Context | None = None
) -> None:
    if type.endswith('data'):
        for data in page:
            console.print(pprint.pformat(data))
            console.print()
    else:
        output = functools.partial(
            _output_filter_page,
            console=console, pageno=pageno,
            encoder=encoder, resolve=resolve, context=context)
        if type.endswith('descriptor'):
            it = itertools.chain(*(
                (entity, SnakSet(
                    *entity.descriptor_to_snaks(desc)))  # type: ignore
                for entity, desc in page))
            output(page=cast(Iterable[Term], list(it)))
        else:
            output(page=cast(Iterable[Term], page))


if __name__ == '__main__':
    cli()
