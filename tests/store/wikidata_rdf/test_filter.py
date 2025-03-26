# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Quantity, Statement, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import TestCase


class Test(TestCase):

    KB = Store(
        'wikidata-rdf',
        'tests/data/adam.ttl',
        'tests/data/andar.ttl',
        'tests/data/benzene.ttl',
        'tests/data/brazil.ttl',
    )

    def test_empty(self) -> None:
        self.assertEqual(
            set(self.KB.filter(snak_mask=Filter.SnakMask(0))), set())

    def test_full(self) -> None:
        kb = Store('rdf', 'tests/data/andar.ttl')
        self.assertEqual(
            set(kb.filter()),
            {wd.lemma(wd.L(46803), Text('andar', 'pt')),
             wd.language(wd.L(46803), wd.Portuguese),
             wd.lexical_category(wd.L(46803), wd.verb)})

    # -- masks --

    def test_snak_mask(self) -> None:
        kb = Store('rdf', 'tests/data/adam.ttl')
        kb.unset_flags(kb.BEST_RANK)
        self.assertEqual(
            set(kb.filter(snak_mask=Filter.VALUE_SNAK)),
            {wd.alias(wd.Adam, Text('Adam', 'es')),
             wd.alias(wd.Adam, Text('Adan', 'es')),
             wd.alias(wd.Adam, Text('Adanico', 'es')),
             wd.alias(wd.Adam, Text('Adánico', 'es')),
             wd.date_of_birth(wd.Adam, Time(
                 '4003-01-01', Time.YEAR, 0, wd.proleptic_Julian_calendar)),
             wd.description(wd.Adam, 'first man according to the Abrahamic '
                            'creation and religions such as Judaism, '
                            'Christianity, and Islam'),
             wd.description(wd.Adam, Text(
                 'figura bíblica do livro de Gênesis', 'pt-br')),
             wd.description(wd.Adam, Text(
                 'primer hombre, según la Biblia', 'es')),
             wd.label(wd.Adam, 'Adam'),
             wd.label(wd.Adam, Text('Adán', 'es')),
             wd.label(wd.Adam, Text('Adão', 'pt-br'))})
        self.assertEqual(
            set(kb.filter(
                snak_mask=Filter.SOME_VALUE_SNAK | Filter.NO_VALUE_SNAK)),
            {Statement(wd.Adam, wd.date_of_birth.no_value()),
             Statement(wd.Adam, wd.family_name.some_value()),
             Statement(wd.Adam, wd.father.no_value())})

    def test_subject_mask(self) -> None:
        self.assertEqual(
            set(self.KB.filter(subject_mask=Filter.PROPERTY)),
            {wd.description(wd.InChIKey, 'A hashed version of the full '
                            'standard InChI - designed to create an '
                            'identifier that encodes structural '
                            'information and can also be practically '
                            'used in web searching.'),
             wd.description(wd.InChIKey, Text(
                 'código condensado para la identificación '
                 'de un compuesto químico', 'es')),
             wd.instance_of(
                 wd.InChIKey, wd.Wikidata_property_to_identify_substances),
             wd.label(wd.InChIKey, 'InChIKey'),
             wd.label(wd.InChIKey, Text('InChIKey', 'es')),
             wd.related_property(wd.InChIKey, wd.InChI)})

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        self.assertEqual(
            set(self.KB.filter(value_mask=Filter.TIME)),
            {Statement(wd.Adam, wd.date_of_birth.no_value()),
             Statement(wd.Adam, wd.family_name.some_value()),
             Statement(wd.Adam, wd.father.no_value()),
             wd.inception(wd.Brazil, Time(
                 '1822-09-07', Time.DAY, 0,
                 wd.proleptic_Gregorian_calendar))})

    def test_language(self) -> None:
        self.assertEqual(
            set(self.KB.filter(
                snak_mask=Filter.VALUE_SNAK,
                value_mask=Filter.TEXT,
                language='pt')),
            {wd.lemma(wd.L(46803), Text('andar', 'pt')),
             wd.official_name(wd.Brazil, Text(
                 'República Federativa do Brasil', 'pt'))})

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        self.assertEqual(
            set(self.KB.filter(subject=wd.benzene)),
            {wd.alias(wd.benzene, 'benzol'),
             wd.density(wd.benzene, Quantity(
                 '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
             wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N'),
             wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
             wd.label(wd.benzene, 'benzene'),
             wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))})

    def test_value_fp_property(self) -> None:
        self.assertEqual(
            set(self.KB.filter(property=wd.mass)),
            {wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))})

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        self.assertEqual(
            set(self.KB.filter(value=Text('Brazil', 'en'))),
            {wd.label(wd.Brazil, 'Brazil')})
        self.assertEqual(
            set(self.KB.filter(value=Text('Brazil', 'es'))),
            set())

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        raise self.TODO()

    def test_value_fp_quantity(self) -> None:
        stmt = wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))
        self.assertEqual(
            set(self.KB.filter(value=Quantity('.88'))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Quantity(
                '.88', wd.gram_per_cubic_centimetre))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Quantity('.88', wd.kilogram))),
            set())
        self.assertEqual(
            set(self.KB.filter(value=Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87'))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Quantity('.88', None, '.88'))),
            set())
        self.assertEqual(
            set(self.KB.filter(value=Quantity(
                '.88', wd.gram_per_cubic_centimetre, None, '.89'))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Quantity('.88', None, None, '.88'))),
            set())

    def test_value_fp_time(self):
        stmt = wd.inception(wd.Brazil, Time(
            '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar))
        self.assertEqual(
            set(self.KB.filter(value=Time('1822-09-07'))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Time('1822-09-07', Time.DAY))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Time('1822-09-07', Time.YEAR))),
            set())
        self.assertEqual(
            set(self.KB.filter(value=Time('1822-09-07', Time.DAY, 0))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Time('1822-09-07', None, 8))),
            set())
        self.assertEqual(
            set(self.KB.filter(value=Time(
                '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar))),
            {stmt})
        self.assertEqual(
            set(self.KB.filter(value=Time(
                '1822-09-07', None, None, wd.proleptic_Julian_calendar))),
            set())

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        self.assertEqual(
            set(self.KB.filter(
                subject=wd.instance_of(wd.type_of_a_chemical_entity),
                property=wd.mass)),
            {wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))})
        self.assertEqual(
            set(self.KB.filter(
                subject=wd.instance_of(
                    wd.Wikidata_property_to_identify_substances),
                property=wd.label)),
            {wd.label(wd.InChIKey, 'InChIKey'),
             wd.label(wd.InChIKey, Text('InChIKey', 'es'))})

    def test_snak_fp_property(self) -> None:
        self.assertEqual(
            set(self.KB.filter(
                subject=wd.benzene,
                property=wd.instance_of(
                    wd.Wikidata_property_to_identify_substances))),
            {wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N')})

    def test_snak_fp_value(self) -> None:
        self.assertEqual(
            set(self.KB.filter(
                subject=wd.Brazil,
                value=wd.demonym(Text('Latinoamericana', 'es')))),
            {wd.part_of(wd.Brazil, wd.Latin_America)})

    def test_or_fp_subject_property(self) -> None:
        self.assertEqual(
            set(self.KB.filter(
                subject=wd.Brazil | wd.benzene,
                property=wd.label | wd.mass)),
            {wd.label(wd.benzene, 'benzene'),
             wd.label(wd.Brazil, 'Brazil'),
             wd.label(wd.Brazil, Text('Brasil', 'pt-br')),
             wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton))})

    def test_and_fp_subject(self) -> None:
        raise self.TODO()

    def test_and_fp_property(self) -> None:
        raise self.TODO()

    def test_and_fp_value(self) -> None:
        raise self.TODO()

    def test_or_fp_subject(self) -> None:
        raise self.TODO()

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
