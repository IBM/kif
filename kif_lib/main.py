# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import click

from .store import Store
from .version import __version__


@click.command()
def main() -> None:
    click.echo(
        f'KIF version: {__version__}')
    click.echo(
        f'KIF store plugins: {", ".join(sorted(Store.registry.keys()))}')
