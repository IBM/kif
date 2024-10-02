# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from ... import itertools
from ...model import (
    AnnotationRecord,
    AnnotationRecordSet,
    ExternalIdDatatype,
    Filter,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    KIF_Object,
    Property,
    Quantity,
    QuantityDatatype,
    ReferenceRecord,
    Statement,
    String,
    StringDatatype,
    T_IRI,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
    Value,
    ValueSnak,
)
from ...namespace import DCT, FOAF, RDF, WD, WDS, XSD
from ...rdflib import Literal, Namespace
from ...typing import Any, cast, Iterable, Iterator, override, TypeAlias
from ...vocabulary import wd
from ..abc import Store
from ..sparql_mapping import SPARQL_Mapping

filter_ = filter

CITO = Namespace('http://purl.org/spar/cito/')
OBO = Namespace('http://purl.obolibrary.org/obo/')
PATENT = Namespace('http://data.epo.org/linked-data/def/patent/')
PUBCHEM = Namespace('http://rdf.ncbi.nlm.nih.gov/pubchem/')
PUBCHEM_COMPOUND = Namespace(str(PUBCHEM) + 'compound/')
PUBCHEM_CONCEPT = Namespace(str(PUBCHEM) + 'concept/')
PUBCHEM_PATENT = Namespace(str(PUBCHEM) + 'patent/')
PUBCHEM_SOURCE = Namespace(str(PUBCHEM) + 'source/')
PUBCHEM_VOCABULARY = Namespace(str(PUBCHEM) + 'vocabulary#')
SEMSCI = Namespace('http://semanticscience.org/resource/')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')


class IAO:
    """The OBO IAO namespace.

    See <https://www.ebi.ac.uk/ols4/>.
    """
    definition = OBO.IAO_0000115


class RO:
    """The OBO RO namespace.

    See <https://www.ebi.ac.uk/ols4/>.
    """
    has_role = OBO.RO_0000087


class CHEMINF:
    """The CHEMINF namespace.

    See <https://www.ebi.ac.uk/ols4/>.
    See <http://doi.org/10.1186/s13321-015-0084-4>.
    """
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
    xlogp3_calculated_by_the_xlogp3_software = SEMSCI.CHEMINF_000395


class SIO:
    """The SEMSCI SIO namespace."""
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
            return cls.check_string(v).content

        @classmethod
        def check_chemical_formula(cls, v: Value) -> str:
            """Checks whether `v` is a chemical formula.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not a chemical formula.
            """
            return cls.check_string(v).content

        @classmethod
        def check_InChI(cls, v: Value) -> str:
            """Checks whether `v` is an InChI.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an InChI.
            """
            return cls._check(
                cls.check_string(v).content,
                lambda s: s.startswith('InChI='))

        @classmethod
        def check_InChIKey(cls, v: Value) -> str:
            """Checks whether `v` is an InChIKey.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an InChIKey.
            """
            return cls.check_string(v).content

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
            return cls._check(
                cls.check_string(v).content, lambda x: bool(_re.match(x)))

# == Hooks =================================================================

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
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> tuple[Filter, int, bool, Any]:
        from ..sparql import SPARQL_Store
        assert isinstance(store, SPARQL_Store)
        if filter.value.is_empty():
            return filter, limit, distinct, None
        subject, property, value, snak_mask = filter._unpack_legacy()
        if (property is None
                or property
                not in cls._toxicity_properties_inv):
            return filter, limit, distinct, None
        else:
            new_filter = Filter(
                subject,
                wd.instance_of,
                wd.type_of_a_chemical_entity,
                snak_mask)
            return new_filter, store.max_page_size, distinct, dict(
                original_filter=filter,
                original_limit=limit)

    @classmethod
    @override
    def filter_post_hook(
            cls,
            store: Store,
            filter: Filter,
            limit: int,
            distinct: bool,
            data: Any,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        if data is None:
            return it           # nothing to do
        else:
            def mk_it() -> Iterator[Statement]:
                assert isinstance(data, dict)
                original_filter = data['original_filter']
                assert isinstance(original_filter, Filter)
                original_limit = data['original_limit']
                assert isinstance(original_limit, int)
                count = 0
                cids_it = map(
                    lambda iri: iri.content[len(cls.COMPOUND.content) + 3:],
                    filter_(cls.is_pubchem_compound_iri, map(
                        lambda stmt: stmt.subject.iri, it)))
                for batch in itertools.batched(
                        cids_it, store.default_page_size):
                    for stmt, annots in cls._get_toxicity(set(batch)):
                        if original_filter.match(stmt):
                            from ..sparql import SPARQL_Store
                            st = cast(SPARQL_Store, store)
                            st._cache_add_wds(stmt, WDS[stmt.digest])
                            st._cache.set(stmt, 'annotations', annots)
                            yield stmt
                            count += 1
                        if count >= original_limit:
                            break
                    if count >= original_limit:
                        break
            return mk_it()

    @classmethod
    def _get_toxicity(
            cls,
            cids: Iterable[str]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        import json

        import httpx
        ors = list(map(lambda cid: dict(cid=cid), cids))
        if not ors:
            return iter(())
        res = httpx.get(
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
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        for entry in response:
            assert isinstance(entry, dict)
            try:
                subject = cls._parse_toxicity_cid(entry['cid'])
                property = cls._parse_toxicity_testtype(entry['testtype'])
                value = cls._parse_toxicity_dose(entry['dose'])
                stmt = cast(Statement, property(subject, value))
                annots = cls._parse_toxicity_annotations(entry)
                yield stmt, annots
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
            _re=re.compile(r'^(\d+\.?\d*)\s*(\S*)$'),
            _unit={
                'mg/kg': wd.milligram_per_kilogram,
                'ug/kg': wd.microgram_per_kilogram,
                'gm/kg': wd.gram_per_kilogram,
            }
    ) -> Quantity:
        m = _re.match(dose)
        if m is None:
            raise ValueError
        amount, unit_key = m.groups()
        return Quantity(amount, _unit[unit_key])

    @classmethod
    def _parse_toxicity_annotations(
            cls,
            entry: dict[str, Any],
            _organism={
                'child': wd.child,
                'dog': wd.dog,
                'frog': wd.frog,
                'guinea pig': wd.Guinea_pig,
                'human': wd.human,
                'infant': wd.infant,
                'mammal (species unspecified)': wd.mammal,
                'mammal': wd.mammal,
                'man': wd.man,
                'mouse': wd.laboratory_rat,
                'rabbit': wd.rabbit,
                'rat': wd.laboratory_rat,
                'woman': wd.woman,
            },
            _route={
                'intraperitoneal': wd.intraperitoneal_injection,
                'intravenous': wd.intravenous_injection,
                'oral': wd.oral_administration,
                'rectal': wd.rectal_administration,
                'skin': wd.skin_absorption,
                'subcutaneous': wd.subcutaneous_injection,
            }
    ) -> AnnotationRecordSet:
        try:
            quals = []
            if 'effect' in entry:
                quals.append(wd.has_effect(Text(entry['effect'])))
            if 'organism' in entry:
                organism_key = entry['organism']
                quals.append(wd.applies_to_taxon(_organism.get(
                    organism_key, organism_key)))
            if 'route' in entry:
                route_key = entry['route']
                if route_key != 'unreported':
                    quals.append(wd.route_of_administration(_route.get(
                        route_key, route_key)))
            ref = []
            if 'reference' in entry:
                ref.append(wd.stated_in(Text(entry['reference'])))
            return AnnotationRecordSet(
                AnnotationRecord(
                    quals,
                    ReferenceRecord(*ref)))
        except (KeyError, ValueError):
            return AnnotationRecordSet(AnnotationRecord())  # skip

    @classmethod
    def get_annotations_post_hook(
            cls,
            store: Store,
            stmts: Iterable[Statement],
            data: Any,
            it: Iterator[tuple[Statement, AnnotationRecordSet | None]]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        for stmt, annots in it:
            if stmt.snak.property in cls._toxicity_properties_inv:
                saved_annots = store._cache.get(stmt, 'annotations')
                if saved_annots is not None:
                    assert isinstance(saved_annots, AnnotationRecordSet)
                    annots = saved_annots
            yield stmt, annots

# == IRI prefix mappings ===================================================

    #: The IRI prefix of compounds.
    COMPOUND = IRI(WD.Q_PUBCHEM_COMPOUND_)

    #: The IRI prefix of patents.
    PATENT = IRI(WD.Q_PUBCHEM_PATENT_)

    #: The IRI prefix of sources.
    SOURCE = IRI(WD.Q_PUBCHEM_SOURCE_)

    @classmethod
    def compound(cls, id: int | str) -> Item:
        """Makes an item from compound id.

        Parameters:
           id: Compound id.

        Returns:
           The resulting item.
        """
        KIF_Object._check_arg_isinstance(
            id, (int, str), cls.compound, 'id', 1)
        if isinstance(id, int):
            id = f'CID{id}'
        elif isinstance(id, str):
            try:
                id = f'CID{int(id)}'
            except ValueError:
                pass
        return Item(cls.COMPOUND.content + id)

    @classmethod
    def patent(cls, id: str) -> Item:
        """Makes an item from patent id.

        Parameters:
           id: Patent id.

        Returns:
           The resulting item.
        """
        return Item(cls.PATENT.content + id)

    @classmethod
    def source(cls, id: str) -> Item:
        """Makes an item from source id.

        Parameters:
           id: Source id.

        Returns:
           The resulting item.
        """
        return Item(cls.SOURCE.content + id)

    @classmethod
    def is_pubchem_compound_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem compound.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI.check(iri, cls.is_pubchem_compound_iri, 'iri', 1)
        return iri.content.startswith(cls.COMPOUND.content)

    @classmethod
    def is_pubchem_patent_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem patent.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI.check(iri, cls.is_pubchem_patent_iri, 'iri', 1)
        return iri.content.startswith(cls.PATENT.content)

    @classmethod
    def is_pubchem_source_iri(cls, iri: T_IRI) -> bool:
        """Tests whether IRI prefix matches that of a PubChem source.

        Parameters:
           iri: IRI.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        iri = IRI.check(iri, cls.is_pubchem_source_iri, 'iri', 1)
        return iri.content.startswith(cls.SOURCE.content)


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
def wd_COMPOUND_label(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, SIO.has_value, v),
        (attr, RDF.type, CHEMINF.IUPAC_Name_generated_by_LexiChem))


@PubChemMapping.register_alias(
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_COMPOUND_alias(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, SIO.has_value, v),
        (attr, RDF.type, CHEMINF.
         pubchem_depositor_supplied_molecular_entity_name))


@PubChemMapping.register_description(
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_COMPOUND_description(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    chebi_class = q.bnode()
    q.triples(
        (s, RDF.type, chebi_class),
        (chebi_class, IAO.definition, v))


@PubChemMapping.register(
    property=wd.canonical_SMILES,
    datatype=StringDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_canonical_SMILES(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
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
    datatype=StringDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_chemical_formula(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
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
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_CAS_Registry_Number(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.CAS_registry_number),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.ChEBI_ID,
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_ChEBI_ID(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.ChEBI_identifier),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.ChEMBL_ID,
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_ChEMBL_ID(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.ChEMBL_identifier),
        (attr, SIO.has_value, v))


@PubChemMapping.register(
    property=wd.described_by_source,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.PATENT)
def wd_described_by_source(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    substance = q.bnode()
    q.triples(
        (substance, CHEMINF.has_PubChem_normalized_counterpart, s),
        (substance, CITO.isDiscussedBy, v),
        (v, RDF.type, PATENT.Publication))


@PubChemMapping.register(
    property=wd.has_part,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.COMPOUND)
def wd_has_part(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, CHEMINF.has_component_with_uncharged_counterpart, v)


@PubChemMapping.register(
    property=wd.InChI,
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_InChI(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
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
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_InChIKey(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
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
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value=wd.type_of_a_chemical_entity)
def wd_COMPOUND_instance_of(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    attr = q.bnode()
    q.triples(
        (s, SIO.has_attribute, attr),
        (attr, RDF.type, CHEMINF.structure_complexity_calculated_by_cactvs))


@PubChemMapping.register(
    property=wd.isomeric_SMILES,
    datatype=StringDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_isomeric_SMILES(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: Isomeric SMILES values in PubChem are tagged with @en.
        ###
        v = Text(spec.check_isomeric_SMILES(cast(Value, v)), 'en')
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.isomeric_SMILES_generated_by_OEChem),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.legal_status_medicine,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value=wd.FDA_approved)
def wd_legal_status_medicine(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, RO.has_role, PUBCHEM_VOCABULARY.FDAApprovedDrugs)


@PubChemMapping.register(
    property=wd.mass,
    datatype=QuantityDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_datatype=XSD.decimal,
    value_datatype_encoded=XSD.float,
    value_unit=wd.gram_per_mole)
def wd_mass(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: Mass values in PubChem have datatype float.
        ###
        qt = spec.check_quantity(cast(Value, v))
        v = Literal(str(qt.amount), datatype=XSD.float)
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.
             molecular_weight_calculated_by_the_pubchem_software_library),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.manufacturer,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.SOURCE)
def wd_manufacturer(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    substance = q.bnode()
    q.triples(
        (substance, CHEMINF.has_PubChem_normalized_counterpart, s),
        (substance, DCT.source, v),
        (v, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors))


@PubChemMapping.register(
    property=wd.partition_coefficient_water_octanol,
    datatype=QuantityDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_datatype=XSD.decimal,
    value_datatype_encoded=XSD.float,
    annotations=[
        AnnotationRecord([ValueSnak(
            wd.based_on_heuristic, wd.machine_learning)])])
def wd_partition_coefficient_water_octanol(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: LogP values in PubChem have datatype float.
        ###
        qt = spec.check_quantity(cast(Value, v))
        v = Literal(str(qt.amount), datatype=XSD.float)
    with q.sp(s, SIO.has_attribute) as sp:
        sp.pairs(
            (RDF.type, CHEMINF.xlogp3_calculated_by_the_xlogp3_software),
            (SIO.has_value, v))


@PubChemMapping.register(
    property=wd.PubChem_CID,
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.COMPOUND)
def wd_PubChem_CID(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
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
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.COMPOUND)
def wd_stereoisomer_of(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, CHEMINF.is_stereoisomer_of, v)


@PubChemMapping.register(
    property=wd.trading_name,
    datatype=TextDatatype(),
    subject_prefix=PubChemMapping.COMPOUND,
    value_language='en')
def wd_trading_name(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: Trading name values in PubChem have no language tag.
        ###
        v = String(spec.check_text(cast(Value, v)).content)
    attr = q.bnode()
    q.triples(
        (attr, SIO.is_attribute_of, s),
        (attr, RDF.type, CHEMINF.drug_trade_name),
        (attr, SIO.has_value, v))


# -- Patent ----------------------------------------------------------------

@PubChemMapping.register_label(
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_PATENT_label(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, PATENT.titleOfInvention, v)


@PubChemMapping.register_description(
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_PATENT_description(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, DCT.abstract, v)


@PubChemMapping.register(
    property=wd.author_name_string,
    datatype=StringDatatype(),
    subject_prefix=PubChemMapping.PATENT)
def wd_author_name_string(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    with q.sp(s, PATENT.inventorVC) as sp:
        sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    property=wd.instance_of,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.PATENT,
    value=wd.patent)
def wd_PATENT_instance_of(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, RDF.type, PATENT.Publication)


@PubChemMapping.register(
    property=wd.main_subject,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.PATENT,
    value_prefix=PubChemMapping.COMPOUND)
def wd_main_subject(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    substance = q.bnode()
    q.triples(
        (substance, CITO.isDiscussedBy, s),
        (s, RDF.type, PATENT.Publication),
        (substance, CHEMINF.has_PubChem_normalized_counterpart, v))


@PubChemMapping.register(
    property=wd.patent_number,
    datatype=ExternalIdDatatype(),
    subject_prefix=PubChemMapping.PATENT)
def wd_patent_number(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, PATENT.publicationNumber, v)


@PubChemMapping.register(
    property=wd.publication_date,
    datatype=TimeDatatype(),
    subject_prefix=PubChemMapping.PATENT,
    value_precision=Time.DAY,
    value_timezone=0,
    value_calendar=wd.proleptic_Gregorian_calendar)
def wd_publication_date(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, PATENT.publicationDate, v)


# @PubChemMapping.register(
#     property=wd.sponsor,
#     datatype=StringDatatype(),
#     subject_prefix=PubChemMapping.PATENT)
# def wd_sponsor(
#         spec: Spec,
#         q: Builder,
#         s: TTrm,
#         p: TTrm,
#         v: TTrm
# ) -> None:
#     with q.sp(s, PATENT.applicantVC) as sp:
#         sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    property=wd.title,
    datatype=TextDatatype(),
    subject_prefix=PubChemMapping.PATENT,
    value_language='en')
def wd_title(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: Title values in PubChem have no language tag.
        ###
        v = String(spec.check_text(cast(Value, v)).content)
    q.triple(s, PATENT.titleOfInvention, v)


# -- Source ----------------------------------------------------------------

@PubChemMapping.register_label(
    subject_prefix=PubChemMapping.SOURCE,
    value_language='en')
def wd_SOURCE_label(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, DCT.title, v)


@PubChemMapping.register_alias(
    subject_prefix=PubChemMapping.SOURCE,
    value_language='en')
def wd_SOURCE_alias(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, DCT.alternative, v)


@PubChemMapping.register(
    property=wd.instance_of,
    datatype=ItemDatatype(),
    subject_prefix=PubChemMapping.SOURCE,
    value=wd.business)
def wd_SOURCE_instance_of(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triple(s, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors)


@PubChemMapping.register(
    property=wd.official_website,
    datatype=IRI_Datatype(),
    subject_prefix=PubChemMapping.SOURCE)
def wd_SOURCE_official_website(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    q.triples(
        (s, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors),
        (s, FOAF.homepage, v))


@PubChemMapping.register(
    property=wd.short_name,
    datatype=TextDatatype(),
    subject_prefix=PubChemMapping.SOURCE,
    value_language='en')
def wd_SOURCE_short_name(
        spec: Spec,
        q: Builder,
        s: TTrm,
        p: TTrm,
        v: TTrm
) -> None:
    if isinstance(v, Value):
        ###
        # IMPORTANT: Short-name values in PubChem have no language tag.
        ###
        v = String(spec.check_text(cast(Value, v)).content)
    q.triples(
        (s, DCT.subject, PUBCHEM_CONCEPT.Chemical_Vendors),
        (s, DCT.alternative, v))
