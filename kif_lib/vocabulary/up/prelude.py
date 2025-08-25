# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...context import Context
from ...model import Item, TText, TTextSet
from ...namespace.uniprot import UniProt

__all__ = (
    'taxonomy',
    'reload',
)


def taxonomy(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a UniProt taxonomy item with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       context: KIF context.

    Returns:
       Item.
    """
    return Context.top(context).entities.register(
        Item(UniProt.TAXONOMY[str(name)]),
        label=label, aliases=aliases, description=description)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `eu` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(UniProt.TAXONOMY, prefix='up_taxonomy')
    resolver_iri = ctx.options.vocabulary.up.resolver
    if resolver_iri is not None:
        from ...store import Store
        kb = Store('uniprot-sparql', resolver_iri)
        ctx.iris.register(UniProt.TAXONOMY, resolver=kb)


reload(force=False)
