# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import Callable, cast, NoReturn, TypeVar, Union

from rdflib.namespace import Namespace

from ... import namespace as NS
from ... import vocabulary as wd
from ...model import Item, Quantity, String, Text, Time, Value
from ..sparql_builder import SPARQL_Builder
from ..sparql_mapping import SPARQL_Mapping

Builder = SPARQL_Builder
Entry = SPARQL_Mapping.Entry
T = TypeVar('T')
TTrm = Builder.TTrm
Variable = SPARQL_Builder.Variable

CITO = Namespace('http://purl.org/spar/cito/')
PATENT = Namespace('http://data.epo.org/linked-data/def/patent/')
PUBCHEM = Namespace('http://rdf.ncbi.nlm.nih.gov/pubchem/')
PUBCHEM_COMPOUND = Namespace(str(PUBCHEM) + 'compound/')
PUBCHEM_DESCRIPTOR = Namespace(str(PUBCHEM) + 'descriptor/')
PUBCHEM_PATENT = Namespace(str(PUBCHEM) + 'patent/')
SEMSCI = Namespace('http://semanticscience.org/resource/')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')

PubChemMapping = SPARQL_Mapping()

COMPOUND_REPL = (PUBCHEM_COMPOUND, NS.WD.Q_PUBCHEM_COMPOUND_)
PATENT_REPL = (PUBCHEM_PATENT, NS.WD.Q_PUBCHEM_PATENT_)


class Check:
    exception = SPARQL_Mapping.Entry.Skip

    @classmethod
    def _check(cls, v: T, test: Callable[[T], bool]) -> Union[T, NoReturn]:
        if test(v):
            return v
        else:
            raise cls.exception

    @classmethod
    def quantity(cls, v: Value) -> Quantity:
        if not Quantity.test(v):
            raise cls.exception
        return cast(Quantity, v)

    @classmethod
    def string(cls, v: Value) -> String:
        if not String.test(v):
            raise cls.exception
        return cast(String, v)

    @classmethod
    def text(cls, v: Value) -> Text:
        if not Text.test(v):
            raise cls.exception
        return cast(Text, v)

    @classmethod
    def time(cls, v: Value) -> Time:
        if not Time.test(v):
            raise cls.exception
        return cast(Time, v)

    @classmethod
    def InChI(cls, v: Value) -> str:
        return cls._check(
            cls.string(v).value, lambda s: s.startswith('InChI='))


# -- Compounds -------------------------------------------------------------

@PubChemMapping.register(
    wd.described_by_source, Item,
    subject_replace_prefix=COMPOUND_REPL,
    value_replace_prefix=PATENT_REPL)
def wd_described_by_source(
        entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CITO.isDiscussedBy, v),
        (v, NS.RDF.type, PATENT.Publication),
        (substance, SEMSCI.CHEMINF_000477, s))


@PubChemMapping.register(
    wd.InChI, String,
    subject_replace_prefix=COMPOUND_REPL)
def wd_InChI(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        ###
        # IMPORTANT: InChI literals in PubChem are tagged with @en.  We have
        # to add [remove] this tag when converting InChI values to [from]
        # PubChem.
        ###
        sv = Check.InChI(cast(Value, v))
        v = Text(sv, 'en')
    with q.sp(s, SEMSCI.SIO_000008) as sp:
        sp.pair(NS.RDF.type, SEMSCI.CHEMINF_000396)
        sp.pair(SEMSCI.SIO_000300, v)


@PubChemMapping.register(
    wd.mass, Quantity,
    unit=wd.gram_per_mole,
    subject_replace_prefix=COMPOUND_REPL,
    value_set_datatype=NS.XSD.decimal)
def wd_mass(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        qt = Check.quantity(cast(Value, v))
        if (qt.unit is not None and qt.unit != entry.kwargs.get('unit')
            or qt.lower_bound is not None
                or qt.upper_bound is not None):
            raise entry.Skip
    with q.sp(s, SEMSCI.SIO_000008) as sp:
        sp.pair(NS.RDF.type, SEMSCI.CHEMINF_000338)
        sp.pair(SEMSCI.SIO_000300, v)


# -- Patents ---------------------------------------------------------------

@PubChemMapping.register(
    wd.author_name_string, String,
    subject_replace_prefix=PATENT_REPL)
def wd_author_name_string(
        entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    with q.sp(s, PATENT.inventorVC) as sp:
        sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    wd.main_subject, Item,
    subject_replace_prefix=PATENT_REPL,
    value_replace_prefix=COMPOUND_REPL)
def wd_main_subject(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    substance = q.bnode()
    q.triples(
        (substance, CITO.isDiscussedBy, s),
        (s, NS.RDF.type, PATENT.Publication),
        (substance, SEMSCI.CHEMINF_000477, v))


@PubChemMapping.register(
    wd.patent_number, String,
    subject_replace_prefix=PATENT_REPL)
def wd_patent_number(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    q.triple(s, PATENT.publicationNumber, v)


@PubChemMapping.register(
    wd.publication_date, Time,
    precision=Time.DAY, timezone=0, calendar=wd.proleptic_Gregorian_calendar,
    subject_replace_prefix=PATENT_REPL)
def wd_publication_date(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        tm = Check.time(cast(Value, v))
        if ((tm.precision is not None
             and tm.precision != entry.kwargs.get('precision'))
            or (tm.timezone is not None
                and tm.timezone != entry.kwargs.get('timezone'))
            or (tm.calendar_model is not None
                and tm.calendar_model != entry.kwargs.get('calendar'))):
            raise entry.Skip
    q.triple(s, PATENT.publicationDate, v)


@PubChemMapping.register(
    wd.sponsor, String,
    subject_replace_prefix=PATENT_REPL)
def wd_sponsor(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    with q.sp(s, PATENT.applicantVC) as sp:
        sp.pair(VCARD.fn, v)


@PubChemMapping.register(
    wd.title, Text,
    subject_replace_prefix=PATENT_REPL,
    value_set_language='en')
def wd_title(entry: Entry, q: Builder, s: TTrm, p: TTrm, v: TTrm):
    if Value.test(v):
        v = String(Check.text(cast(Value, v)).value)
    q.triple(s, PATENT.titleOfInvention, v)
