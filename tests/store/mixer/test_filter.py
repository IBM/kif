# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Deprecated, Preferred, Quantity, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S('mixer', [
            cls.S('wikidata-rdf', 'tests/data/adam.ttl'),
            cls.S('empty'),
            cls.S('wikidata-rdf', 'tests/data/instance_of.ttl'),
            cls.S('empty'),
            cls.S('wikidata-rdf', graph=[
                wd.inverse_property.no_value(wd.instance_of, rank=Deprecated),
            ]),
            cls.S('empty'),
            cls.S('wikidata-rdf', graph=[
                wd.label(wd.benzene, 'benzene'),
                wd.mass(
                    wd.benzene, Quantity('78.046950192', wd.dalton),
                    references=[[
                        wd.title('benzene'),
                        wd.stated_in(wd.PubChem),
                        wd.language_of_work_or_name(wd.English),
                        wd.PubChem_CID('241'),
                        wd.retrieved(Time(
                            '2016-10-19', Time.DAY, 0,
                            wd.proleptic_Gregorian_calendar))]]),
                wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N'),
                wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity)]),
            cls.S('wikidata-rdf', graph=[
                wd.density.some_value(wd.benzene, rank=Deprecated)])])

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        f, F = self.store_filter_assertion(self.KB())
        f(F(),
          {wd.father.no_value(wd.Adam),
           wd.label(wd.Adam, 'Adam'),
           wd.label(wd.Adam, Text('Adán', 'es')),
           wd.label(wd.Adam, Text('Adão', 'pt')),
           wd.alias(wd.Adam, Text('Adam', 'es')),
           wd.alias(wd.Adam, Text('Adánico', 'es')),
           wd.alias(wd.Adam, Text('Adanico', 'es')),
           wd.alias(wd.Adam, Text('Adan', 'es')),
           wd.description(wd.Adam, Text(
               'first man according to the Abrahamic creation '
               'and religions such as Judaism, Christianity, and Islam')),
           wd.description(wd.Adam, Text(
               'primer hombre, según la Biblia', 'es')),
           wd.description(wd.Adam, Text(
               'figura bíblica do livro de Gênesis', 'pt')),
           wd.family_name.some_value(wd.Adam),
           wd.date_of_birth.no_value(wd.Adam),
           wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
           wd.alias(wd.instance_of, 'type'),
           wd.alias(wd.instance_of, 'is of type'),
           wd.alias(wd.instance_of, 'has type'),
           wd.alias(wd.instance_of, 'is a'),
           wd.label(wd.instance_of, 'instance of'),
           wd.description(wd.instance_of, Text(
               'that class of which this subject is a '
               'particular example and member; different '
               'from P279 (subclass of); for example: K2 '
               'is an instance of mountain; volcano is a '
               'subclass of mountain (and an instance of '
               'volcanic landform)')),
           wd.label(wd.benzene, 'benzene'),
           wd.inverse_property.no_value(wd.instance_of),
           wd.InChIKey(wd.benzene, 'UHOVQNZJYSORNB-UHFFFAOYSA-N'),
           wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)),
           wd.density.some_value(wd.benzene)})

    # -- masks --

    def test_snak_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SOME_VALUE_SNAK),
           {wd.density.some_value(wd.benzene, rank=Deprecated),
            wd.family_name.some_value(wd.Adam)})
        xf(F(snak_mask=F.NO_VALUE_SNAK),
           {wd.father.no_value(wd.Adam),
            wd.date_of_birth.no_value(wd.Adam, rank=Preferred, references=[[
                wd.reference_URL('http://islamqa.info/ar/20907'),
            ]]),
            wd.inverse_property.no_value(wd.instance_of, rank=Deprecated)})

    def test_subject_mask(self) -> None:
        raise self.TODO()

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        raise self.TODO()

    def test_language(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(property=wd.alias, language='es'),
           {wd.alias(wd.Adam, Text('Adam', 'es')),
            wd.alias(wd.Adam, Text('Adánico', 'es')),
            wd.alias(wd.Adam, Text('Adan', 'es')),
            wd.alias(wd.Adam, Text('Adanico', 'es'))})

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        raise self.TODO()

    def test_value_fp_property(self) -> None:
        raise self.TODO()

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        raise self.TODO()

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        raise self.TODO()

    def test_value_fp_quantity(self) -> None:
        raise self.TODO()

    def test_value_fp_time(self):
        raise self.TODO()

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        raise self.TODO()

    def test_snak_fp_property(self) -> None:
        raise self.TODO()

    def test_snak_fp_value(self) -> None:
        raise self.TODO()

    def test_or_fp_subject_property(self) -> None:
        raise self.TODO()

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

    def test_extra_references(self) -> None:
        ##
        # Make sure `extra_references` are preserved.
        ##
        child = self.S('wikidata-rdf', 'tests/data/benzene.ttl')
        child.set_extra_references([[wd.stated_in(wd.Wikidata)]])
        stmt = next(child.filter_annotated())
        self.assertTrue(stmt.references.issuperset(child.extra_references))
        mixer1 = self.S('mixer', [child])
        stmt = next(mixer1.filter_annotated())
        self.assertTrue(stmt.references.issuperset(child.extra_references))
        mixer2 = self.S('mixer', [mixer1])
        stmt = next(mixer2.filter_annotated())
        self.assertTrue(stmt.references.issuperset(child.extra_references))


if __name__ == '__main__':
    Test.main()
