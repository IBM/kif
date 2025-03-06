# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..context import Context
from ..namespace.pubchem import PubChem
from .pc_ import CID, Isotope_Atom_Count, patent, source

__all__ = (
    'CID',
    'Isotope_Atom_Count',
    'patent',
    'reload',
    'source',
)


def reload(force: bool = True, context: Context | None = None) -> None:
    """Reloads the `pc` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    ctx = Context.top(context)
    ctx.iris.register(PubChem.COMPOUND, prefix='pc')
    resolver_iri = ctx.options.vocabulary.pc.resolver
    if resolver_iri is not None:
        from ..compiler.sparql.mapping.pubchem import PubChemMapping
        from ..store import Store
        kb = Store('sparql2', resolver_iri, PubChemMapping())
        ctx.iris.register(PubChem.COMPOUND, resolver=kb)
        ctx.iris.register(PubChem.PATENT, resolver=kb)
        ctx.iris.register(PubChem.SOURCE, resolver=kb)
    if force:
        import importlib

        from . import pc
        importlib.reload(pc)


reload(force=False)
