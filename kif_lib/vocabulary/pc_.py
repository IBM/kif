# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..context import Context
from ..model import Item, Property, Quantity, TText, TTextSet
from ..namespace.pubchem import PubChem
from ..namespace.semsci import CHEMINF


def CID(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a PubChem compound item with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       context: KIF context.

    Returns:
       Item.
    """
    if isinstance(name, str) and name.startswith('CID'):
        name = PubChem.COMPOUND[name]
    else:
        name = PubChem.COMPOUND[f'CID{name}']
    return Context.top(context).entities.register(
        Item(name), label=label, aliases=aliases, description=description)


def patent(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a PubChem patent item with the given descriptors.

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
        Item(PubChem.PATENT[name]),
        label=label, aliases=aliases, description=description)


def source(
        name: str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a PubChem source item with the given descriptors.

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
        Item(PubChem.SOURCE[name]),
        label=label, aliases=aliases, description=description)


Isotope_Atom_Count = Property(
    CHEMINF.isotope_atom_count_generated_by_pubchem_software_library,
    Quantity)
