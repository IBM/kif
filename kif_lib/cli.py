# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import functools
import os
import re
import sys

try:
    import click
except ImportError as err:
    raise ImportError(
        f'{__name__} requires https://pypi.org/project/click/') from err

try:
    from rich.console import Console
    from rich.markdown import Markdown
except ImportError as err:
    raise ImportError(
        f'{__name__} requires https://pypi.org/project/rich/') from err

from . import __description__, __version__, itertools
from .context import Context
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
    SomeValueSnak,
    Statement,
    String,
    Text,
    Value,
    ValueSnak,
)
from .model.object import Decoder, Encoder
from .store import Store
from .typing import (
    Any,
    ClassVar,
    Final,
    Iterable,
    override,
    Self,
    Sequence,
    TypeVar,
)
from .vocabulary import db, pc, wd

TObj = TypeVar('TObj', bound=KIF_Object)

#: The globals table to be passed to :func:`eval`.
_G: Final[dict[str, Any]] = {}


@click.group(help=f'KIF: {__description__}.')
@click.version_option(version=__version__)
@click.option(
    '--module',
    '-m',
    metavar='MOD',
    multiple=True,
    help='Load module MOD.')
def cli(module: Sequence[str] = ()) -> None:
    if module:
        import importlib
        sys.path.append(os.getcwd())
        for mod in module:
            global _G           # noqa: F824
            _G[mod] = importlib.import_module(mod)


@cli.command(help='Show the available decoders and exit.')
def list_decoders() -> None:
    _list_name_description_pairs(
        ((k, v.description) for k, v in Decoder.registry.items()))


@cli.command(help='Show the available encoders and exit.')
def list_encoders() -> None:
    _list_name_description_pairs(
        ((k, v.description) for k, v in Encoder.registry.items()))


@cli.command(help='Show KIF context options and exit.')
@click.argument(
    'name',
    type=str,
    default='kif'
)
@click.option(
    '--describe',
    '-d',
    'describe',
    is_flag=True,
    default=False,
    help='Show option description.')
def list_options(name: str, describe: bool | None = None) -> None:
    ctx = Context.top()
    if describe:
        click.echo(ctx.get_option_description_by_name(name))
    else:
        click.echo(ctx.get_option_by_name(name))


@cli.command(help='Show the available stores and exit.')
def list_stores() -> None:
    _list_name_description_pairs(
        ((k, v.store_description) for k, v in Store.registry.items()))


def _list_name_description_pairs(pairs: Iterable[tuple[str, str]]) -> None:
    pairs = list(pairs)
    longest_name_length = max(map(len, map(lambda t: t[0], pairs)))
    for k, v in sorted(pairs):
        click.echo(f'{k:<{longest_name_length}}: {v}')


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
            'DATA_VALUE': Filter.DATA_VALUE,
            'DataValue': DataValue,
            'db': db,
            'Decoder': Decoder,
            'DEEP_DATA_VALUE': Filter.DEEP_DATA_VALUE,
            'DeepDataValue': DeepDataValue,
            'Deprecated': Deprecated,
            'DEPRECATED': Filter.DEPRECATED,
            'Encoder': Encoder,
            'Entity': Entity,
            'ENTITY': Filter.ENTITY,
            'EXTERNAL_ID': Filter.EXTERNAL_ID,
            'ExternalId': ExternalId,
            'Filter': Filter,
            'IRI': IRI,
            'ITEM': Filter.ITEM,
            'Item': Item,
            'LEXEME': Filter.LEXEME,
            'Lexeme': Lexeme,
            'NO_VALUE_SNAK': Filter.NO_VALUE_SNAK,
            'NORMAL': Filter.NORMAL,
            'Normal': Normal,
            'NoValueSnak': NoValueSnak,
            'pc': pc,
            'PREFERRED': Filter.PREFERRED,
            'Preferred': Preferred,
            'PROPERTY': Filter.PROPERTY,
            'Property': Property,
            'QUANTITY': Filter.QUANTITY,
            'Quantity': Quantity,
            'SHALLOW_DATA_VALUE': Filter.SHALLOW_DATA_VALUE,
            'ShallowDataValue': ShallowDataValue,
            'SOME_VALUE_SNAK': Filter.SOME_VALUE_SNAK,
            'SomeValueSnak': SomeValueSnak,
            'STIRNG': Filter.STRING,
            'Store': Store,
            'STRING': Filter.STRING,
            'String': String,
            'TEXT': Filter.TEXT,
            'Text': Text,
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


class StoreParamType(KIF_ParamType):

    name: str = 'store'

    @override
    def convert(
            self,
            value: Any,
            param: click.Parameter | None,
            ctx: click.Context | None
    ) -> Store:
        if isinstance(value, str):
            for store_name in Store.registry.keys():
                m = re.match(f'^{store_name}(@(.*))?$', value)
                if m is not None:
                    input_sources = m.group(2)
                    if input_sources:
                        return Store(store_name, *input_sources.split(';'))
                    else:
                        return Store(store_name)
        try:
            return KIF_Object._check_arg_isinstance(self.eval(value), Store)
        except (ValueError, TypeError) as err:
            return self.fail(str(err), param, ctx)

    @override
    def split_envvar_value(self, rv: str) -> Sequence[str]:  # type: ignore
        return (rv or '').split(';')


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

    no_async_ = click.option(
        '--no-async',
        'async_',
        is_flag=True,
        default=True,
        help='Do not use the asynchronous API.',
        envvar='ASYNC')

    no_distinct = click.option(
        '--no-distinct',
        'distinct',
        is_flag=True,
        default=True,
        help='Do not suppress duplicates.',
        envvar='DISTINCT')

    no_resolve = click.option(
        '--no-resolve',
        'resolve',
        is_flag=True,
        default=True,
        help='Do not resolve entity labels.',
        envvar='RESOLVE')

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
        type=DatatypeMaskParamType.get_instance(),
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

    value_mask = click.option(
        '--value-mask',
        'value_mask',
        type=DatatypeMaskParamType.get_instance(),
        required=False,
        help='Value datatype mask.',
        envvar='VALUE_MASK')

    @classmethod
    def make_context(
            cls,
            resolve: bool | None = None
    ) -> Context:
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
            snak_mask: Filter.SnakMask | None = None,
            subject_mask: Filter.DatatypeMask | None = None,
            property_mask: Filter.DatatypeMask | None = None,
            value_mask: Filter.DatatypeMask | None = None,
            rank_mask: Filter.RankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            dry_run: bool | None = None,
            console: Console | None = None
    ) -> Filter:
        fr = Filter(
            subject=And(subject, subject_option),
            property=And(property, property_option),
            value=And(value, value_option),
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
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
        if page_size is not None:
            target.set_page_size(page_size)
        if timeout is not None:
            target.set_timeout(timeout)
        return target


@cli.command(help='Tests whether some statement matches filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.dry_run
@FilterParam.language
@FilterParam.no_async_
@FilterParam.property_option
@FilterParam.property_mask
@FilterParam.rank_mask
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_option
@FilterParam.subject_mask
@FilterParam.timeout
@FilterParam.value_option
@FilterParam.value_mask
def ask(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.DatatypeMask | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        language: str | None = None,
        async_: bool | None = None,
        dry_run: bool | None = None,
        timeout: float | None = None
) -> None:
    fr = FilterParam.make_filter(
        subject=subject,
        subject_option=subject_option,
        property=property,
        property_option=property_option,
        value=value,
        value_option=value_option,
        snak_mask=snak_mask,
        subject_mask=subject_mask,
        property_mask=property_mask,
        value_mask=value_mask,
        rank_mask=rank_mask,
        language=language,
        dry_run=dry_run)
    target = FilterParam.make_store(store=store, timeout=timeout)
    status: bool
    if async_:
        async def aask():
            return await target.aask(filter=fr)
        status = asyncio.run(aask())
    else:
        status = target.ask(filter=fr)
    sys.exit(int(not status))


@cli.command(help='Counts the number of statements matching filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.annotated
@FilterParam.dry_run
@FilterParam.language
@FilterParam.no_async_
@FilterParam.no_distinct
@FilterParam.property_option
@FilterParam.property_mask
@FilterParam.rank_mask
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_option
@FilterParam.subject_mask
@FilterParam.timeout
@FilterParam.value_option
@FilterParam.value_mask
def count(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.DatatypeMask | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        language: str | None = None,
        annotated: bool | None = None,
        async_: bool | None = None,
        distinct: bool | None = None,
        dry_run: bool | None = None,
        timeout: float | None = None
) -> None:
    fr = FilterParam.make_filter(
        subject=subject,
        subject_option=subject_option,
        property=property,
        property_option=property_option,
        value=value,
        value_option=value_option,
        snak_mask=snak_mask,
        subject_mask=subject_mask,
        property_mask=property_mask,
        value_mask=value_mask,
        rank_mask=rank_mask,
        language=language,
        dry_run=dry_run)
    target = FilterParam.make_store(
        store=store,
        distinct=distinct,
        timeout=timeout)
    n: int
    if async_:
        async def acount():
            return await target.acount(filter=fr)
        n = asyncio.run(acount())
    else:
        n = target.count(filter=fr)
    click.echo(n)


@cli.command(help='Searches for statements matching filter.')
@FilterParam.subject
@FilterParam.property
@FilterParam.value
@FilterParam.annotated
@FilterParam.dry_run
@FilterParam.encoder
@FilterParam.language
@FilterParam.limit
@FilterParam.lookahead
@FilterParam.no_async_
@FilterParam.no_distinct
@FilterParam.no_resolve
@FilterParam.page_size
@FilterParam.property_option
@FilterParam.property_mask
@FilterParam.rank_mask
@FilterParam.snak_mask
@FilterParam.store
@FilterParam.subject_option
@FilterParam.subject_mask
@FilterParam.timeout
@FilterParam.value_option
@FilterParam.value_mask
def filter(
        store: Sequence[Store],
        subject: Fingerprint | None = None,
        subject_option: Fingerprint | None = None,
        property: Fingerprint | None = None,
        property_option: Fingerprint | None = None,
        value: Fingerprint | None = None,
        value_option: Fingerprint | None = None,
        snak_mask: Filter.SnakMask | None = None,
        subject_mask: Filter.DatatypeMask | None = None,
        property_mask: Filter.DatatypeMask | None = None,
        value_mask: Filter.DatatypeMask | None = None,
        rank_mask: Filter.RankMask | None = None,
        language: str | None = None,
        annotated: bool | None = None,
        async_: bool | None = None,
        distinct: bool | None = None,
        dry_run: bool | None = None,
        encoder: Encoder | None = None,
        limit: int | None = None,
        lookahead: int | None = None,
        page_size: int | None = None,
        resolve: bool | None = None,
        timeout: float | None = None
) -> None:
    console = Console()
    context = FilterParam.make_context(resolve)
    fr = FilterParam.make_filter(
        subject=subject,
        subject_option=subject_option,
        property=property,
        property_option=property_option,
        value=value,
        value_option=value_option,
        snak_mask=snak_mask,
        subject_mask=subject_mask,
        property_mask=property_mask,
        value_mask=value_mask,
        rank_mask=rank_mask,
        language=language,
        annotated=annotated,
        dry_run=dry_run,
        console=console)
    target = FilterParam.make_store(
        store=store,
        distinct=distinct,
        limit=limit,
        lookahead=lookahead,
        page_size=page_size,
        timeout=timeout)

    def output(
            page: Iterable[Statement],
            pageno: int
    ) -> None:
        if resolve:
            resolved_page = context.resolve(
                page, label=True, language='en')
        else:
            resolved_page = page
        if encoder is None:
            ###
            # FIXME: This is not working!
            ###
            # it = (f'{(pageno * target.page_size) + i}.\t'
            #       + textwrap.indent(stmt.to_markdown(), '\t').lstrip()
            #       for i, stmt in enumerate(resolved_page, 1))
            ###
            it = map(Statement.to_markdown, resolved_page)
            console.print(Markdown('\n\n'.join(it)))
        else:
            for stmt in resolved_page:
                print(encoder.encode(stmt).rstrip(), flush=True)
    if async_:
        async def afilter():
            it, n = target.afilter(filter=fr), 0
            while True:
                page = await itertools.atake(target.page_size, it)
                if not page:
                    break
                output(page, n)
                n += 1
        asyncio.run(afilter())
    else:
        batches = itertools.batched(
            target.filter(filter=fr), target.page_size)
        for pageno, page in enumerate(batches):
            output(page, pageno)


if __name__ == '__main__':
    cli()
