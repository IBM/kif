# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from ....model import (
    ExternalId,
    IRI,
    Item,
    Quantity,
    String,
    Text,
    Time,
    Variables,
)
from ....namespace import RDF, SKOS, Wikidata, XSD
from ....namespace.cito import CITO
from ....namespace.patent import PATENT
from ....namespace.pubchem import PubChem
from ....namespace.semsci import CHEMINF, SIO
from ....namespace.vcard import VCARD
from ....typing import TypeAlias
from ....vocabulary import pc, wd
from ..compiler import SPARQL_Compiler as Compiler
from .mapping import SPARQL_Mapping as M

__all__ = (
    'PubChemMapping',
)

URI: TypeAlias = Compiler.Query.URI
V_URI: TypeAlias = Compiler.Query.V_URI
VLiteral: TypeAlias = Compiler.Query.VLiteral
x, y, z = Variables('x', 'y', 'z')


class PubChemMapping(M):

    @M.register(
        wd.instance_of(
            pc.Isotope_Atom_Count, wd.Wikidata_property_related_to_chemistry))
    def wd_instance_of_Isotope_Atom_Count(self, c: Compiler):
        pass                    # pseudo-entry

# -- Compound --------------------------------------------------------------

    class CheckCompound(M.CheckRegex):
        def __init__(self):
            super().__init__(
                f'^{re.escape(PubChem.COMPOUND)}CID[1-9][0-9]+$')

    class CheckCanonicalSMILES(M.CheckRegex):
        def __init__(self):
            super().__init__(r'^[A-Za-z0-9+\-\*=#$:()\.>/\\\[\]%]+$')

    class CheckPubChemCID(M.CheckRegex):
        def __init__(self):
            super().__init__(r'^[1-9][0-9]+$')

    @M.register(
        wd.canonical_SMILES(Item(x), String(y)),
        {x: CheckCompound(),
         y: CheckCanonicalSMILES() >> M.PatchLiteral(language='en')})
    def wd_canonical_SMILES(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.canonical_smiles_generated_by_OEChem),
            (attr, SIO.has_value, y))

    @M.register(
        wd.exact_match(Item(x), IRI(y)),
        {x: M.UpdatePrefix(Wikidata.WD, 'https://www.wikidata.org/wiki/'),
         y: CheckCompound()})
    def wd_exact_match(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()(
            (c.query.URI(y) if isinstance(y, c.Query.Literal) else y,
             SKOS.closeMatch, x))

    @M.register(
        wd.has_part(Item(x), Item(y)),
        {x: CheckCompound(),
         y: CheckCompound()})
    def wd_has_part(self, c: Compiler, x: V_URI, y: V_URI):
        c.q.triples()(
            (x, CHEMINF.has_component_with_uncharged_counterpart, y))

    @M.register(
        wd.instance_of(Item(x), wd.type_of_a_chemical_entity),
        {x: CheckCompound()})
    def wd_instance_of_type_of_a_chemical_entity(self, c: Compiler, x: V_URI):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID))

    @M.register(
        pc.Isotope_Atom_Count(Item(x), Quantity(y)),
        {x: CheckCompound(),
         y: M.PatchLiteral(datatype=XSD.int)})
    def pc_Isotope_Atom_Count(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             isotope_atom_count_generated_by_pubchem_software_library),
            (attr, SIO.has_value, y))

    @M.register(
        wd.mass(Item(x), Quantity(y, wd.gram_per_mole)),
        {x: CheckCompound(),
         y: M.PatchLiteral(datatype=XSD.float)})
    def wd_mass(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             molecular_weight_calculated_by_the_pubchem_software_library),
            (attr, SIO.has_value, y))

    @M.register(
        wd.PubChem_CID(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckPubChemCID() >> M.PatchLiteral(language='en')})
    def wd_PubChem_CID(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID),
            (attr, SIO.has_value, y))

# -- Patent ----------------------------------------------------------------

    class CheckPatent(M.CheckPrefix):
        def __init__(self):
            super().__init__(PubChem.PATENT)

    @M.register(
        wd.author_name_string(Item(x), String(y)),
        {x: CheckPatent()})
    def wd_author_name_string(self, c: Compiler, x: V_URI, y: VLiteral):
        vcard = c.bnode()
        c.q.triples()(
            (x, PATENT.inventorVC, vcard),
            (vcard, VCARD.fn, y))

    @M.register(
        wd.instance_of(Item(x), wd.patent),
        {x: CheckPatent()})
    def wd_instance_of_patent(self, c: Compiler, x: V_URI):
        c.q.triples()((x, RDF.type, PATENT.Publication))

    @M.register(
        wd.main_subject(Item(x), Item(y)),
        {x: CheckPatent(),
         y: CheckCompound()})
    def wd_main_subject(self, c: Compiler, x: V_URI, y: V_URI):
        attr = c.bnode()
        c.q.triples()(
            (y, CITO.isDiscussedBy, x),
            (x, RDF.type, PATENT.Publication),
            (y, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID))

    @M.register(
        wd.patent_number(Item(x), ExternalId(y)),
        {x: CheckPatent()})
    def wd_patent_number(self, c: Compiler, x: V_URI, y: V_URI):
        c.q.triples()((x, PATENT.publicationNumber, y))

    @M.register(
        wd.publication_date(
            Item(x), Time(y, Time.DAY, 0, wd.proleptic_Gregorian_calendar)),
        {x: CheckPatent()})
    def wd_publication_date(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()((x, PATENT.publicationDate, y))

    @M.register(
        wd.title(Item(x), Text(y, 'en')),
        {x: CheckPatent(),
         y: M.PatchLiteral(language='en')})
    def wd_title(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()((x, PATENT.titleOfInvention, y))
