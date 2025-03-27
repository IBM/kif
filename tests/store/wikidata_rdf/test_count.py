# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Quantity, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S(
            'wikidata-rdf',
            'tests/data/adam.ttl',
            'tests/data/andar.ttl',
            'tests/data/benzene.ttl',
            'tests/data/brazil.ttl'
        )

    def test_empty(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(43, F())

    # -- masks --

    def test_snak_mask(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(40, F(snak_mask=F.VALUE_SNAK))
        c(1, F(snak_mask=F.SOME_VALUE_SNAK))
        c(2, F(snak_mask=F.NO_VALUE_SNAK))

    def test_subject_mask(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(6, F(subject_mask=F.PROPERTY))

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(32, F(value_mask=F.TEXT))
        c(0, F(value_mask=F.IRI, snak_mask=F.VALUE_SNAK))

    def test_language(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(2, F(value_mask=F.TEXT, language='pt', snak_mask=F.VALUE_SNAK))

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(10, F(subject=wd.Brazil))
        c(6, F(subject=wd.InChIKey))
        c(3, F(subject=wd.L(46803)))

    def test_value_fp_property(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(2, F(subject=wd.Brazil, property=wd.label))
        c(1, F(subject=wd.benzene, property=wd.mass))

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(value=Text('Brazil', 'en')))

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(value=ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')))

    def test_value_fp_quantity(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(subject=wd.benzene, property=wd.mass, value=Quantity(
            '78.046950192')))
        c(1, F(property=wd.mass, value=Quantity('78.046950192')))
        c(1, F(value=Quantity('78.046950192')))
        c(1, F(value=Quantity('78.046950192', wd.dalton)))
        c(0, F(value=Quantity('78.046950192', wd.kilogram)))
        c(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre)))
        c(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87')))
        c(0, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.88')))
        c(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, None, '.89')))
        c(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89')))

    def test_value_fp_time(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(value=Time('1822-09-07')))
        c(0, F(value=Time('1822-09-08')))
        c(1, F(property=wd.inception, value=Time('1822-09-07')))
        c(1, F(value=Time('1822-09-07', Time.DAY)))
        c(0, F(value=Time('1822-09-07', Time.YEAR)))
        c(1, F(value=Time('1822-09-07', None, 0)))
        c(0, F(value=Time('1822-09-07', None, 9)))
        c(1, F(value=Time(
            '1822-09-07', None, None, wd.proleptic_Gregorian_calendar)))
        c(0, F(value=Time(
            '1822-09-07', None, None, wd.proleptic_Julian_calendar)))
        c(1, F(value=Time(
            '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)))

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(subject=wd.instance_of(wd.type_of_a_chemical_entity),
               property=wd.density))

    def test_snak_fp_property(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(subject=wd.benzene, property=wd.related_property(wd.InChI)))

    def test_snak_fp_value(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(1, F(subject=wd.Brazil,
               value=wd.demonym(Text('Latinoamericana', 'es'))))

    def test_and_fp_subject(self) -> None:
        raise self.TODO()

    def test_and_fp_property(self) -> None:
        raise self.TODO()

    def test_and_fp_value(self) -> None:
        raise self.TODO()

    def test_or_fp_subject(self) -> None:
        raise self.TODO()

    def test_or_fp_subject_property(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(4, F(subject=wd.Brazil | wd.benzene, property=wd.label | wd.mass))

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
