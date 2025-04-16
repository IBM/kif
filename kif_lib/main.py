# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import click

from . import __description__, __title__, __version__
from .store import Store


@click.command()
def main() -> None:
    click.echo(f'''\
KIF __title__       : {__title__}
KIF __version__     : {__version__}
KIF __description__ : {__description__}
KIF store plugins   : {", ".join(sorted(Store.registry.keys()))}
    ''')
