# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

from ....context import Context
from ....model import (
    ExternalId,
    IRI,
    Item,
    Normal,
    Quantity,
    String,
    Text,
    Time,
    Variables,
)
from ....namespace import DCT, FOAF, RDF, RDFS, SKOS, Wikidata, XSD
from ....namespace.cito import CITO
from ....namespace.go import GO
from ....namespace.obo import IAO, OBO, RO
from ....namespace.patent import PATENT
from ....namespace.pubchem import PubChem
from ....namespace.semsci import CHEMINF, SIO
from ....namespace.vcard import VCARD
from ....typing import Final, TypeAlias
from ....vocabulary import pc_ as pc
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M
from .wikidata import WikidataMapping

if TYPE_CHECKING:  # pragma: no cover
    from .pubchem_options import PubChemMappingOptions

__all__ = (
    'PubChemMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral

#: Variables used in register patterns.
s, v = Variables('s', 'v')


class PubChemMapping(M):
    """PubChem SPARQL mapping.

    Parameters:
       normalize_casrn: Whether to normalize the returned CAS-RNs.
    """

# -- Checks ----------------------------------------------------------------

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
        r'^[A-Z][A-Z]-\w*(-[A-Z]+[1-9][0-9]*)?$')

    _re_patent_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(PubChem.PATENT)}'
        r'[A-Z][A-Z]-[A-Za-z0-9\-]+$')

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

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    #: PubChem SPARQL mapping options.
    _options: PubChemMappingOptions

    def __init__(
            self,
            normalize_casrn: bool | None = None,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()
        if normalize_casrn is not None:
            self.options.set_normalize_casrn(normalize_casrn)

    def _get_context_options(self) -> PubChemMappingOptions:
        return self.context.options.compiler.sparql.mapping.pubchem

    @property
    def options(self) -> PubChemMappingOptions:
        """The PubChem SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> PubChemMappingOptions:
        """Gets the PubChem SPARQL mapping options.

        Returns:
           PubChem SPARQL mapping options.
        """
        return self._options

# -- Pseudo-entries --------------------------------------------------------

    @M.register(
        list(map(lambda p: p(
            pc.isotope_atom_count,
            wd.Wikidata_property_related_to_chemistry), (
                wd.instance_of, wd.type))),
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_instance_of_pc_isotope_atom_count(self, c: C) -> None:
        pass

    @M.register(
        [wd.label(pc.isotope_atom_count, 'isotope atom count')],
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_label_pc_isotope_atom_count(self, c: C) -> None:
        pass

    @M.register(
        list(map(lambda p: p(
            pc.IUPAC_name,
            wd.Wikidata_property_related_to_chemistry), (
                wd.instance_of, wd.type))),
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_instance_of_pc_IUPAC_name(self, c: C) -> None:
        pass

    @M.register(
        [wd.label(pc.IUPAC_name, 'IUPAC name')],
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_label_pc_IUPAC_name(self, c: C) -> None:
        pass

# -- Compound --------------------------------------------------------------

    @M.register(
        [wd.label(Item(s), Text(v, 'en'))],
        {s: CheckCompound()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_compound(self, c: C, s: V_URI, v: VLiteral) -> None:
        chebi_ty = c.bnode()
        c.q.triples()(
            (s, RDF.type, chebi_ty),
            (chebi_ty, GO.inSubset, c.uri(str(OBO) + 'chebi#3_STAR')),
            (chebi_ty, RDFS.label, v))

    @M.register(
        [wd.alias(Item(s), Text(v, 'en'))],
        {s: CheckCompound()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_alias_compound(self, c: C, s: V_URI, v: VLiteral) -> None:
        chebi_ty = c.fresh_qvar()
        c.q.triples()((s, RDF.type, chebi_ty))
        with c.q.union():
            with c.q.group():
                c.q.triples()((chebi_ty, GO.hasExactSynonym, v))
            with c.q.group():
                c.q.triples()((chebi_ty, GO.hasRelatedSynonym, v))

    @M.register(
        [wd.description(Item(s), Text(v, 'en'))],
        {s: CheckCompound()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_description_compound(self, c: C, s: V_URI, v: VLiteral) -> None:
        chebi_ty = c.bnode()
        c.q.triples()(
            (s, RDF.type, chebi_ty),
            (chebi_ty, IAO.definition, v))

    @M.register(
        [wd.canonical_SMILES(Item(s), String(v))],
        {s: CheckCompound(),
         v: CheckCanonicalSMILES(set_language='en')},
        rank=Normal)
    def wd_canonical_SMILES(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.canonical_smiles_generated_by_OEChem),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.CAS_Registry_Number(Item(s), ExternalId(v))],
        {s: CheckCompound(),
         v: CheckCAS_RegistryNumber()},
        rank=Normal)
    def wd_CAS_Registry_Number(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, s),
            (attr, RDF.type, CHEMINF.CAS_registry_number),
            (attr, SIO.has_value, v))
        if isinstance(v, Var) and self.options.normalize_casrn:
            c.q.filter(~(c.q.strstarts(v, 'cas-')))

    @M.register(
        [wd.ChEBI_ID(Item(s), ExternalId(v))],
        {s: CheckCompound(),    # pre
         v: CheckChEBI_ID() >> M.CheckStr(replace_prefix=('', 'CHEBI:'))},
        {v: M.CheckLiteral(sub=(r'^(chebi|CHEBI):(\d+)$', r'\2'))},  # post
        rank=Normal)
    def wd_ChEBI_ID(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, s),
            (attr, RDF.type, CHEMINF.ChEBI_identifier),
            (attr, SIO.has_value, v))
        c.q.filter(c.q.strstarts(v, 'CHEBI:'))

    @M.register(
        [wd.ChEMBL_ID(Item(s), ExternalId(v))],
        {s: CheckCompound(),
         v: CheckChEMBL_ID()},
        rank=Normal)
    def wd_ChEMBL_ID(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, s),
            (attr, RDF.type, CHEMINF.ChEMBL_identifier),
            (attr, SIO.has_value, v))
        c.q.filter(c.q.strstarts(v, 'CHEMBL'))

    @M.register(
        [wd.chemical_formula(Item(s), String(v))],
        {s: CheckCompound(),    # pre
         v: M.CheckLiteral(tr={
             '₀': '0',
             '₁': '1',
             '₂': '2',
             '₃': '3',
             '₄': '4',
             '₅': '5',
             '₆': '6',
             '₇': '7',
             '₈': '8',
             '₉': '9',
         }, set_language='en')},
        {v: M.CheckLiteral(tr={  # post
            '0': '₀',
            '1': '₁',
            '2': '₂',
            '3': '₃',
            '4': '₄',
            '5': '₅',
            '6': '₆',
            '7': '₇',
            '8': '₈',
            '9': '₉',
        })},
        rank=Normal)
    def wd_chemical_formula(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type,
             CHEMINF.
             molecular_formula_calculated_by_the_pubchem_software_library),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.has_part(Item(s), Item(v))],
        {s: CheckCompound(),
         v: CheckCompound()},
        rank=Normal)
    def wd_has_part(self, c: C, s: V_URI, v: V_URI) -> None:
        c.q.triples()(
            (s, CHEMINF.has_component_with_uncharged_counterpart, v))

    @M.register(
        [wd.part_of(Item(s), Item(v))],
        {s: CheckCompound(),
         v: CheckCompound()},
        rank=Normal)
    def wd_part_of(self, c: C, s: V_URI, v: V_URI) -> None:
        self.wd_has_part(c, v, s)

    @M.register(
        [wd.InChI(Item(s), ExternalId(v))],
        {s: CheckCompound(),
         v: CheckInChI(set_language='en')},
        rank=Normal)
    def wd_InChI(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type,
             CHEMINF.InChI_calculated_by_library_version_1_0_4),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.InChIKey(Item(s), ExternalId(v))],
        {s: CheckCompound(),
         v: CheckInChIKey(set_language='en')},
        rank=Normal)
    def wd_InChIKey(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, s),
            (attr, RDF.type,
             CHEMINF.InChIKey_generated_by_software_version_1_0_4),
            (attr, SIO.has_value, v))

    @M.register(
        list(map(lambda p: p(Item(s), wd.type_of_a_chemical_entity), (
            wd.instance_of, wd.type))),
        {s: CheckCompound()},
        rank=Normal)
    def wd_instance_of_type_of_a_chemical_entity(
            self,
            c: C,
            s: V_URI
    ) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID))

    @M.register(
        [wd.isomeric_SMILES(Item(s), String(v))],
        {s: CheckCompound(),
         v: M.CheckLiteral(set_language='en')},
        rank=Normal)
    def wd_isomeric_SMILES(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.isomeric_SMILES_generated_by_OEChem),
            (attr, SIO.has_value, v))

    @M.register(
        [pc.isotope_atom_count(Item(s), Quantity(v))],
        {s: CheckCompound(),
         v: M.CheckInt()},
        rank=Normal)
    def pc_isotope_atom_count(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             isotope_atom_count_generated_by_pubchem_software_library),
            (attr, SIO.has_value, v))

    @M.register(
        [pc.IUPAC_name(Item(s), Text(v, 'en'))],
        {s: CheckCompound()},
        rank=Normal)
    def wd_IUPAC_name(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (attr, SIO.is_attribute_of, s),
            (attr, RDF.type, CHEMINF.IUPAC_Name_generated_by_LexiChem),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.legal_status_medicine(Item(s), wd.FDA_approved)],
        {s: CheckCompound()},
        rank=Normal)
    def wd_legal_status_medicine(self, c: C, s: V_URI) -> None:
        c.q.triples()(
            (s, RO.has_role, PubChem.VOCABULARY.FDAApprovedDrugs))

    @M.register(
        [wd.mass(Item(s), Quantity(v, wd.dalton))],
        {s: CheckCompound(),
         v: M.CheckLiteral(set_datatype=XSD.float)},
        rank=Normal)
    def wd_mass(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.
             exact_mass_calculated_by_pubchem_software_library),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.manufacturer(Item(s), Item(v)),
         wd.material_produced(Item(v), Item(s))],
        {s: CheckCompound(),
         v: CheckSource()},
        rank=Normal)
    def wd_manufacturer(self, c: C, s: V_URI, v: V_URI) -> None:
        subst = c.bnode()
        c.q.triples()(
            (subst, CHEMINF.has_PubChem_normalized_counterpart, s),
            (subst, DCT.source, v),
            (v, RDF.type, DCT._NS['Dataset']),
            (v, DCT.subject, PubChem.CONCEPT.Chemical_Vendors))

    @M.register(
        [wd.partition_coefficient_water_octanol(Item(s), Quantity(v))],
        {s: CheckCompound(),
         v: M.CheckLiteral(set_datatype=XSD.float)},
        rank=Normal)
    def wd_partition_coefficient_water_octanol(
            self,
            c: C,
            s: V_URI,
            v: VLiteral
    ) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type,
             CHEMINF.xlogp3_calculated_by_the_xlogp3_software),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.PubChem_CID(Item(s), ExternalId(v))],
        {s: CheckCompound(),
         v: CheckPubChemCID(set_language='en')},
        rank=Normal)
    def wd_PubChem_CID(self, c: C, s: V_URI, v: VLiteral) -> None:
        attr = c.bnode()
        c.q.triples()(
            (s, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID),
            (attr, SIO.has_value, v))

    @M.register(
        [wd.said_to_be_the_same_as(Item(s), Item(v))],
        {s: CheckCompound(),    # post
         v: M.CheckURI(
            startswith=Wikidata.WD,
            replace_prefix=(Wikidata.WD, 'https://www.wikidata.org/wiki/'))},
        {v: M.CheckURI(         # post
            startswith='https://www.wikidata.org/wiki/',
            replace_prefix=('https://www.wikidata.org/wiki/', Wikidata.WD))},
        rank=Normal)
    def wd_said_to_be_the_same_as(self, c: C, s: V_URI, v: V_URI) -> None:
        c.q.triples()(
            (s, SKOS.closeMatch, v))
        c.q.filter(
            c.q.strstarts(c.q.str(v), 'https://www.wikidata.org/wiki/'))

    @M.register(
        [wd.stereoisomer_of(Item(s), Item(v))],
        {s: CheckCompound(),
         v: CheckCompound()},
        rank=Normal)
    def wd_stereoisomer_of(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, CHEMINF.is_stereoisomer_of, v))

# -- Patent ----------------------------------------------------------------

    @M.register(
        [wd.description(Item(s), Text(v, 'en'))],
        {s: CheckPatent()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_description_patent(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, RDF.type, PATENT.Publication),
            (s, DCT.abstract, v))

    @M.register(
        [wd.author_name_string(Item(s), String(v))],
        {s: CheckPatent()},
        rank=Normal)
    def wd_author_name_string(self, c: C, s: V_URI, v: VLiteral) -> None:
        vcard = c.bnode()
        c.q.triples()(
            (s, RDF.type, PATENT.Publication),
            (s, PATENT.inventorVC, vcard),
            (vcard, VCARD.fn, v))

    @M.register(
        list(map(lambda p: p(Item(s), wd.patent), (wd.instance_of, wd.type))),
        {s: CheckPatent()},
        rank=Normal)
    def wd_instance_of_patent(self, c: C, s: V_URI) -> None:
        c.q.triples()((s, RDF.type, PATENT.Publication))

    @M.register(
        [wd.main_subject(Item(s), Item(v)),
         wd.described_by_source(Item(v), Item(s))],
        {s: CheckPatent(),
         v: CheckCompound()},
        rank=Normal)
    def wd_main_subject(self, c: C, s: V_URI, v: V_URI) -> None:
        attr = c.bnode()
        c.q.triples()(
            (v, CITO.isDiscussedBy, s),
            (s, RDF.type, PATENT.Publication),
            (v, SIO.has_attribute, attr),
            (attr, RDF.type, CHEMINF.PubChem_compound_identifier_CID))

    @M.register(
        [wd.patent_number(Item(s), ExternalId(v))],
        {s: CheckPatent(),
         v: CheckPatentNumber()},
        rank=Normal)
    def wd_patent_number(self, c: C, s: V_URI, v: V_URI) -> None:
        c.q.triples()(
            (s, RDF.type, PATENT.Publication),
            (s, PATENT.publicationNumber, v))

    @M.register(
        [wd.publication_date(
            Item(s), Time(v, Time.DAY, 0, wd.proleptic_Gregorian_calendar))],
        {s: CheckPatent()},
        rank=Normal)
    def wd_publication_date(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, RDF.type, PATENT.Publication),
            (s, PATENT.publicationDate, v))

    @M.register(
        [wd.title(Item(s), Text(v, 'en')),
         wd.label(Item(s), Text(v, 'en'))],
        {s: CheckPatent(),
         v: M.CheckLiteral()},
        rank=Normal)
    def wd_title(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, RDF.type, PATENT.Publication),
            (s, PATENT.titleOfInvention, v))

# -- Source ----------------------------------------------------------------

    @M.register(
        [wd.label(Item(s), Text(v, 'en'))],
        {s: CheckSource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_source(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, RDF.type, DCT._NS['Dataset']),
            (s, DCT.title, v))

    @M.register(
        [wd.alias(Item(s), Text(v, 'en'))],
        {s: CheckSource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_alias_source(self, c: C, s: V_URI, v: VLiteral) -> None:
        c.q.triples()(
            (s, RDF.type, DCT._NS['Dataset']),
            (s, DCT.alternative, v))

    @M.register(
        list(map(lambda p: p(Item(s), wd.vendor), (wd.instance_of, wd.type))),
        {s: CheckSource()},
        rank=Normal)
    def wd_instance_of_vendor(self, c: C, s: V_URI) -> None:
        c.q.triples()(
            (s, RDF.type, DCT._NS['Dataset']),
            (s, DCT.subject, PubChem.CONCEPT.Chemical_Vendors))

    @M.register(
        [wd.official_website(Item(s), IRI(v))],
        {s: CheckSource(),
         v: WikidataMapping.CheckIRI()},
        rank=Normal)
    def wd_official_website(self, c: C, s: V_URI, v: V_URI) -> None:
        c.q.triples()(
            (s, RDF.type, DCT._NS['Dataset']),
            (s, FOAF.homepage, v))
