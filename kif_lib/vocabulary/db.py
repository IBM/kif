# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..context import Context
from ..model import Item, Property, TDatatype, TProperty, TText, TTextSet
from ..namespace.dbpedia import DBpedia

__all__ = (
    'oc',
    'op',
    'r',
)


def oc(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a DBpedia ontology item with the given descriptors.

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
        Item(DBpedia.ONTOLOGY[name]),
        label=label, aliases=aliases, description=description)


def op(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        range: TDatatype | None = None,
        inverse: TProperty | None = None,
        context: Context | None = None
) -> Property:
    """Creates a DBpedia ontology property with the given descriptors.

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
        Property(DBpedia.ONTOLOGY[name]),
        label=label, aliases=aliases, description=description,
        range=range, inverse=inverse)


def r(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a DBpedia resource item with the given descriptors.

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
        Item(DBpedia.RESOURCE[name]),
        label=label, aliases=aliases, description=description)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `db` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(DBpedia.ONTOLOGY, prefix='dbo')
    ctx.iris.register(DBpedia.PROPERTY, prefix='dbp')
    ctx.iris.register(DBpedia.RESOURCE, prefix='dbr')
    resolver_iri = ctx.options.vocabulary.db.resolver
    if resolver_iri is not None:
        from ..store import Store
        kb = Store('dbpedia-sparql', resolver_iri)
        ctx.iris.register(DBpedia.ONTOLOGY, resolver=kb)
        ctx.iris.register(DBpedia.PROPERTY, resolver=kb)
        ctx.iris.register(DBpedia.RESOURCE, resolver=kb)
    if force:
        import importlib

        from . import db
        importlib.reload(db)


reload(force=False)
