# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...context import Context
from ...model import IRI, Item, Property, TDatatype, TProperty, TText, TTextSet
from ...namespace.factgrid import FactGrid
from ...typing import cast

__all__ = (
    'P',
    'Q',
    'reload',
)


def P(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        range: TDatatype | None = None,
        inverse: TProperty | None = None,
        context: Context | None = None
) -> Property:
    """Creates a FactGrid property with the given descriptors.

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
    if isinstance(name, str) and name[0] == 'P':
        iri = IRI(str(FactGrid.WD[name]))
    else:
        iri = IRI(str(FactGrid.WD[f'P{name}']))
    return Context.top(context).entities.register(
        Property(iri),
        label=label, aliases=aliases, description=description,
        range=range, inverse=inverse)


def Q(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a FactGrid item with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       context: KIF context.

    Returns:
       Item.
    """
    if isinstance(name, str) and name[0] == 'Q':
        iri = IRI(str(FactGrid.WD[name]))
    else:
        iri = IRI(str(FactGrid.WD[f'Q{name}']))
    return Context.top(context).entities.register(
        Item(iri), label=label, aliases=aliases, description=description)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `fg` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(FactGrid.WD, prefix='fg')
    ctx.iris.register(IRI(FactGrid.WD), schema=cast(Property.Schema, {
        k: IRI(str(v)) for k, v in FactGrid.schema.items()}))
    resolver_iri = ctx.options.vocabulary.fg.resolver
    if resolver_iri is not None:
        from ...store import Store
        kb = Store('factgrid-sparql', resolver_iri)
        ctx.iris.register(FactGrid.WD, resolver=kb)
    if force:
        import importlib

        from . import item, property
        importlib.reload(item)
        importlib.reload(property)

reload(force=False)
