# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ....model import ExternalId, Item, Quantity, String, Variables
from ....namespace import RDF, XSD
from ....namespace.semsci import CHEMINF, SIO
from ....typing import TypeAlias
from ....vocabulary import pc, wd
from ..compiler import SPARQL_Compiler as Compiler
from .mapping import register, SPARQL_Mapping

__all__ = (
    'PubChemMapping',
)

V_URI: TypeAlias = Compiler.Query.V_URI
VLiteral: TypeAlias = Compiler.Query.VLiteral
x, y, z = Variables('x', 'y', 'z')


class PubChemMapping(SPARQL_Mapping):

    @register(
        wd.canonical_SMILES(Item(x), String(y)),
        {y: SPARQL_Mapping.preprocess_language_tag('en')})
    def wd_canonical_SMILES(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.canonical_smiles_generated_by_OEChem),
            (attr, SIO.has_value, y))

    @register(wd.has_part(Item(x), Item(y)))
    def wd_has_part(self, c: Compiler, x: V_URI, y: V_URI):
        c.q.triples()(
            (x, CHEMINF.has_component_with_uncharged_counterpart, y))

    @register(
        wd.instance_of(
            pc.Isotope_Atom_Count, wd.Wikidata_property_related_to_chemistry))
    def wd_instance_of_Isotope_Atom_Count(self, c: Compiler):
        pass                    # pseudo-entry

    @register(
        pc.Isotope_Atom_Count(Item(x), Quantity(y)),
        {y: SPARQL_Mapping.preprocess_datatype(XSD.int)})
    def pc_Isotope_Atom_Count(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             isotope_atom_count_generated_by_pubchem_software_library),
            (attr, SIO.has_value, y))

    @register(
        wd.mass(Item(x), Quantity(y, wd.gram_per_mole)),
        {y: SPARQL_Mapping.preprocess_datatype(XSD.float)})
    def wd_mass(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             molecular_weight_calculated_by_the_pubchem_software_library),
            (attr, SIO.has_value, y))

    @register(
        wd.PubChem_CID(Item(x), ExternalId(y)),
        {y: SPARQL_Mapping.preprocess_language_tag('en')})
    def wd_PubChem_CID(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID),
            (attr, SIO.has_value, y))
