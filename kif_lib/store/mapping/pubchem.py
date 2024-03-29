# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0


from rdflib.namespace import Namespace

from ...model import Datatype, String, Text, Time, Value
from ...namespace import RDF, WD, XSD
from ...typing import cast, TypeAlias
from ...vocabulary import wd
from ..sparql_mapping import SPARQL_Mapping

CITO = Namespace('http://purl.org/spar/cito/')
PATENT = Namespace('http://data.epo.org/linked-data/def/patent/')
PUBCHEM = Namespace('http://rdf.ncbi.nlm.nih.gov/pubchem/')
PUBCHEM_COMPOUND = Namespace(str(PUBCHEM) + 'compound/')
PUBCHEM_DESCRIPTOR = Namespace(str(PUBCHEM) + 'descriptor/')
PUBCHEM_PATENT = Namespace(str(PUBCHEM) + 'patent/')
SEMSCI = Namespace('http://semanticscience.org/resource/')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')


class PubChemMapping(SPARQL_Mapping):
    """PubChem SPARQL mapping."""

    class Spec(SPARQL_Mapping.Spec):
        """Mapping specification in the PubChem SPARQL mapping."""

        @classmethod
        def check_InChI(cls, v: Value) -> str:
            """Checks whether `v` an InChI.

            Returns:
               The string value of `v`.

            Raises:
               Spec.Skip: `v` is not an InChI.
            """
            return cls._check(
                cls.check_string(v).value,
                lambda s: s.startswith('InChI='))

    COMPOUND = WD.Q_PUBCHEM_COMPOUND_
    PATENT = WD.Q_PUBCHEM_PATENT_

    @classmethod
    def _init(cls):
        cls.specs = dict()
        cls.iri_prefix_replacements = dict()
        cls.iri_prefix_replacements_inv = dict()
        print(super())


PubChemMapping.register_iri_prefix_replacement(
    PUBCHEM_COMPOUND, PubChemMapping.COMPOUND)

PubChemMapping.register_iri_prefix_replacement(
    PUBCHEM_PATENT, PubChemMapping.PATENT)

Builder: TypeAlias = PubChemMapping.Builder
Spec: TypeAlias = PubChemMapping.Spec
TTrm: TypeAlias = PubChemMapping.Builder.TTrm


@PubChemMapping.register(
    property=wd.described_by_source,
    datatype=Datatype.item,
    subject_prefix=PubChemMapping.COMPOUND,
    value_prefix=PubChemMapping.PATENT)
def wd_described_by_source(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CITO.isDiscussedBy, v),
        (v, RDF.type, PATENT.Publication),
        (substance, SEMSCI.CHEMINF_000477, s))


@PubChemMapping.register(
    property=wd.InChI,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.COMPOUND)
def wd_InChI(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: InChI literals in PubChem are tagged with @en.  We have
        # to add [remove] this tag when converting InChI values to [from]
        # PubChem.
        ###
        sv = spec.check_InChI(cast(Value, v))
        v = Text(sv, 'en')
    with q.sp(s, SEMSCI.SIO_000008) as sp:
        sp.pair(RDF.type, SEMSCI.CHEMINF_000396)
        sp.pair(SEMSCI.SIO_000300, v)


@PubChemMapping.register(
    property=wd.mass,
    datatype=Datatype.quantity,
    unit=wd.gram_per_mole,
    subject_prefix=PubChemMapping.COMPOUND,
    value_set_datatype=XSD.decimal)
def wd_mass(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        qt = spec.check_quantity(cast(Value, v))
        if (qt.unit is not None and qt.unit != spec.kwargs.get('unit')
            or qt.lower_bound is not None
                or qt.upper_bound is not None):
            raise spec.Skip
    with q.sp(s, SEMSCI.SIO_000008) as sp:
        sp.pair(RDF.type, SEMSCI.CHEMINF_000338)
        sp.pair(SEMSCI.SIO_000300, v)


@PubChemMapping.register(
    property=wd.author_name_string,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.PATENT)
def wd_author_name_string(
        spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    with q.sp(s, PATENT.inventorVC) as sp:
        sp.pair(VCARD.fn, v)


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
        (substance, SEMSCI.CHEMINF_000477, v))


@PubChemMapping.register(
    property=wd.patent_number,
    datatype=Datatype.string,
    subject_prefix=PubChemMapping.PATENT)
def wd_patent_number(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, PATENT.publicationNumber, v)


@PubChemMapping.register(
    property=wd.publication_date,
    datatype=Datatype.time,
    subject_prefix=PubChemMapping.PATENT,
    precision=Time.DAY,
    timezone=0,
    calendar=wd.proleptic_Gregorian_calendar)
def wd_publication_date(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        tm = spec.check_time(cast(Value, v))
        if ((tm.precision is not None
             and tm.precision != spec.kwargs.get('precision'))
            or (tm.timezone is not None
                and tm.timezone != spec.kwargs.get('timezone'))
            or (tm.calendar is not None
                and tm.calendar != spec.kwargs.get('calendar'))):
            raise spec.Skip
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
    value_set_language='en')
def wd_title(spec: Spec, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        v = String(spec.check_text(cast(Value, v)).value)
    q.triple(s, PATENT.titleOfInvention, v)
