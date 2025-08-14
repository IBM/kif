# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...context import Context
from ...model import Item, TText, TTextSet
from ...namespace.europa import Europa

__all__ = (
    'Dataset',
    'reload',
)


def Dataset(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a Europa dataset item with the given descriptors.

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
        Item(Europa.DATASET[name]),
        label=label, aliases=aliases, description=description)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `db` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(Europa.DATASET, prefix='eu_dataset')
    ctx.iris.register(Europa.EUROPA, prefix='eu')
    resolver_iri = ctx.options.vocabulary.eu.resolver
    if resolver_iri is not None:
        from ...store import Store
        kb = Store('europa-sparql', resolver_iri)
        ctx.iris.register(Europa.DATASET, resolver=kb)
        ctx.iris.register(Europa.EUROPA, resolver=kb)


reload(force=False)
