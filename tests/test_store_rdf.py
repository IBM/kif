# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    Filter,
    NormalRank,
    NoValueSnak,
    PreferredRank,
    QualifierRecord,
    Quantity,
    ReferenceRecord,
    ReferenceRecordSet,
    SomeValueSnak,
    Statement,
    Store,
    Text,
    Time,
)
from kif_lib.store.rdf import RDF_Store
from kif_lib.typing import cast
from kif_lib.vocabulary import wd

from .data import ADAM_TTL, BENZENE_TTL, BRAZIL_TTL
from .tests import StoreTestCase


class TestStoreRDF(StoreTestCase):

    def test_sanity(self) -> None:
        self.store_sanity_checks(Store('rdf', BENZENE_TTL))

    def test__iter__(self) -> None:
        kb = cast(RDF_Store, Store('rdf', BENZENE_TTL))
        stmt = next(iter(kb))
        self.assertIsInstance(stmt, Statement)
        # force pagination
        it = iter(Store('rdf', BENZENE_TTL, page_size=1))
        for i in range(3):
            self.assertIsInstance(next(it), Statement)

    def test__len__(self) -> None:
        kb = Store('rdf', BENZENE_TTL)
        self.assertEqual(len(kb), 6)

    def test__eval_select_query_string(self) -> None:
        kb = cast(RDF_Store, Store('rdf', BENZENE_TTL))
        res = kb._eval_select_query_string(
            'select * where {?s ?p ?o} limit 1')
        self.assertIn('vars', res['head'])
        self.assertIn('bindings', res['results'])

    def test_contains(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_contains(kb)

    def _test_contains(self, kb) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.store_test_contains(
            kb,
            wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
            # quantity
            wd.density(wd.benzene, Quantity('0.88')),
            wd.density(wd.benzene, Quantity(
                '0.88', wd.gram_per_cubic_centimetre)),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, None, '.89')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
            # time
            wd.inception(wd.Brazil, Time('1822-09-07')),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.Precision.DAY)),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.DAY, 0)),
            wd.inception(wd.Brazil, Time(
                '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)),
            # some value
            Statement(wd.Adam, SomeValueSnak(wd.family_name)),
            # no value
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)))
        self.store_test_not_contains(
            kb,
            wd.instance_of(wd.benzene, wd.chemical_compound),
            # quantity
            wd.density(wd.benzene, Quantity('0.89')),
            wd.density(wd.benzene, Quantity(
                '0.89', wd.gram_per_cubic_centimetre)),
            wd.density(wd.benzene, Quantity('0.89', wd.kilogram)),
            wd.density(wd.benzene, Quantity(
                '.89', wd.gram_per_cubic_centimetre, '.87', '.89')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.88', '.89')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.88')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, None, '.88')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.88', '.89')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.88')),
            # time
            wd.inception(wd.Brazil, Time('1822-09-08')),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.YEAR)),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.DAY, 1)),
            wd.inception(wd.Brazil, Time(
                '1822-09-07', Time.DAY, 0, wd.proleptic_Julian_calendar)),
            # some value
            Statement(wd.Brazil, SomeValueSnak(wd.inception)),
            # no value
            Statement(wd.Brazil, NoValueSnak(wd.inception)))

    def test_contains_any_rank(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_contains_any_rank(kb)

    def _test_contains_any_rank(self, kb) -> None:
        self.store_test_contains(
            kb,
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)))
        self.store_test_not_contains(
            kb,
            wd.date_of_birth(wd.Adam, Time(
                '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)))
        kb.unset_flags(kb.BEST_RANK)
        self.store_test_contains(
            kb,
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
            wd.date_of_birth(wd.Adam, Time(
                '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)))

    def test_count(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_count(kb)

    def _test_count(self, kb) -> None:
        self.store_test_count(kb, 15)
        self.store_test_count(kb, 12, snak_mask=Filter.VALUE_SNAK)
        self.store_test_count(kb, 2, snak_mask=Filter.NO_VALUE_SNAK)
        self.store_test_count(kb, 1, snak_mask=Filter.SOME_VALUE_SNAK)
        self.store_test_count(kb, 2, wd.InChIKey)
        self.store_test_count(kb, 4, wd.Brazil)
        self.store_test_count(kb, 1, wd.benzene, wd.mass)
        # text
        self.store_test_count(kb, 0, None, None, Text('Brazil', 'en'))
        # quantity
        self.store_test_count(kb, 1, wd.benzene, wd.mass,
                              Quantity('78.046950192'))
        self.store_test_count(kb, 1, None, wd.mass, Quantity('78.046950192'))
        self.store_test_count(kb, 1, None, None, Quantity('78.046950192'))
        self.store_test_count(kb, 0, None, None, Quantity('78.12'))
        self.store_test_count(
            kb, 1, None, wd.mass, Quantity('78.046950192', wd.dalton))
        self.store_test_count(
            kb, 0, None, wd.mass, Quantity('78.046950192', wd.kilogram))
        self.store_test_count(
            kb, 1, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre))
        self.store_test_count(
            kb, 1, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre, '0.87'))
        self.store_test_count(
            kb, 0, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre, '0.88'))
        self.store_test_count(
            kb, 1, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre, None, '0.89'))
        self.store_test_count(
            kb, 0, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre, None, '0.88'))
        self.store_test_count(
            kb, 1, None, wd.density, Quantity(
                '0.88', wd.gram_per_cubic_centimetre, '0.87', '0.89'))
        # time
        self.store_test_count(kb, 1, None, None, Time('1822-09-07'))
        self.store_test_count(kb, 0, None, None, Time('1822-09-08'))
        self.store_test_count(kb, 1, None, wd.inception, Time('1822-09-07'))
        self.store_test_count(kb, 1, None, wd.inception, Time(
            '1822-09-07', Time.DAY))
        self.store_test_count(kb, 0, None, wd.inception, Time(
            '1822-09-07', Time.YEAR))
        self.store_test_count(kb, 1, None, wd.inception, Time(
            '1822-09-07', None, 0))
        self.store_test_count(kb, 0, None, wd.inception, Time(
            '1822-09-07', 11, 1))
        self.store_test_count(kb, 1, None, wd.inception, Time(
            '1822-09-07', None, None, wd.proleptic_Gregorian_calendar))
        self.store_test_count(kb, 0, None, wd.inception, Time(
            '1822-09-07', None, None, wd.proleptic_Julian_calendar))
        # some value
        self.store_test_count(
            kb, 1, None, None, None, Filter.SOME_VALUE_SNAK)
        self.store_test_count(
            kb, 1, None, wd.family_name, None, Filter.SOME_VALUE_SNAK)
        # no value
        self.store_test_count(
            kb, 2, None, None, None, Filter.NO_VALUE_SNAK)
        self.store_test_count(
            kb, 1, None, wd.date_of_birth, None, Filter.NO_VALUE_SNAK)
        self.store_test_count(
            kb, 1, None, wd.father, None, Filter.NO_VALUE_SNAK)
        # subject is snak set
        self.store_test_count(
            kb, 4, wd.instance_of(wd.type_of_a_chemical_entity))
        # property is snak set
        self.store_test_count(kb, 2, wd.InChIKey)
        self.store_test_count(kb, 1, None, wd.related_property(wd.InChI))
        # value is snak set
        self.store_test_count(
            kb, 1, None, None,
            wd.demonym(Text('Latinoamericana', 'es')))
        self.store_test_count(
            kb, 0, None, None,
            wd.demonym(Text('Latinoamericana', 'en')))

    def test_count_any_rank(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_count_any_rank(kb)

    def _test_count_any_rank(self, kb) -> None:
        self.store_test_count(kb, 15)
        kb.unset_flags(kb.BEST_RANK)
        self.store_test_count(kb, 16)

    # -- filter --

    def test_filter(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_filter_tail(kb)

    def _test_filter_tail(self, kb) -> None:
        # subject
        self.store_test_filter(
            kb,
            stmts=[
                wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
                wd.InChIKey(
                    wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')),
                wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),
                wd.density(wd.benzene, Quantity(
                    '0.88', wd.gram_per_cubic_centimetre, '0.87', '.89'))],
            subject=wd.benzene
        )
        self.store_test_filter(
            kb,
            stmts=[
                wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
                wd.InChIKey(
                    wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')),
                wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),
                wd.density(wd.benzene, Quantity(
                    '0.88', wd.gram_per_cubic_centimetre, '0.87', '.89'))],
            subject=wd.InChIKey('UHOVQNZJYSORNB-UHFFFAOYSA-N')
        )
        # subject, property
        self.store_test_filter(
            kb,
            stmts=[wd.InChIKey(
                wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N'))],
            subject=wd.benzene,
            property=wd.InChIKey
        )
        self.store_test_filter(
            kb,
            stmts=[wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))],
            subject=wd.benzene,
            property=wd.mass
        )
        self.store_test_filter(
            kb,
            stmts=[wd.InChIKey(
                wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N'))],
            subject=wd.instance_of(wd.type_of_a_chemical_entity),
            property=wd.InChIKey
        )
        self.store_test_filter(
            kb,
            stmts=[wd.InChIKey(
                wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N'))],
            subject=wd.benzene,
            property=wd.related_property(wd.InChI)
        )
        # subject, property, value
        self.store_test_filter(
            kb,
            stmts=[wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))],
            subject=wd.benzene,
            property=wd.mass,
            value=Quantity('78.046950192', wd.dalton)
        )
        self.store_test_filter(
            kb,
            stmts=[],
            subject=wd.benzene,
            property=wd.mass,
            value=Quantity('78.12', wd.dalton)
        )
        # property
        self.store_test_filter(
            kb,
            stmts=[wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))],
            subject=None,
            property=wd.mass
        )
        self.store_test_filter(
            kb,
            stmts=[
                wd.density(wd.benzene, Quantity(
                    '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))
            ],
            subject=None,
            property=wd.density
        )
        self.store_test_filter(
            kb,
            stmts=[wd.InChIKey(
                wd.benzene, ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N'))],
            subject=None,
            property=(
                wd.instance_of(wd.Wikidata_property_to_identify_substances)
                & wd.related_property(wd.InChI))
        )
        # property, value
        self.store_test_filter(
            kb,
            stmts=[
                wd.density(wd.benzene, Quantity(
                    '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))
            ],
            subject=None,
            property=wd.density,
            value=Quantity('.88')
        )
        self.store_test_filter(
            kb,
            stmts=[],
            subject=None,
            property=wd.density,
            value=Quantity('.88', wd.kilogram)
        )
        # value
        self.store_test_filter(
            kb,
            stmts=[],
            subject=None,
            property=None,
            value=Text('Brazil', 'en')
        )
        self.store_test_filter(
            kb,
            stmts=[wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))],
            subject=None,
            property=None,
            value=Quantity('78.046950192')
        )
        self.store_test_filter(
            kb,
            stmts=[],
            subject=None,
            property=None,
            value=Quantity('78.046950192', wd.kilogram)
        )
        self.store_test_filter(
            kb,
            stmts=[
                wd.inception(wd.Brazil, Time(
                    '1822-09-07', Time.DAY, 0,
                    wd.proleptic_Gregorian_calendar))
            ],
            subject=None,
            property=None,
            value=Time('1822-09-07')
        )
        self.store_test_filter(
            kb,
            stmts=[],
            subject=None,
            property=None,
            value=Time('1822-09-07', Time.YEAR)
        )
        # some value
        self.store_test_filter(
            kb,
            stmts=[Statement(wd.Adam, SomeValueSnak(wd.family_name))],
            subject=None,
            property=wd.family_name,
            value=None,
            snak_mask=Filter.SOME_VALUE_SNAK
        )
        self.store_test_filter(
            kb,
            stmts=[Statement(wd.Adam, SomeValueSnak(wd.family_name))],
            subject=None,
            property=None,
            value=None,
            snak_mask=Filter.SOME_VALUE_SNAK
        )
        # no value
        self.store_test_filter(
            kb,
            stmts=[Statement(wd.Adam, NoValueSnak(wd.date_of_birth))],
            subject=None,
            property=wd.date_of_birth,
            value=None,
            snak_mask=Filter.NO_VALUE_SNAK
        )
        self.store_test_filter(
            kb,
            stmts=[
                Statement(wd.Adam, NoValueSnak(wd.father)),
                Statement(wd.Adam, NoValueSnak(wd.date_of_birth))
            ],
            subject=None,
            property=None,
            value=None,
            snak_mask=Filter.NO_VALUE_SNAK
        )

    def test_filter_any_rank(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_filter_any_rank(kb)

    def _test_filter_any_rank(self, kb) -> None:
        self.store_test_filter(
            kb,
            stmts=[Statement(wd.Adam, NoValueSnak(wd.date_of_birth))],
            subject=wd.Adam,
            property=wd.date_of_birth
        )
        kb.unset_flags(kb.BEST_RANK)
        kb.unset_flags(kb.LATE_FILTER)
        self.store_test_filter(
            kb,
            stmts=[
                Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
                wd.date_of_birth(wd.Adam, Time(
                    '4003-01-01', 9, 0, wd.proleptic_Julian_calendar))
            ],
            subject=wd.Adam,
            property=wd.date_of_birth
        )
        kb.set_flags(kb.LATE_FILTER)

    def test_get_annotations(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self._test_get_annotations(kb)

    def _test_get_annotations(self, kb) -> None:
        self.store_test_get_annotations(
            kb,
            [(wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),  # 0
              {(
                  QualifierRecord(),
                  ReferenceRecordSet(
                      ReferenceRecord(
                          wd.stated_in(wd.PubChem),
                          wd.language_of_work_or_name(wd.English),
                          wd.PubChem_CID('241'),
                          wd.title(Text('benzene', 'en')),
                          wd.retrieved(Time(
                              '2016-10-19', 11, 0,
                              wd.proleptic_Gregorian_calendar)))),
                  NormalRank())}),
             # 1
             (wd.mass(wd.benzene, Quantity('78.046950192')), None),
             # 2
             (wd.density(wd.benzene, Quantity(
                 '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
              {(QualifierRecord(
                  wd.phase_of_matter(wd.liquid),
                  wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21))),
                ReferenceRecordSet(
                    ReferenceRecord(
                        wd.stated_in(wd.Hazardous_Substances_Data_Bank),
                        wd.HSDB_ID('35#section=TSCA-Test-Submissions'))),
                NormalRank())}),
             # 3
             (Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
              {(QualifierRecord(),
                ReferenceRecordSet(
                    ReferenceRecord(
                        wd.reference_URL('http://islamqa.info/ar/20907'))),
                PreferredRank())}),
             # 4
             (wd.date_of_birth(wd.Adam, Time(
                 '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)), None),
             # 5
             (wd.demonym(wd.Latin_America, Text('Latinoamericana', 'es')),
              {(QualifierRecord(wd.applies_to_part(wd.feminine)),
                ReferenceRecordSet(), NormalRank())})
             ],
            wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),
            wd.mass(wd.benzene, Quantity('78.046950192')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
            wd.date_of_birth(wd.Adam, Time(
                '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)),
            wd.demonym(wd.Latin_America, Text('Latinoamericana', 'es')))
        # empty batch
        self.store_test_get_annotations(
            kb,
            [(wd.inception(wd.Brazil, Time('1822-09-08')), None)],
            wd.inception(wd.Brazil, Time('1822-09-08')))
        # extra references
        saved_references = kb.extra_references
        kb.extra_references = [
            ReferenceRecord(
                wd.stated_in(wd.Wikidata),
                wd.reference_URL('http://www.wikidata.org/')),
            ReferenceRecord(
                wd.stated_in(wd.PubChem))]
        self.store_test_get_annotations(
            kb,
            [(wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),  # 0
              {(QualifierRecord(),
                ReferenceRecordSet(
                    ReferenceRecord(
                        wd.stated_in(wd.PubChem),
                        wd.language_of_work_or_name(wd.English),
                        wd.PubChem_CID('241'),
                        wd.title(Text('benzene', 'en')),
                        wd.retrieved(Time(
                            '2016-10-19', 11, 0,
                            wd.proleptic_Gregorian_calendar))),
                    ReferenceRecord(
                        wd.stated_in(wd.Wikidata),
                        wd.reference_URL('http://www.wikidata.org/')),
                    ReferenceRecord(
                        wd.stated_in(wd.PubChem))),
                NormalRank())}),
             # 1
             (wd.density(wd.benzene, Quantity(
                 '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
              {(QualifierRecord(
                  wd.phase_of_matter(wd.liquid),
                  wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21))),
                ReferenceRecordSet(
                    ReferenceRecord(
                        wd.stated_in(wd.Hazardous_Substances_Data_Bank),
                        wd.HSDB_ID('35#section=TSCA-Test-Submissions')),
                    ReferenceRecord(
                        wd.stated_in(wd.Wikidata),
                        wd.reference_URL('http://www.wikidata.org/')),
                    ReferenceRecord(
                        wd.stated_in(wd.PubChem))),
                NormalRank())}),
             ],
            wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89')))
        kb.extra_references = saved_references

    def test_get_annotations_any_rank(self) -> None:
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        kb.unset_flags(kb.BEST_RANK)
        self.store_test_get_annotations(
            kb,
            [(Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
              {(QualifierRecord(),
                ReferenceRecordSet(
                    ReferenceRecord(
                        wd.reference_URL('http://islamqa.info/ar/20907'))),
                PreferredRank())}),
             (wd.date_of_birth(wd.Adam, Time(
                 '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)),
              {(QualifierRecord(
                  wd.statement_supported_by(wd.Q(746069))),
                ReferenceRecordSet(
                    ReferenceRecord(wd.reference_URL(
                        'https://amazingbibletimeline.com/'
                        'timeline_online/'))),
                NormalRank())})
             ],
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
            wd.date_of_birth(wd.Adam, Time(
                '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)))


if __name__ == '__main__':
    TestStoreRDF.main()
