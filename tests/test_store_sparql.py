# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import cast

import kif_lib.vocabulary as wd
from kif_lib import (
    Normal,
    NoValueSnak,
    Preferred,
    Quantity,
    ReferenceRecord,
    SnakMask,
    SomeValueSnak,
    Statement,
    Store,
    String,
    Text,
    Time,
    ValueSnak,
)
from kif_lib.store import SPARQL_Store

from .tests import kif_TestCase, main, skip_if_set, WIKIDATA

skip_if_set('SKIP_TEST_STORE_SPARQL')


class TestSPARQL_Store(kif_TestCase):

    def test__init__(self):
        # bad argument: format
        self.assertRaises(ValueError, Store, 'xxx')
        # good arguments
        kb = Store('sparql', WIKIDATA)
        self.assertIsInstance(kb, SPARQL_Store)
        self.assertEqual(kb._flags, Store.ALL)

    # -- Set interface -----------------------------------------------------

    def test__contains__(self):
        kb = Store('sparql', WIKIDATA)
        self.assertNotIn(0, kb)
        stmt = wd.subclass_of(wd.benzene, wd.aromatic_hydrocarbon)
        self.assertIn(stmt, kb)
        stmt = wd.mass(wd.benzene, Quantity('33.'))
        self.assertNotIn(stmt, kb)
        stmt = wd.ionization_energy(wd.benzene, Quantity('9.24'))
        self.assertIn(stmt, kb)
        stmt = wd.ionization_energy(wd.benzene, Quantity('9.24', wd.dalton))
        self.assertNotIn(stmt, kb)

    def test__iter__(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(iter(kb))
        self.assertIsInstance(stmt, Statement)
        # force pagination
        it = iter(Store('sparql', WIKIDATA, page_size=5))
        for i in range(12):
            self.assertIsInstance(next(it), Statement)

    def test__len__(self):
        kb = Store('sparql', WIKIDATA)
        self.assertTrue(len(kb) > 1_000_000_000)

    # -- Queries -----------------------------------------------------------

    def test__eval_construct_query_string(self):
        from rdflib import Graph
        kb = Store('sparql', WIKIDATA)
        res = kb._eval_construct_query_string(
            'construct {?s ?p ?o} where {?s ?p ?o} limit 1')
        self.assertIsInstance(res, Graph)
        # syntax error
        self.assertRaises(
            SyntaxError, kb._eval_construct_query_string, 'xxx')
        # connection error
        kb = Store('sparql', 'https://example')
        self.assertRaises(
            IOError, kb._eval_construct_query_string,
            'construct {?s ?p ?o} where {?s ?p ?o} limit 1')

    def test__eval_select_query_string(self):
        kb = Store('sparql', WIKIDATA)
        res = kb._eval_select_query_string(
            'select * where {?s ?p ?o} limit 1')
        self.assertEqual(res['head'], {'vars': ['s', 'p', 'o']})
        self.assertIn('bindings', res['results'])

    def test_contains(self):
        kb = Store('sparql', WIKIDATA)
        stmt = wd.subclass_of(wd.benzene, wd.aromatic_hydrocarbon)
        self.assertTrue(kb.contains(stmt))
        # bad argument
        self.assertRaises(TypeError, kb.contains, 0)
        # quantity
        qt = Quantity('16.157')
        self.assertIn(wd.specific_heat_capacity(wd.benzene, qt), kb)
        qt = Quantity('16.155')
        self.assertNotIn(wd.specific_heat_capacity(wd.benzene, qt), kb)
        # quantity with unit
        qt = Quantity('16.157', wd.joule_per_mole_kelvin_difference)
        self.assertIn(wd.specific_heat_capacity(wd.benzene, qt), kb)
        qt = Quantity('16.157', wd.dalton)
        self.assertNotIn(wd.specific_heat_capacity(wd.benzene, qt), kb)
        # quantity with lower/upper bound
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89')
        self.assertIn(wd.density(wd.benzene, qt), kb)
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.87')
        self.assertIn(wd.density(wd.benzene, qt), kb)
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.86')
        self.assertNotIn(wd.density(wd.benzene, qt), kb)
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, None, '.89')
        self.assertIn(wd.density(wd.benzene, qt), kb)
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, None, '.90')
        self.assertNotIn(wd.density(wd.benzene, qt), kb)
        # time
        tm = Time('1822-09-07')
        self.assertTrue(wd.inception(wd.Brazil, tm))
        # time with precision
        tm = Time('1822-09-07', Time.Precision.DAY)
        self.assertIn(wd.inception(wd.Brazil, tm), kb)
        tm = Time('1822-09-07', Time.Precision.YEAR)
        self.assertNotIn(wd.inception(wd.Brazil, tm), kb)
        # time with timezone
        tm = Time('1822-09-07', Time.Precision.DAY, 0)
        self.assertIn(wd.inception(wd.Brazil, tm), kb)
        tm = Time('1822-09-07', Time.Precision.DAY, 1)
        self.assertNotIn(wd.inception(wd.Brazil, tm), kb)
        # time with calendar model
        tm = Time('1822-09-07', None, 0, wd.proleptic_Gregorian_calendar)
        self.assertIn(wd.inception(wd.Brazil, tm), kb)

    def test_count(self):
        kb = Store('sparql', WIKIDATA)
        # bad argument: subject
        self.assertRaises(TypeError, kb.count, 0)
        # bad argument: property
        self.assertRaises(TypeError, kb.count, None, 0)
        # bad argument: value
        self.assertRaises(TypeError, kb.count, None, None, 0)
        # bad argument: snak_class
        self.assertRaises(TypeError, kb.count, None, None, None, 'abc')
        # good arguments
        n = kb.count(subject=wd.benzene, property=wd.mass)
        self.assertEqual(n, 1)
        # everything
        n = kb.count()
        self.assertTrue(n > 1_000_000_000)
        # everything with best rank flag disabled
        kb.unset_flags(kb.BEST_RANK)
        self.assertTrue(kb.count() > n)
        kb.set_flags(kb.BEST_RANK)
        # some value
        n = kb.count(wd.Adam, wd.family_name)
        self.assertEqual(n, 1)
        # no value
        n = kb.count(wd.Adam, wd.father)
        self.assertEqual(n, 1)
        # empty criteria: some value
        kb.unset_flags(kb.SOME_VALUE_SNAK)
        n = kb.count(snak_mask=SnakMask.SOME_VALUE_SNAK)
        self.assertEqual(n, 0)
        # empty criteria: no value
        kb.unset_flags(kb.NO_VALUE_SNAK)
        n = kb.count(snak_mask=SnakMask.NO_VALUE_SNAK)
        self.assertEqual(n, 0)
        # empty criteria: some value & no value
        n = kb.count(snak_mask=SnakMask.SOME_VALUE_SNAK)
        self.assertEqual(n, 0)
        # with best rank flag disabled
        kb = Store('sparql', WIKIDATA)
        kb.unset_flags(kb.BEST_RANK)
        n = kb.count(wd.Adam, wd.date_of_birth)
        self.assertEqual(n, 2)
        # with best rank flag enabled
        kb.set_flags(kb.BEST_RANK)
        n = kb.count(wd.Adam, wd.date_of_birth)
        self.assertEqual(n, 1)

    def test_count_snak(self):
        kb = Store('sparql', WIKIDATA)
        # bad argument: subject
        self.assertRaises(TypeError, kb.count_snak, 0)
        # bad argument: snak
        self.assertRaises(TypeError, kb.count_snak, None, 0)
        # good arguments
        snak = ValueSnak(wd.mass, Quantity('78.11', wd.dalton))
        self.assertEqual(kb.count_snak(None, snak), 1)

    def test_filter(self):
        kb = Store('sparql', WIKIDATA)
        # good arguments
        stmt = next(kb.filter())
        self.assertIsInstance(stmt, Statement)
        # subject
        stmt = next(kb.filter(subject=wd.benzene))
        self.assertEqual(stmt.subject, wd.benzene)
        # subject is fingerprint
        stmt = next(kb.filter([wd.InChIKey(
            String('UHOVQNZJYSORNB-UHFFFAOYSA-N'))]))
        self.assertEqual(stmt.subject, wd.benzene)
        # property
        stmt = next(kb.filter(property=wd.mass))
        self.assertEqual(stmt.snak.property, wd.mass)
        # value: iri
        stmt = next(kb.filter(value=wd.benzene))
        self.assertTrue(stmt.snak.value, wd.benzene)
        # value: text
        stmt = next(kb.filter(
            value=Text('Federative Republic of Brazil', 'en')))
        self.assert_statement(stmt, wd.Brazil, ValueSnak(
            wd.official_name, Text('Federative Republic of Brazil', 'en')))
        # value: string
        stmt = next(kb.filter(value=String('UHOVQNZJYSORNB-UHFFFAOYSA-N')))
        self.assert_statement(stmt, wd.benzene, wd.InChIKey(String(
            'UHOVQNZJYSORNB-UHFFFAOYSA-N')))
        # subject & property
        stmt = next(kb.filter(subject=wd.benzene, property=wd.mass))
        self.assert_statement(stmt, wd.benzene, wd.mass(stmt.snak.value))
        # subject & property: value is text
        stmts = sorted(kb.filter(wd.Brazil, wd.official_name),
                       key=lambda s: cast(ValueSnak, s.snak).value.language)
        self.assert_statement(
            stmts[0], wd.Brazil, ValueSnak(
                wd.official_name, Text(
                    'Federative Republic of Brazil', 'en')))
        self.assert_statement(
            stmts[1], wd.Brazil, ValueSnak(
                wd.official_name, Text(
                    'République fédérative du Brésil', 'fr')))
        # subject & value: quantity
        stmt = next(kb.filter(
            subject=wd.benzene, value=Quantity('9.24', wd.electronvolt)))
        qt = Quantity('9.24', wd.electronvolt, '9.23', '9.25')
        self.assert_statement(stmt, wd.benzene, wd.ionization_energy(qt))
        # subject & value: time
        stmt = next(kb.filter(subject=wd.Brazil, value=Time('1822-09-07')))
        self.assert_statement(stmt, wd.Brazil, wd.inception(stmt.snak.value))
        # property & value: quantity
        stmt = next(kb.filter(
            property=wd.ionization_energy,
            value=Quantity('9.24', None, '9.23', '9.25')))
        qt = Quantity('9.24', wd.electronvolt, '9.23', '9.25')
        self.assert_statement(stmt, wd.benzene, wd.ionization_energy(qt))
        ###
        # TODO: property & value: quantity without unit
        ###
        # property & value: time
        stmt = next(kb.filter(
            property=wd.inception, value=Time('1822-09-07', 11, 0)))
        self.assertEqual(stmt.subject, wd.Brazil)
        ###
        # TODO: property & value: time without precision
        ###
        # subject & property: some value
        stmt = next(kb.filter(wd.Adam, wd.date_of_death))
        self.assertTrue(stmt.snak.is_some_value_snak())
        # subject & property: no value
        stmt = next(kb.filter(wd.Adam, wd.date_of_birth))
        self.assertTrue(stmt.snak.is_no_value_snak())
        # snak_class: some value
        some = list(sorted(kb.filter(
            wd.Adam, None, None, SnakMask.SOME_VALUE_SNAK)))
        self.assertEqual(len(some), 2)
        # snak_class: no value
        wdno = list(sorted(kb.filter(
            wd.Adam, None, None, SnakMask.NO_VALUE_SNAK)))
        self.assert_statement(wdno[0], wd.Adam, NoValueSnak(wd.father))
        self.assert_statement(wdno[1], wd.Adam, NoValueSnak(wd.mother))
        self.assert_statement(wdno[2], wd.Adam, NoValueSnak(wd.date_of_birth))
        # subject & property: some value (newer Wikidata)
        kb = Store('sparql', WIKIDATA)
        it = kb.filter(wd.Adam, wd.date_of_death)
        self.assertTrue(next(it).snak.is_some_value_snak())
        self.assertRaises(StopIteration, next, it)
        # empty criteria: some value
        kb.unset_flags(kb.SOME_VALUE_SNAK)
        self.assertFalse(list(kb.filter(
            snak_mask=SnakMask.SOME_VALUE_SNAK)))
        # empty criteria: no value
        kb.unset_flags(kb.NO_VALUE_SNAK)
        self.assertFalse(list(kb.filter(snak_mask=SnakMask.NO_VALUE_SNAK)))
        # empty criteria: some value & no value
        self.assertFalse(list(kb.filter(snak_mask=SnakMask.SOME_VALUE_SNAK)))
        # limit
        kb = Store('sparql', WIKIDATA)
        stmts = list(kb.filter(wd.Adam, limit=120))
        self.assertEqual(len(stmts), 120)

    def test_filter_snak(self):
        kb = Store('sparql', WIKIDATA)
        # bad argument: subject
        self.assertRaises(TypeError, kb.filter_snak, 0)
        # bad argument: snak
        self.assertRaises(TypeError, kb.filter_snak, None, 0)
        # good arguments
        snak = ValueSnak(wd.mass, Quantity('78.11', wd.dalton))
        stmt = next(kb.filter_snak(None, snak))
        self.assert_statement(
            stmt, wd.benzene, wd.mass(Quantity('78.11', wd.dalton)))
        # subject is a property
        stmt = next(kb.filter_snak(
            None, wd.type_of_unit_for_this_property(wd.unit_of_mass)))
        self.assertTrue(stmt.subject.is_property())
        # subject is fingerprint
        stmt = next(kb.filter_snak(
            [wd.InChIKey(String('UHOVQNZJYSORNB-UHFFFAOYSA-N'))]))
        self.assertEqual(stmt.subject, wd.benzene)
        # snak: None
        stmt = next(kb.filter_snak(wd.Adam, limit=1))
        self.assert_statement(stmt, wd.Adam, stmt.snak)
        # snak: some value
        stmt = next(kb.filter_snak(wd.Adam, SomeValueSnak(wd.family_name)))
        self.assert_statement(stmt, wd.Adam, SomeValueSnak(wd.family_name))
        # snak: no value
        stmt = next(kb.filter_snak(wd.Adam, NoValueSnak(wd.father)))
        self.assert_statement(stmt, wd.Adam, NoValueSnak(wd.father))
        # limit
        kb = Store('sparql', WIKIDATA)
        stmts = list(kb.filter_snak(wd.Adam, limit=0))
        self.assertEqual(len(stmts), 0)

    # -- Annotations -------------------------------------------------------

    def test_get_qualifiers(self):
        kb = Store('sparql', WIKIDATA)

        def get_qualifiers(stmt):
            stmt, annots = next(kb.get_annotations([stmt]))
            if annots is None:
                raise ValueError
            else:
                return annots[0].qualifiers
        # good arguments
        qt = Quantity('16.157', wd.joule_per_mole_kelvin_difference)
        stmt = wd.specific_heat_capacity(wd.benzene, qt)
        self.assertIn(stmt, kb)
        quals = sorted(list(get_qualifiers(stmt)))
        self.assertEqual(len(quals), 2)
        self.assertEqual(
            quals[0], wd.temperature(Quantity('298', wd.kelvin)))
        self.assertEqual(quals[1], wd.phase_of_matter(wd.liquid))
        stmt = next(kb.filter(
            wd.benzene, wd.safety_classification_and_labelling, limit=1))
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 4)
        # no such statement
        self.assertRaises(
            ValueError, get_qualifiers,
            wd.inception(wd.Brazil, Time('2023-09-05')))
        # no such statement: force cache hit
        self.assertRaises(
            ValueError, get_qualifiers,
            wd.inception(wd.Brazil, Time('2023-09-05')))
        # no qualifiers
        stmt = wd.mass(wd.benzene, Quantity('78.11', wd.dalton))
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 0)
        # statement with deep value
        stmt = wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))
        quals = sorted(list(get_qualifiers(stmt)))
        self.assertEqual(
            quals[0],
            wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)))
        self.assertEqual(
            quals[1],
            wd.phase_of_matter(wd.liquid))
        # statement is a some value
        stmt = Statement(wd.Adam, SomeValueSnak(wd.date_of_death))
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 0)
        # one of the qualifiers is a quantity
        stmt = wd.lowest_point(wd.Brazil, wd.Atlantic_Ocean)
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 1)
        self.assert_value_snak(
            quals[0], wd.elevation_above_sea_level, Quantity(0, wd.metre))
        # one of the qualifiers is a time
        stmt = wd.country(wd.Brazil, wd.Brazil)
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 1)
        self.assert_value_snak(
            quals[0], wd.start_time, Time(
                '1822-01-01', 9, 0, wd.proleptic_Gregorian_calendar))
        # one of the qualifiers is a some value
        stmt = wd.YouTube_video_ID(
            wd.Supercalifragilisticexpialidocious, String('tRFHXMQP-QU'))
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 1)
        self.assert_some_value_snak(quals[0], wd.end_time)
        # same thing with newer Wikidata
        quals = get_qualifiers(stmt)
        self.assertEqual(len(quals), 1)
        self.assert_some_value_snak(quals[0], wd.end_time)
        # statement is a no value
        stmt = Statement(wd.Germany, NoValueSnak(wd.speed_limit))
        quals = list(get_qualifiers(stmt))
        self.assertEqual(len(quals), 1)
        self.assert_value_snak(
            quals[0], wd.valid_in_place, wd.autobahn_in_Germany)
        # one of the qualifiers is a no value
        Italo_Balbo = wd.Q(1056)
        Governor_General_of_Italian_Libya = wd.Q(59859989)
        it = kb.filter(Italo_Balbo, wd.position_held,
                       Governor_General_of_Italian_Libya)
        quals = list(filter(
            lambda q: q.is_no_value_snak(), get_qualifiers(next(it))))
        self.assertEqual(len(quals), 1)
        self.assert_no_value_snak(quals[0], wd.P(1365))

    def test_get_references(self):
        kb = Store('sparql', WIKIDATA)

        def get_references(stmt):
            stmt, annots = next(kb.get_annotations([stmt]))
            if annots is None:
                raise ValueError
            else:
                if annots:
                    return annots[0].references
                else:
                    return annots
        # good arguments
        stmt = wd.inception(
            wd.Brazil,
            Time('1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar))
        refs = get_references(stmt)
        self.assertEqual(len(refs), 3)
        found = False
        for r in refs:
            if wd.imported_from_Wikimedia_project(wd.English_Wikipedia):
                found = True
                break
        self.assertTrue(found)
        # no such statement
        self.assertRaises(
            ValueError, get_references,
            wd.inception(wd.Brazil, Time('2023-09-05')))
        # no such statement: force cache hit
        self.assertRaises(
            ValueError, get_references,
            wd.inception(wd.Brazil, Time('2023-09-05')))
        # no references
        stmt = wd.instance_of(wd.Brazil, wd.country_)
        refs = list(get_references(stmt))
        self.assertEqual(len(refs), 0)
        # statement with deep value
        stmt = wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))
        refs = sorted(list(get_references(stmt)))
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0], ReferenceRecord(
            wd.HSDB_ID(String('35#section=TSCA-Test-Submissions')),
            wd.stated_in(wd.Hazardous_Substances_Data_Bank)))
        ###
        # TODO: statement is a some value
        ###
        # one of the snaks is a quantity
        Revele = wd.Q(104532651)
        reverse_Bechdel_Test = wd.Q(105776216)
        stmt = wd.assessment(Revele, reverse_Bechdel_Test)
        refs = get_references(stmt)
        self.assertEqual(len(refs), 1)
        self.assertEqual(len(refs[0]), 4)
        self.assertIn(ValueSnak(wd.stated_in, Revele), refs[0])
        self.assertIn(
            ValueSnak(wd.time_index, Quantity('15.9', wd.minute)), refs[0])
        ###
        # TODO: one of the snaks is a time
        ###
        # TODO: one of the qualifiers is a some value
        ###
        # TODO: same thing with newer Wikidata
        ###
        # statement is a no value
        stmt = Statement(wd.Germany, NoValueSnak(wd.speed_limit))
        refs = list(get_references(stmt))
        self.assertEqual(len(refs), 1)
        self.assertIn(ValueSnak(wd.stated_in, wd.Q(11774726)), refs[0])
        ###
        # TODO: one of the references is a no value
        ###

    def test_get_rank(self):
        kb = Store('sparql', WIKIDATA)

        def get_rank(stmt):
            stmt, annots = next(kb.get_annotations([stmt]))
            if annots is None:
                raise ValueError
            else:
                return annots[0].rank
        # preferred
        stmt = Statement(wd.Adam, NoValueSnak(wd.date_of_birth))
        self.assertEqual(get_rank(stmt), Preferred)
        # normal
        stmt = Statement(
            wd.Adam, ValueSnak(wd.place_of_birth, wd.Garden_of_Eden))
        self.assertEqual(get_rank(stmt), Normal)
        ###
        # TODO: deprecated
        ###
        # no such statement
        self.assertRaises(
            ValueError, get_rank,
            wd.inception(wd.Brazil, Time('2023-09-05')))
        # no such statement: force cache hit
        self.assertRaises(
            ValueError, get_rank,
            wd.inception(wd.Brazil, Time('2023-09-05')))


if __name__ == '__main__':
    main()
