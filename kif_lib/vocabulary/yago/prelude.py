# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...context import Context
from ...model import Item, Property, TDatatype, TProperty, TText, TTextSet
from ...namespace.yago import YAGO

__all__ = (
    'P',
    'Q',
    'reload',
)


def P(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        range: TDatatype | None = None,
        inverse: TProperty | None = None,
        context: Context | None = None
) -> Property:
    """Creates a Yago property with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       range: Datatype.
       inverse: Inverse property.
       context: KIF context.

    Returns:
       Property.
    """
    return Context.top(context).entities.register(
        Property(YAGO[name]),
        label=label, aliases=aliases, description=description,
        range=range, inverse=inverse)


def Q(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a Yago item with the given descriptors.

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
        Item(YAGO[name]),
        label=label, aliases=aliases, description=description)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `yago` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(YAGO, prefix='yago')
    resolver_iri = ctx.options.vocabulary.yago.resolver
    if resolver_iri is not None:
        from ...store import Store
        kb = Store('yago-sparql', resolver_iri)
        ctx.iris.register(YAGO, resolver=kb)


reload(force=False)
