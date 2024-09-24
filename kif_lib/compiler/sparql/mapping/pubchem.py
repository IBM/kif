# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
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
from ....namespace import DCT, RDF, SKOS, Wikidata, XSD
from ....namespace.cito import CITO
from ....namespace.obo import RO
from ....namespace.patent import PATENT
from ....namespace.pubchem import PubChem
from ....namespace.semsci import CHEMINF, SIO
from ....namespace.vcard import VCARD
from ....typing import Final, TypeAlias
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

    _re_canonical_smiles: Final[re.Pattern] = re.compile(
        r'^[A-Za-z0-9+\-\*=#$:()\.>/\\\[\]%]+$')

    _re_cas_registry_number: Final[re.Pattern] = re.compile(
        r'^\d+-\d+-\d+$')

    _re_chebi_id: Final[re.Pattern] = re.compile(
        r'^[1-9][0-9]*$')

    _re_chembl_id: Final[re.Pattern] = re.compile(
        r'^CHEMBL\d+$')

    _re_compound_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(PubChem.COMPOUND)}CID[1-9][0-9]*$')

    _re_inchikey: Final[re.Pattern] = re.compile(
        r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$')

    _re_patent_number: Final[re.Pattern] = re.compile(
        r'^[A-Z][A-Z]-[1-9][0-9]*(-[A-Z]+[1-9][0-9]*)?$')

    _re_patent_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(PubChem.PATENT)}'
        r'[A-Z][A-Z]-[1-9][0-9]*(-[A-Z]+[1-9][0-9]*)?$')

    _re_pubchem_cid: Final[re.Pattern] = re.compile(
        r'^[1-9][0-9]*$')

    _re_source: Final[re.Pattern] = re.compile(
        f'^{re.escape(PubChem.SOURCE)}[a-zA-Z0-9-_-]+$')

    #: Checks whether argument is a canonical SMILES value.
    CheckCanonicalSMILES: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_canonical_smiles)

    #: Checks whether argument is a CAS Registry Number.
    CheckCAS_RegistryNumber: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_cas_registry_number)

    #: Checks whether argument is a ChEBI id.
    CheckChEBI_ID: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_chebi_id)

    #: Checks whether argument is a ChEMBL id.
    CheckChEMBL_ID: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_chembl_id)

    #: Checks whether argument is a compound URI.
    CheckCompound: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_compound_uri)

    #: Checks whether argument is a valid InChI value.
    CheckInChI: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, startswith='InChI=')

    #: Checks whether argument is a valid InChIKey value.
    CheckInChIKey: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_inchikey)

    #: Checks whether argument is a patent.
    CheckPatent: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_patent_uri)

    #: Checks whether argument is a patent number.
    CheckPatentNumber: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_patent_number)

    #: Checks whether argument is a valid PubChem CID value.
    CheckPubChemCID: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckLiteral, match=_re_pubchem_cid)

    #: Checks whether argument is a source.
    CheckSource: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_source)

# -- Non-Wikidata Properties -----------------------------------------------

    @M.register(
        wd.instance_of(
            pc.Isotope_Atom_Count, wd.Wikidata_property_related_to_chemistry))
    def wd_instance_of_Isotope_Atom_Count(self, c: Compiler):
        pass                    # pseudo-entry

# -- Compound --------------------------------------------------------------

    @M.register(
        wd.canonical_SMILES(Item(x), String(y)),
        {x: CheckCompound(),
         y: CheckCanonicalSMILES(set_language='en')})
    def wd_canonical_SMILES(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.canonical_smiles_generated_by_OEChem),
            (attr, SIO.has_value, y))

    @M.register(
        wd.CAS_Registry_Number(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckCAS_RegistryNumber()})
    def wd_CAS_Registry_Number(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, x),
            (attr, RDF.type, CHEMINF.CAS_registry_number),
            (attr, SIO.has_value, y))

    @M.register(
        wd.ChEBI_ID(Item(x), ExternalId(y)),
        {x: CheckCompound(),    # pre
         y: CheckChEBI_ID() >> M.CheckStr(replace_prefix=('', 'CHEBI:'))},
        {y: M.CheckLiteral(sub=(r'^(chebi|CHEBI):(\d+)$', r'\2'))})  # post
    def wd_ChEBI_ID(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, x),
            (attr, RDF.type, CHEMINF.ChEBI_identifier),
            (attr, SIO.has_value, y))
        c.q.filter(c.q.strstarts(y, 'CHEBI:'))

    @M.register(
        wd.ChEMBL_ID(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckChEMBL_ID()})
    def wd_ChEMBL_ID(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, x),
            (attr, RDF.type, CHEMINF.ChEMBL_identifier),
            (attr, SIO.has_value, y))
        c.q.filter(c.q.strstarts(y, 'CHEMBL'))

    @M.register(
        wd.exact_match(Item(x), IRI(y)),
        {x: M.CheckURI(         # pre
            replace_prefix=(Wikidata.WD, 'https://www.wikidata.org/wiki/')),
         y: M.CheckLiteral(match=_re_compound_uri)},
        {x: M.CheckURI(         # post
            replace_prefix=('https://www.wikidata.org/wiki/', Wikidata.WD))})
    def wd_exact_match(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()(
            (c.query.URI(y) if isinstance(y, c.Query.Literal) else y,
             SKOS.closeMatch, x))

    @M.register(                # TODO: wd.part_of
        wd.has_part(Item(x), Item(y)),
        {x: CheckCompound(),
         y: CheckCompound()})
    def wd_has_part(self, c: Compiler, x: V_URI, y: V_URI):
        c.q.triples()(
            (x, CHEMINF.has_component_with_uncharged_counterpart, y))

    @M.register(
        wd.InChI(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckInChI(set_language='en')})
    def wd_InChI(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type,
             CHEMINF.InChI_calculated_by_library_version_1_0_4),
            (attr, SIO.has_value, y))

    @M.register(
        wd.InChIKey(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckInChIKey(set_language='en')})
    def wd_InChIKey(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, x),
            (attr, RDF.type,
             CHEMINF.InChIKey_generated_by_software_version_1_0_4),
            (attr, SIO.has_value, y))

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
         y: M.CheckLiteral(set_datatype=XSD.int)})
    def pc_Isotope_Atom_Count(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             isotope_atom_count_generated_by_pubchem_software_library),
            (attr, SIO.has_value, y))

    @M.register(
        wd.isomeric_SMILES(Item(x), String(y)),
        {x: CheckCompound(),
         y: M.CheckLiteral(set_language='en')})
    def wd_isomeric_SMILES(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.isomeric_SMILES_generated_by_OEChem),
            (attr, SIO.has_value, y))

    @M.register(
        wd.legal_status(Item(x), wd.FDA_approved),
        {x: CheckCompound()})
    def wd_legal_status(self, c: Compiler, x: V_URI):
        c.q.triples()(
            (x, RO.has_role, PubChem.VOCABULARY.FDAApprovedDrugs))

    @M.register(
        wd.mass(Item(x), Quantity(y, wd.gram_per_mole)),
        {x: CheckCompound(),
         y: M.CheckLiteral(set_datatype=XSD.float)})
    def wd_mass(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             molecular_weight_calculated_by_the_pubchem_software_library),
            (attr, SIO.has_value, y))

    @M.register(                # TODO: inverse
        wd.manufacturer(Item(x), Item(y)),
        {x: CheckCompound(),
         y: CheckSource()})
    def wd_manufacturer(self, c: Compiler, x: V_URI, y: V_URI):
        subst = c.bnode()
        c.q.triples()(
            (subst, CHEMINF.has_PubChem_normalized_counterpart, x),
            (subst, DCT.source, y),
            (y, DCT.subject, PubChem.CONCEPT.Chemical_Vendors))

    @M.register(
        wd.partition_coefficient_water_octanol(Item(x), Quantity(y)),
        {x: CheckCompound(),
         y: M.CheckLiteral(set_datatype=XSD.float)})
    def wd_partition_coefficient_water_octanol(
            self,
            c: Compiler,
            x: V_URI,
            y: VLiteral
    ):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type,
             CHEMINF.xlogp3_calculated_by_the_xlogp3_software),
            (attr, SIO.has_value, y))

    @M.register(
        wd.PubChem_CID(Item(x), ExternalId(y)),
        {x: CheckCompound(),
         y: CheckPubChemCID(set_language='en')})
    def wd_PubChem_CID(self, c: Compiler, x: V_URI, y: VLiteral):
        attr = c.bnode()
        c.q.triples()(
            (x, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID),
            (attr, SIO.has_value, y))

    @M.register(
        wd.stereoisomer_of(Item(x), Item(y)),
        {x: CheckCompound(),
         y: CheckCompound()})
    def wd_stereoisomer_of(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()(
            (x, CHEMINF.is_stereoisomer_of, y))

# -- Patent ----------------------------------------------------------------

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

    @M.register(                # TODO: wd.described_by_source
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
        {x: CheckPatent(),
         y: CheckPatentNumber()})
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
         y: M.CheckLiteral(set_language='en')})
    def wd_title(self, c: Compiler, x: V_URI, y: VLiteral):
        c.q.triples()((x, PATENT.titleOfInvention, y))

# -- Source ----------------------------------------------------------------

    @M.register(
        wd.instance_of(Item(x), wd.business),
        {x: CheckSource()})
    def wd_instance_of_manufacturer(self, c: Compiler, x: V_URI):
        c.q.triples()(
            (x, DCT.subject, PubChem.CONCEPT.Chemical_Vendors))
