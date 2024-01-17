# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import (
    FilterPattern,
    IRI,
    Item,
    NoValueSnak,
    Quantity,
    SnakMask,
    SomeValueSnak,
    Statement,
    Store,
    String,
    Text,
    Time,
    ValueSnak,
)

from .tests import kif_TestCase, main, skip_if_set, WIKIDATA

skip_if_set('SKIP_TEST_STORE_SPARQL')


class TestSPARQL_StoreFilter(kif_TestCase):

    def test_filter_bad_argument(self):
        kb = Store('sparql', WIKIDATA)
        # bad argument: subject
        self.assertRaises(TypeError, kb.filter, 0)
        self.assertRaises(TypeError, kb.filter, IRI('x'))
        # bad argument: property
        self.assertRaises(TypeError, kb.filter, None, 0)
        self.assertRaises(TypeError, kb.filter, None, IRI('x'))
        # bad argument: value
        self.assertRaises(TypeError, kb.filter, None, None, 0)
        # bad argument: snak_mask
        self.assertRaises(
            TypeError, kb.filter, None, None, None, 'abc')
        self.assertRaises(
            TypeError, kb.filter, None, None, Item('x'), NoValueSnak)
        # bad argument: pattern
        self.assertRaises(TypeError, kb.filter, pattern=Item('x'))
        # bad argument: limit
        self.assertRaises(TypeError, kb.filter, limit=Item('x'))

    def test_filter_full(self):
        kb = Store('sparql', WIKIDATA)
        pat = FilterPattern()
        self.assertEqual(len(list(kb.filter(pattern=pat, limit=1))), 1)

    def test_filter_empty(self):
        kb = Store('sparql', WIKIDATA)
        pat = FilterPattern(None, None, None, SnakMask(0))
        self.assertEqual(len(list(kb.filter(pattern=pat, limit=1))), 0)

    def test_filter_subject_is_item(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(wd.Brazil))
        self.assertEqual(stmt.subject, wd.Brazil)

    def test_filter_subject_is_snak_set(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter([
            wd.official_language(wd.Portuguese),
            wd.part_of(wd.Latin_America)]))
        self.assertEqual(stmt.subject, wd.Brazil)
        # some value snak
        stmt = next(kb.filter(
            SomeValueSnak(wd.date_of_death), wd.spouse, wd.Eve))
        stmt = next(kb.filter(stmt.subject, wd.date_of_death))
        self.assert_statement(
            stmt, stmt.subject, SomeValueSnak(wd.date_of_death))
        # no value snak
        stmt = next(kb.filter(
            [NoValueSnak(wd.date_of_birth)], wd.spouse, wd.Eve))
        stmt = next(kb.filter(stmt.subject, wd.date_of_birth))
        self.assert_statement(
            stmt, stmt.subject, NoValueSnak(wd.date_of_birth))

    def test_filter_property_is_property(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(property=wd.part_of))
        self.assertEqual(stmt.snak.property, wd.part_of)

    def test_filter_property_is_snak_set(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(
            subject=wd.Brazil,
            property=wd.Wikidata_item_of_this_property(wd.part),
            value=wd.Latin_America))
        self.assert_statement(
            stmt, wd.Brazil, ValueSnak(wd.part_of, wd.Latin_America))

    def test_filter_value_is_item(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(wd.Brazil, wd.continent, wd.South_America))
        self.assert_statement(
            stmt, wd.Brazil, wd.continent(wd.South_America))

    def test_filter_value_is_property(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(None, wd.Wikidata_property, wd.continent))
        self.assert_statement(
            stmt, wd.continent_, wd.Wikidata_property(wd.continent))

    def test_filter_value_is_iri(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(wd.benzene, wd.chemical_structure))
        self.assert_statement(
            stmt, wd.benzene, wd.chemical_structure(IRI(
                'http://commons.wikimedia.org/wiki/Special:FilePath/'
                'Benzene-2D-full.svg')))

    def test_filter_value_is_text(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(
            value=Text('Federative Republic of Brazil', 'en')))
        self.assert_statement(
            stmt, wd.Brazil, wd.official_name(Text(
                'Federative Republic of Brazil', 'en')))

    def test_filter_value_is_string(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(value=String('UHOVQNZJYSORNB-UHFFFAOYSA-N')))
        self.assert_statement(
            stmt, wd.benzene,
            wd.InChIKey(String('UHOVQNZJYSORNB-UHFFFAOYSA-N')))

    def test_filter_value_is_quantity(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(wd.benzene, value=Quantity('78.11')))
        self.assert_statement(
            stmt, wd.benzene, wd.mass(Quantity('78.11', wd.dalton)))
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89')
        stmt = next(kb.filter(wd.benzene, wd.density, qt))
        self.assert_statement(stmt, wd.benzene, wd.density(qt))
        stmt = next(kb.filter(wd.benzene, wd.density, qt.replace(
            None, qt.Nil, qt.Nil, qt.Nil)))
        self.assert_statement(stmt, wd.benzene, wd.density(qt))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.benzene, wd.density, qt.replace(
                    '.87', qt.Nil, qt.Nil, qt.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.benzene, wd.density, qt.replace(
                    None, wd.kilogram, qt.Nil, qt.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.benzene, wd.density, qt.replace(
                    None, qt.Nil, '.88', qt.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.benzene, wd.density, qt.replace(
                    None, qt.Nil, qt.Nil, '.88')))

    def test_filter_value_is_time(self):
        kb = Store('sparql', WIKIDATA)
        tm = Time(
            '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)
        stmt = next(kb.filter(wd.Brazil, wd.inception, tm))
        self.assert_statement(stmt, wd.Brazil, wd.inception(tm))
        stmt = next(kb.filter(wd.Brazil, wd.inception, tm.replace(
            None, tm.Nil, tm.Nil, tm.Nil)))
        self.assert_statement(stmt, wd.Brazil, wd.inception(tm))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.Brazil, wd.inception, tm.replace(
                    '1822-09-08', tm.Nil, tm.Nil, tm.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.Brazil, wd.inception, tm.replace(
                    None, tm.HOUR, tm.Nil, tm.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.Brazil, wd.inception, tm.replace(
                    None, tm.Nil, 1, tm.Nil)))
        self.assertRaises(
            StopIteration, next, kb.filter(
                wd.Brazil, wd.inception, tm.replace(
                    None, tm.Nil, 0, wd.proleptic_Julian_calendar)))

    def test_filter_value_is_snak_set(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(value=[
            wd.official_language(wd.Portuguese),
            wd.inception(Time('1822-09-07')),
            wd.continent(wd.South_America)]))
        self.assert_value_snak(stmt.snak, stmt.snak.property, wd.Brazil)
        # some value snak
        stmt = next(kb.filter(
            property=wd.father, value=SomeValueSnak(wd.date_of_death)))
        stmt = next(kb.filter(stmt.snak.value, wd.date_of_death))
        self.assert_statement(
            stmt, stmt.subject, SomeValueSnak(wd.date_of_death))
        # no value snak
        stmt = next(kb.filter(value=[NoValueSnak(wd.date_of_birth)]))
        stmt = next(kb.filter(stmt.snak.value, wd.date_of_birth))
        self.assert_statement(
            stmt, stmt.subject, NoValueSnak(wd.date_of_birth))

    def test_filter_snak_mask_value_snak(self):
        kb = Store('sparql', WIKIDATA)
        kb.unset_flags(kb.BEST_RANK)
        stmt = next(kb.filter(
            wd.Adam, wd.date_of_death, snak_mask=SnakMask.VALUE_SNAK))
        self.assert_statement(
            stmt, wd.Adam, wd.date_of_death(
                Time('3073-01-01', 9, 0, wd.proleptic_Julian_calendar)))
        kb.set_flags(kb.BEST_RANK)
        it = kb.filter(
            wd.Adam, wd.date_of_death, snak_mask=SnakMask.VALUE_SNAK)
        self.assertRaises(StopIteration, next, it)

    def test_filter_snak_mask_some_value_snak(self):
        kb = Store('sparql', WIKIDATA)
        kb.unset_flags(kb.BEST_RANK)
        stmt = next(kb.filter(
            wd.Adam, wd.date_of_death, snak_mask=SnakMask.SOME_VALUE_SNAK))
        self.assert_statement(
            stmt, wd.Adam, SomeValueSnak(wd.date_of_death))

    def test_filter_snak_mask_no_value_snak(self):
        kb = Store('sparql', WIKIDATA)
        stmt = next(kb.filter(
            wd.Adam, wd.date_of_birth, snak_mask=SnakMask.NO_VALUE_SNAK))
        self.assert_statement(
            stmt, wd.Adam, NoValueSnak(wd.date_of_birth))

    def test_filter_store_flag_early_late_filter(self):
        kb = Store('sparql', WIKIDATA)
        kb.unset_flags(kb.EARLY_FILTER | kb.BEST_RANK)
        res = list(kb.filter(
            wd.Adam, wd.date_of_death, None, SnakMask.SOME_VALUE_SNAK))
        self.assertEqual(
            res, [Statement(wd.Adam, SomeValueSnak(wd.date_of_death))])
        kb.unset_flags(kb.LATE_FILTER)
        res = sorted(list(kb.filter(
            wd.Adam, wd.date_of_death, None, SnakMask.SOME_VALUE_SNAK)))
        self.assertEqual(len(res), 2)
        self.assert_statement(
            res[0], wd.Adam, SomeValueSnak(wd.date_of_death))
        self.assert_statement(
            res[1], wd.Adam, wd.date_of_death(Time('3073-01-01')))


if __name__ == '__main__':
    main()
