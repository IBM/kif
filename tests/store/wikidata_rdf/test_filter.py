# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Graph, Preferred, Quantity, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        return cls.S(
            'wikidata-rdf',
            'tests/data/adam.ttl',
            'tests/data/andar.ttl',
            'tests/data/benzene.ttl',
            'tests/data/brazil.ttl')

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        xf, F = self.store_xfilter_assertion(
            self.S('rdf', 'tests/data/andar.ttl'))
        xf(F(),
           {wd.lemma(wd.L(46803), Text('andar', 'pt')),
            wd.language(wd.L(46803), wd.Portuguese),
            wd.lexical_category(wd.L(46803), wd.verb)})

    # -- masks --

    def test_snak_mask(self) -> None:
        kb = self.S('rdf', 'tests/data/adam.ttl')
        kb.best_ranked = False
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(snak_mask=F.VALUE_SNAK),
           {wd.alias(wd.Adam, Text('Adam', 'es')),
            wd.alias(wd.Adam, Text('Adan', 'es')),
            wd.alias(wd.Adam, Text('Adanico', 'es')),
            wd.alias(wd.Adam, Text('Adánico', 'es')),
            wd.date_of_birth(
                wd.Adam, Time(
                    '4003-01-01', Time.YEAR, 0,
                    wd.proleptic_Julian_calendar),
                qualifiers=[wd.statement_supported_by(wd.Q(746069))],
                references=[[wd.reference_URL(
                    'https://amazingbibletimeline.com/timeline_online/')]]),
            wd.description(wd.Adam, 'first man according to the Abrahamic '
                           'creation and religions such as Judaism, '
                           'Christianity, and Islam'),
            wd.description(wd.Adam, Text(
                'figura bíblica do livro de Gênesis', 'pt')),
            wd.description(wd.Adam, Text(
                'primer hombre, según la Biblia', 'es')),
            wd.label(wd.Adam, 'Adam'),
            wd.label(wd.Adam, Text('Adán', 'es')),
            wd.label(wd.Adam, Text('Adão', 'pt'))})
        xf(F(snak_mask=F.SOME_VALUE_SNAK | F.NO_VALUE_SNAK),
           {wd.date_of_birth.no_value(
               wd.Adam, references=[[
                   wd.reference_URL('http://islamqa.info/ar/20907')]],
               rank=Preferred),
            wd.family_name.some_value(wd.Adam),
            wd.father.no_value(wd.Adam)})

    def test_subject_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject_mask=F.PROPERTY),
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
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value_mask=F.TIME),
           {wd.date_of_birth.no_value(
               wd.Adam, references=[[
                   wd.reference_URL('http://islamqa.info/ar/20907')]],
               rank=Preferred),
            wd.family_name.some_value(wd.Adam),
            wd.father.no_value(wd.Adam),
            wd.inception(wd.Brazil, Time(
                '1822-09-07', Time.DAY, 0,
                wd.proleptic_Gregorian_calendar))})

    def test_language(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.VALUE_SNAK, value_mask=F.TEXT, language='pt'),
           {wd.lemma(wd.L(46803), Text('andar', 'pt')),
            wd.label(wd.Adam, Text('Adão', 'pt')),
            wd.description(wd.Adam, Text(
                'figura bíblica do livro de Gênesis', 'pt')),
            wd.description(wd.Brazil, Text(
                'país na América do Sul', 'pt')),
            wd.label(wd.Brazil, Text('Brasil', 'pt')),
            wd.alias(wd.Brazil, Text('🇧🇷', 'pt')),
            wd.alias(wd.Brazil, Text('pindorama', 'pt')),
            wd.official_name(wd.Brazil, Text(
                'República Federativa do Brasil', 'pt'))})

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.benzene),
           {wd.alias(wd.benzene, 'benzol'),
            wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
            wd.density(
                wd.benzene, Quantity(
                    '.88', wd.gram_per_cubic_centimetre, '.87', '.89'),
                qualifiers=[
                    wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
                    wd.phase_of_matter(wd.liquid)],
                references=[[
                    wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                    wd.stated_in(wd.Q(5687720))]]),
            wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N'),
            wd.label(wd.benzene, 'benzene'),
            wd.mass(
                wd.benzene, Quantity('78.046950192', wd.dalton),
                references=[[
                    wd.title('benzene'),
                    wd.stated_in(wd.PubChem),
                    wd.language_of_work_or_name(wd.English),
                    wd.PubChem_CID('241'),
                    wd.retrieved(Time('2016-10-19', Time.DAY, 0,
                                      wd.proleptic_Gregorian_calendar))]])})

    def test_value_fp_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(property=wd.mass),
           {wd.mass(
               wd.benzene, Quantity('78.046950192', wd.dalton),
               references=[[
                   wd.title('benzene'),
                   wd.stated_in(wd.PubChem),
                   wd.language_of_work_or_name(wd.English),
                   wd.PubChem_CID('241'),
                   wd.retrieved(Time('2016-10-19', Time.DAY, 0,
                                     wd.proleptic_Gregorian_calendar))]])})

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value=Text('Brazil', 'en')),
           {wd.label(wd.Brazil, 'Brazil')})
        xf(F(value=Text('Brazil', 'es')), ())

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value=ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')),
           {wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N')})

    def test_value_fp_quantity(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        stmt = wd.density(
            wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89'),
            qualifiers=[
                wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
                wd.phase_of_matter(wd.liquid)],
            references=[[
                wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                wd.stated_in(wd.Q(5687720))]])
        xf(F(value=Quantity('.88')), {stmt})
        xf(F(value=Quantity('.88', wd.gram_per_cubic_centimetre)), {stmt})
        xf(F(value=Quantity('.88', wd.kilogram)), ())
        xf(F(value=Quantity('.88', wd.gram_per_cubic_centimetre, '.87')),
           {stmt})
        xf(F(value=Quantity('.88', None, '.88')), ())
        xf(F(value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, None, '.89')), {stmt})
        xf(F(value=Quantity('.88', None, None, '.88')), ())

    def test_value_fp_time(self):
        xf, F = self.store_xfilter_assertion(self.KB())
        stmt = wd.inception(wd.Brazil, Time(
            '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar))
        xf(F(value=Time('1822-09-07')), {stmt})
        xf(F(value=Time('1822-09-07', Time.DAY)), {stmt})
        xf(F(value=Time('1822-09-07', Time.YEAR)), ())
        xf(F(value=Time('1822-09-07', Time.DAY, 0)), {stmt})
        xf(F(value=Time('1822-09-07', None, 8)), ())
        xf(F(value=Time('1822-09-07', Time.DAY, 0,
                        wd.proleptic_Gregorian_calendar)), {stmt})
        xf(F(value=Time('1822-09-07', None, None,
                        wd.proleptic_Julian_calendar)), ())

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.instance_of(wd.type_of_a_chemical_entity),
             property=wd.mass),
           {wd.mass(
               wd.benzene, Quantity('78.046950192', wd.dalton),
               references=[[
                   wd.title('benzene'),
                   wd.stated_in(wd.PubChem),
                   wd.language_of_work_or_name(wd.English),
                   wd.PubChem_CID('241'),
                   wd.retrieved(Time('2016-10-19', Time.DAY, 0,
                                     wd.proleptic_Gregorian_calendar))]])})
        xf(F(subject=wd.instance_of(
            wd.Wikidata_property_to_identify_substances),
            property=wd.label),
           {wd.label(wd.InChIKey, 'InChIKey'),
            wd.label(wd.InChIKey, Text('InChIKey', 'es'))})

    def test_snak_fp_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.benzene,
             property=wd.instance_of(
                 wd.Wikidata_property_to_identify_substances)),
           {wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N')})

    def test_snak_fp_value(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.Brazil,
             value=wd.demonym(Text('Latinoamericana', 'es'))),
           {wd.part_of(wd.Brazil, wd.Latin_America)})

    def test_or_fp_subject_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.Brazil | wd.benzene,
             property=wd.label | wd.mass),
           {wd.label(wd.benzene, 'benzene'),
            wd.label(wd.Brazil, 'Brazil'),
            wd.label(wd.Brazil, Text('Brasil', 'pt')),
            wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton),
                    references=[[
                        wd.title('benzene'),
                        wd.stated_in(wd.PubChem),
                        wd.language_of_work_or_name(wd.English),
                        wd.PubChem_CID('241'),
                        wd.retrieved(Time(
                            '2016-10-19', Time.DAY, 0,
                            wd.proleptic_Gregorian_calendar))]])})

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

    # -- corner cases --

    def test_distinct(self) -> None:
        ###
        # Store.filter(limit=N, distinct=True) should only consider the
        # statements' (s,p,v) when applying the distinct modifier.  In the
        # example below, it should return exactly two "distinct" statements.
        #
        # - wd.mass(wd.benzene, 0)
        # - wd.density(wd.benzene, 0)
        #
        # Although there are multiple density statements, all of them
        # have the same (s,p,v).
        ###
        kb = self.S(
            'wikidata-rdf',
            wd.mass(wd.benzene, 0),
            *(wd.density(wd.benzene, 0, qualifiers=[wd.temperature(i)])
              for i in range(10)))
        res = list(kb.filter(wd.benzene, distinct=True))
        self.assertEqual(len(res), 2)
        self.assertEqual(
            set(res), {wd.mass(wd.benzene, 0), wd.density(wd.benzene, 0)})
        self.assertEqual(
            set(kb.filter_annotated(wd.benzene, distinct=True)),
            {wd.mass(wd.benzene, 0).annotate(),
             *(wd.density(wd.benzene, 0, qualifiers=[wd.temperature(i)])
               for i in range(10))})
        ###
        # FIXME: Store.count() is still returning the wrong number of
        # statements.  The quick fix of using a blank node for wds does not
        # work for count queries even when COUNT(DISTINCT *) is used.  The
        # correct approach is to replace "*" by an explicit list of
        # variables, derived from the variables occurring in the target
        # patterns.
        ###
        self.assertEqual(kb.count(wd.benzene, wd.density), 10)

    def test_no_and_some_value_at_the_same_time(self) -> None:
        kb = self.S(
            'wikidata-rdf',
            wd.shares_border_with.some_value(wd.Brazil),
            wd.shares_border_with.no_value(wd.Brazil))
        self.assertEqual(
            set(kb.filter()),
            {wd.shares_border_with.some_value(wd.Brazil),
             wd.shares_border_with.no_value(wd.Brazil)})
        self.assertEqual(
            set(kb.filter_annotated()),
            {wd.shares_border_with.some_value(wd.Brazil).annotate(),
             wd.shares_border_with.no_value(wd.Brazil).annotate()})
        ###
        # In May 2025, we observed inconsistencies in WDQS, cases where the
        # same statement is assigned both "no-value" and "some-value".  This
        # was causing KIF return different results for Store.filter() and
        # Store.filter_annotated().  We're documenting this behavior here.
        # Right now there is no simple way to fix this on KIF's side.
        ###
        kb = self.S(
            'wikidata-rdf',
            data=Graph(
                wd.shares_border_with.some_value(wd.Brazil).annotate(),
                wd.shares_border_with.no_value(wd.Brazil).annotate()).to_rdf(
                    gen_wds=lambda x: 0))
        self.assertEqual(
            set(kb.filter()),
            {wd.shares_border_with.some_value(wd.Brazil),
             wd.shares_border_with.no_value(wd.Brazil)})
        ###
        # In the annotated case, the "no-value" is being interpreted as a
        # qualifier of the statement.  We could "fix" this case by filtering
        # the qualifier out since its property is the same as the
        # statement's main snak property.  But we think that the current
        # behavior is justifiable.
        ###
        self.assertEqual(
            set(kb.filter_annotated()),
            {wd.shares_border_with.some_value(wd.Brazil).annotate(
                qualifiers=[wd.shares_border_with.no_value()])})
        ###
        # A final sanity check: In the case where the main snak is a no
        # value and the statement is a qualified with the same snak than the
        # qualifier should be suppressed.
        ###
        kb = self.S(
            'wikidata-rdf',
            data=Graph(
                wd.shares_border_with.no_value(wd.Brazil).annotate(
                    qualifiers=[wd.shares_border_with.no_value()])).to_rdf())
        self.assertEqual(
            set(kb.filter_annotated()),
            {wd.shares_border_with.no_value(wd.Brazil).annotate()})


if __name__ == '__main__':
    Test.main()
