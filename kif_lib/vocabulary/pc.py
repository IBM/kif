# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..model import Item, Property, Quantity
from ..namespace.pubchem import PubChem
from ..namespace.semsci import CHEMINF


def CID(name: int | str, label: str | None = None) -> Item:
    if isinstance(name, str) and name.startswith('CID'):
        name = PubChem.COMPOUND[name]
    else:
        name = PubChem.COMPOUND[f'CID{name}']
    return Item(name)


def patent(name: str, label: str | None = None) -> Item:
    return Item(PubChem.PATENT[name])


def source(name: str, label: str | None = None) -> Item:
    return Item(PubChem.SOURCE[name])


Isotope_Atom_Count = Property(
    CHEMINF.isotope_atom_count_generated_by_pubchem_software_library,
    Quantity)
