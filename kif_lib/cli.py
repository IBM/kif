# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import click

from . import __description__, __version__
from .model import KIF_Object
from .store import Store
from .typing import Callable, Iterable, Sequence


@click.group(help=f'KIF: {__description__}.')
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command(help='Show the available decoders and exit.')
def list_decoders() -> None:
    from .model.kif_object import Decoder
    _list_name_description_pairs(
        ((k, v.description) for k, v in Decoder.registry.items()))


@cli.command(help='Show the available encoders and exit.')
def list_encoders() -> None:
    from .model.kif_object import Encoder
    _list_name_description_pairs(
        ((k, v.description) for k, v in Encoder.registry.items()))


@cli.command(help='Show the available stores and exit.')
def list_stores() -> None:
    _list_name_description_pairs(
        ((k, v.store_description) for k, v in Store.registry.items()))


def _list_name_description_pairs(pairs: Iterable[tuple[str, str]]) -> None:
    pairs = list(pairs)
    longest_name_length = max(map(len, map(lambda t: t[0], pairs)))
    for k, v in sorted(pairs):
        click.echo(f'{k:<{longest_name_length}}: {v}')


@cli.command(help='Searches for statements matching filter.')
@click.argument(
    'input',
    metavar='[INPUT_SPEC]...',
    type=str,
    nargs=-1,
    required=False,
)
@click.option(
    '--limit',
    '-l',
    'limit',
    type=int,
    default=10,
    help='Maximum number of results.',
)
@click.option(
    '--property',
    '-p',
    'property',
    metavar='FINGERPRINT',
    type=str,
    required=False,
    help='Property fingerprint.',
)
@click.option(
    '--subject',
    '-s',
    'subject',
    metavar='FINGERPRINT',
    type=str,
    required=False,
    help='Subject fingerprint.',
)
@click.option(
    '--value',
    '-v',
    'value',
    metavar='FINGERPRINT',
    type=str,
    required=False,
    help='Value fingerprint.',
)
def filter(
        input: Sequence[str],
        limit: int,
        property: str | None = None,
        subject: str | None = None,
        value: str | None = None,
) -> None:
    from .vocabulary import db, pc, wd

    _G = {'db': db, 'pc': pc, 'wd': wd}
    pr = _get_kif_object_printer()
    kb = Store('wdqs', limit=limit)
    it = kb.filter(
        subject=eval(str(subject), globals=_G),
        property=eval(str(property), globals=_G),
        value=eval(str(value), globals=_G),
    )
    for stmt in it:
        pr(stmt)


def _get_kif_object_printer() -> Callable[[KIF_Object], None]:
    try:
        from rich.console import Console
        from rich.markdown import Markdown

        console = Console()
        return lambda obj: console.print(Markdown(obj.to_markdown()))
    except ImportError:
        return lambda obj: click.echo(obj.to_sexp())


if __name__ == '__main__':
    cli()
