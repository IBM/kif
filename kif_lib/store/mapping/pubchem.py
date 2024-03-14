# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from rdflib import Literal
from rdflib.namespace import Namespace

from ...itertools import batched
from ...model import (
    Datatype,
    FilterPattern,
    IRI,
    Item,
    Property,
    Quantity,
    Statement,
    String,
    T_IRI,
    Text,
    Time,
    Value,
)
from ...namespace import DCT, RDF, WD, XSD
from ...typing import Any, cast, Iterable, Iterator, override, TypeAlias
from ...vocabulary import wd
from ..abc import Store
from ..sparql_mapping import SPARQL_Mapping

CITO = Namespace('http://purl.org/spar/cito/')
OBO = Namespace('http://purl.obolibrary.org/obo/')
PATENT = Namespace('http://data.epo.org/linked-data/def/patent/')
PUBCHEM = Namespace('http://rdf.ncbi.nlm.nih.gov/pubchem/')
PUBCHEM_COMPOUND = Namespace(str(PUBCHEM) + 'compound/')
PUBCHEM_CONCEPT = Namespace(str(PUBCHEM) + 'concept/')
PUBCHEM_PATENT = Namespace(str(PUBCHEM) + 'patent/')
PUBCHEM_SOURCE = Namespace(str(PUBCHEM) + 'source/')
SEMSCI = Namespace('http://semanticscience.org/resource/')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')


class IAO:
    # See <https://www.ebi.ac.uk/ols4/>.
    definition = OBO.IAO_0000115


class CHEMINF:
    # See <https://www.ebi.ac.uk/ols4/>.
    canonical_smiles_generated_by_OEChem = SEMSCI.CHEMINF_000376
    CAS_registry_number = SEMSCI.CHEMINF_000446
    ChEBI_identifier = SEMSCI.CHEMINF_000407
    ChEMBL_identifier = SEMSCI.CHEMINF_000412
    drug_trade_name = SEMSCI.CHEMINF_000561
    exact_mass_calculated_by_pubchem_software_library = SEMSCI.CHEMINF_000338
    has_component = SEMSCI.CHEMINF_000478
    has_component_with_uncharged_counterpart = SEMSCI.CHEMINF_000480
    has_PubChem_normalized_counterpart = SEMSCI.CHEMINF_000477
    InChI_calculated_by_library_version_1_0_4 = SEMSCI.CHEMINF_000396
    InChIKey_generated_by_software_version_1_0_4 = SEMSCI.CHEMINF_000399
    IUPAC_Name_generated_by_LexiChem = SEMSCI.CHEMINF_000382
    is_stereoisomer_of = SEMSCI.CHEMINF_000461
    isomeric_SMILES_generated_by_OEChem = SEMSCI.CHEMINF_000379
    molecular_formula_calculated_by_the_pubchem_software_library =\
        SEMSCI.CHEMINF_000335
    molecular_weight_calculated_by_the_pubchem_software_library =\
        SEMSCI.CHEMINF_000334
    PubChem_compound_identifier_CID = SEMSCI.CHEMINF_000140
    pubchem_depositor_supplied_molecular_entity_name = SEMSCI.CHEMINF_000339
    similar_to_by_PubChem_2D_similarity_algorithm = SEMSCI.CHEMINF_000482
    structure_complexity_calculated_by_cactvs = SEMSCI.CHEMINF_000390


class SIO:
    has_attribute = SEMSCI.SIO_000008
    has_value = SEMSCI.SIO_000300
    is_attribute_of = SEMSCI.SIO_000011


class PubChemMapping(SPARQL_Mapping):
    """PubChem SPARQL mapping."""

    class Spec(SPARQL_Mapping.Spec):
        """Mapping spec. of the PubChem SPARQL mapping."""

        @classmethod
        def check_canonical_SMILES(cls, v: Value) -> str:
            """Checks whether `v` is a canonical SMILES.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not a canonical SMILES.
            """
            return cls.check_string(v).value

        @classmethod
        def check_chemical_formula(cls, v: Value) -> str:
            """Checks whether `v` is a chemical formula.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not a chemical formula.
            """
            return cls.check_string(v).value

        @classmethod
        def check_InChI(cls, v: Value) -> str:
            """Checks whether `v` is an InChI.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an InChI.
            """
            return cls._check(
                cls.check_string(v).value,
                lambda s: s.startswith('InChI='))

        @classmethod
        def check_InChIKey(cls, v: Value) -> str:
            """Checks whether `v` is an InChIKey.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an InChIKey.
            """
            return cls.check_string(v).value

        @classmethod
        def check_isomeric_SMILES(cls, v: Value) -> str:
            """Checks whether `v` is an isomeric SMILES.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an isomeric SMILES.
            """
            return cls.check_canonical_SMILES(v)

        @classmethod
        def check_PubChem_CID(
                cls,
                v: Value,
                _re=re.compile('^[0-9]+$')
        ) -> str:
            """Checks whether `v` is a PubChem CID.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not a PubChem CID.
            """
            return cls._check(cls.check_string(v).value, _re.match)

# == Pre/post filter hooks =================================================

    _toxicity_properties = {
        'LD50': wd.median_lethal_dose,
        'LDLo': wd.minimal_lethal_dose,
    }

    _toxicity_properties_inv = {v: k for k, v in _toxicity_properties.items()}

    @override
    @classmethod
    def filter_pre_hook(
            cls,
            store: Store,
            pattern: FilterPattern,
            limit: int,
    ) -> tuple[FilterPattern, int, Any]:
        if (pattern.property is None
                or pattern.property.property
                not in cls._toxicity_properties_inv):
            return pattern, limit, None
        else:
            new_pattern = FilterPattern(
                pattern.subject,
                wd.instance_of,
                wd.type_of_a_chemical_entity,
                pattern.snak_mask)
            return new_pattern, store.maximum_page_size, dict(
                original_pattern=pattern,
                original_limit=limit)

    @override
    @classmethod
    def filter_post_hook(
            cls,
            store: Store,
            pattern: FilterPattern,
            limit: int,
            data: Any,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        if data is None:
            return it           # nothing to do
        else:
            def mk_it():
                assert isinstance(data, dict)
                original_pattern = data['original_pattern']
                assert isinstance(original_pattern, FilterPattern)
                original_limit = data['original_limit']
                assert isinstance(original_limit, int)
                count = 0
                cids_it = map(
                    lambda iri: iri.value[len(cls.COMPOUND.value) + 3:],
                    filter(cls.is_pubchem_compound_iri, map(
                        lambda stmt: stmt.subject.iri, it)))
                for batch in batched(cids_it, store.default_page_size):
                    for stmt in cls._get_toxicity(set(batch)):
                        if original_pattern.match(stmt):
                            yield stmt
                            count += 1
                        if count > original_limit:
                            break
                    if count > original_limit:
                        break
            return mk_it()

    @classmethod
    def _get_toxicity(cls, cids: Iterable[str]) -> Iterator[Statement]:
        import json

        import requests
        ors = list(map(lambda cid: dict(cid=cid), cids))
        if not ors:
            return iter(())
        res = requests.get(
            'https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi',
            params=dict(
                infmt='json',
                outfmt='json',
                query=json.dumps({
                    'download': '*',
                    'collection': 'chemidplus',
                    'start': 1,
                    'limit': 10000000,
                    'where': {'ors': ors},
                })))
        res.raise_for_status()
        return cls._parse_toxicity(res.json())

    @classmethod
    def _parse_toxicity(
            cls,
            response: Iterable[dict[str, Any]]
    ) -> Iterator[Statement]:
        for entry in response:
            # print(entry)
            try:
                subject = cls._parse_toxicity_cid(entry['cid'])
                property = cls._parse_toxicity_testtype(entry['testtype'])
                value = cls._parse_toxicity_dose(entry['dose'])
                yield property(subject, value)
            except (KeyError, ValueError):
                continue        # skip

    @classmethod
    def _parse_toxicity_cid(cls, cid: str) -> Item:
        return cls.compound(f'CID{int(cid)}')

    @classmethod
    def _parse_toxicity_testtype(cls, testtype: str) -> Property:
        return cls._toxicity_properties[testtype]

    @classmethod
    def _parse_toxicity_dose(
            cls,
            dose: str,
            _re=re.compile(r'^(\d+\.?\d*)\s*(.*)$')
    ) -> Quantity:
        m = _re.match(dose)
        if m is None:
            raise ValueError
        amount, unit_str = m.groups()
        if unit_str == 'mg/kg':
            unit = wd.milligram_per_kilogram
        else:
            unit = None
        return Quantity(amount, unit)


# == IRI prefix mappings ===================================================

    #: The IRI prefix of compounds.
    COMPOUND = IRI(WD.Q_PUBCHEM_COMPOUND_)

    #: The IRI prefix of patents.
    PATENT = IRI(WD.Q_PUBCHEM_PATENT_)

    #: The IRI prefix of sources.
    SOURCE = IRI(WD.Q_PUBCHEM_SOURCE_)

    @classmethod
    def compound(cls, id: str) -> Item:
        """Makes an item from compound id.

        Parameters:
           id: Compound id.

        Returns:
           The resulting item.
        """
        return Item(cls.COMPOUND.value + id)

    @classmethod
    def patent(cls, id: str) -> Item:
        """Makes an item from patent id.

        Parameters:
           id: Patent id.

        Returns:
           The resulting item.
        """
        return Item(cls.PATENT.value + id)

    @classmethod
    def source(cls, id: str) -> Item:
        """Makes an item from source id.

        Parameters:
           id: Source id.

        Returns:
           The resulting item.
        """
        return Item(cls.SOURCE.value + id)

    @classmethod
    def is_pubchem_compound_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem compound.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI._check_arg_iri(iri, cls.is_pubchem_compound_iri, 'iri', 1)
        return iri.value.startswith(cls.COMPOUND.value)

    @classmethod
    def is_pubchem_patent_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem patent.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI._check_arg_iri(iri, cls.is_pubchem_patent_iri, 'iri', 1)
        return iri.value.startswith(cls.PATENT.value)

    @classmethod
    def is_pubchem_source_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem source.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI._check_arg_iri(iri, cls.is_pubchem_source_iri, 'iri', 1)
        return iri.value.startswith(cls.SOURCE.value)


PubChemMapping.register_iri_prefix_replacement(
    PUBCHEM_COMPOUND, PubChemMapping.COMPOUND)

PubChemMapping.register_iri_prefix_replacement(
    PUBCHEM_PATENT, PubChemMapping.PATENT)

PubChemMapping.register_iri_prefix_replacement(
    PUBCHEM_SOURCE, PubChemMapping.SOURCE)


# == Property mappings =====================================================

Builder: TypeAlias = PubChemMapping.Builder
Spec: TypeAlias = PubChemMapping.Spec
TTrm: TypeAlias = PubChemMapping.Builder.TTrm


# -- Compound --------------------------------------------------------------

@PubChemMapping.register_label(
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_COMPOUND_label(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, SIO.has_value, v),
        (attr, RDF.type, CHEMINF.IUPAC_Name_generated_by_LexiChem))


@PubChemMapping.register_alias(
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_COMPOUND_alias(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, SIO.has_value, v),
        (attr, RDF.type, CHEMINF.
         pubchem_depositor_supplied_molecular_entity_name))


@PubChemMapping.register_description(
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_COMPOUND_description(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    chebi_class = q.bnode()
    q.triples(
        (s, RDF.type, chebi_class),
        (chebi_class, IAO.definition, v))


@PubChemMapping.register(
    property=wd.canonical_SMILES,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.COMPOUND)
def wd_canonical_SMILES(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Canonical SMILES values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_canonical_SMILES(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.canonical_smiles_generated_by_OEChem),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.chemical_formula,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.COMPOUND)
def wd_chemical_formula(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Chemical formula values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_chemical_formula(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.
             molecular_formula_calculated_by_the_pubchem_software_library),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.CAS_Registry_Number,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_CAS_Registry_Number(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.CAS_registry_number),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.ChEBI_ID,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_ChEBI_ID(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.ChEBI_identifier),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.ChEMBL_ID,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_ChEMBL_ID(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.ChEMBL_identifier),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.described_by_source,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.PATENT)
def wd_described_by_source(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CHEMINF.has_PubChem_normalized_counterpart, s),
        (substance, CITO.isDiscussedBy, v),
        (v, RDF.type, PATENT.Publication))


@PubChemMapping.register(
    property=wd.has_part,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.COMPOUND)
def wd_has_part(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, CHEMINF.has_component_with_uncharged_counterpart, v)


@PubChemMapping.register(
    property=wd.InChI,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_InChI(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: InChI values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_InChI(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.InChI_calculated_by_library_version_1_0_4),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.InChIKey,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_InChIKey(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: InChIKey values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_InChIKey(cast(Value, v)), 'en')
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.
         InChIKey_generated_by_software_version_1_0_4),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.instance_of,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value=wd.type_of_a_chemical_entity)
def wd_COMPOUND_instance_of(
        spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    attr = q.bnode()
    q.triples(
        (s, SIO.has_attribute, attr),
        (attr, RDF.type, CHEMINF.structure_complexity_calculated_by_cactvs))


@PubChemMapping.register(
    property=wd.isomeric_SMILES,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.COMPOUND)
def wd_isomeric_SMILES(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Isomeric SMILES values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_isomeric_SMILES(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.isomeric_SMILES_generated_by_OEChem),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.mass,
    datatype=Datatype.quantity,
    subject_prefix=PubChemMapping.COMPOUND,
    value_datatype=XSD.decimal,
    value_datatype_encoded=XSD.float,
    value_unit=wd.gram_per_mole)
def wd_mass(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Mass values in PubChem have datatype float.
        ###
        qt = spec.check_quantity(cast(Value, v))
        v = Literal(qt.value, datatype=XSD.float)
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.
             molecular_weight_calculated_by_the_pubchem_software_library),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.manufacturer,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.SOURCE)
def wd_manufacturer(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CHEMINF.has_PubChem_normalized_counterpart, s),
        (substance, DCT.source, v),
        (v, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors))


@PubChemMapping.register(
    property=wd.PubChem_CID,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.COMPOUND)
def wd_PubChem_CID(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: CID values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_PubChem_CID(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.PubChem_compound_identifier_CID),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.stereoisomer_of,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.COMPOUND)
def wd_stereoisomer_of(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, CHEMINF.is_stereoisomer_of, v)


@PubChemMapping.register(
    property=wd.trading_name,
    datatype=Datatype.text,
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_trading_name(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Trading name values in PubChem have no language tag.
        ###
        v = String(spec.check_text(cast(Value, v)).value)
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.drug_trade_name),
        (attr, SIO.has_value, v))


# -- Patent ----------------------------------------------------------------

@PubChemMapping.register_label(
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_PATENT_label(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, PATENT.titleOfInvention, v)


@PubChemMapping.register_description(
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_PATENT_description(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, DCT.abstract, v)


@PubChemMapping.register(
    property=wd.author_name_string,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.PATENT)
def wd_author_name_string(
        spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    with q.sp(s, PATENT.inventorVC) as sp:
        sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    property=wd.instance_of,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.PATENT,
    value=wd.patent)
def wd_PATENT_instance_of(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, RDF.type, PATENT.Publication)


@PubChemMapping.register(
    property=wd.main_subject,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.PATENT,
    value_prefix=PubChemMapping.COMPOUND)
def wd_main_subject(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CITO.isDiscussedBy, s),
        (s, RDF.type, PATENT.Publication),
        (substance, CHEMINF.has_PubChem_normalized_counterpart, v))


@PubChemMapping.register(
    property=wd.patent_number,
    datatype=Datatype.string,   # FIXME: ExternalId
    subject_prefix=PubChemMapping.PATENT)
def wd_patent_number(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, PATENT.publicationNumber, v)


@PubChemMapping.register(
    property=wd.publication_date,
    datatype=Datatype.time,
    subject_prefix=PubChemMapping.PATENT,
    value_precision=Time.DAY,
    value_timezone=0,
    value_calendar=wd.proleptic_Gregorian_calendar)
def wd_publication_date(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, PATENT.publicationDate, v)


@PubChemMapping.register(
    property=wd.sponsor,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.PATENT)
def wd_sponsor(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    with q.sp(s, PATENT.applicantVC) as sp:
        sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    property=wd.title,
    datatype=Datatype.text,
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_title(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: Title values in PubChem have no language tag.
        ###
        v = String(spec.check_text(cast(Value, v)).value)
    q.triple(s, PATENT.titleOfInvention, v)


# -- Source ----------------------------------------------------------------

@PubChemMapping.register_label(
    subject_prefix=PubChemMapping.SOURCE,
    value_language='en')
def wd_SOURCE_label(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, DCT.title, v)


@PubChemMapping.register_alias(
    subject_prefix=PubChemMapping.SOURCE,
    value_language='en')
def wd_SOURCE_alias(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, DCT.alternative, v)


@PubChemMapping.register(
    property=wd.instance_of,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.SOURCE,
    value=wd.business)
def wd_SOURCE_instance_of(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors)
