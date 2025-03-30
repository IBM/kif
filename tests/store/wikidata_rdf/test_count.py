# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Quantity, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_empty(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(43, F())

    # -- masks --

    def test_snak_mask(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(40, F(snak_mask=F.VALUE_SNAK))
        xc(1, F(snak_mask=F.SOME_VALUE_SNAK))
        xc(2, F(snak_mask=F.NO_VALUE_SNAK))

    def test_subject_mask(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(6, F(subject_mask=F.PROPERTY))

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(32, F(value_mask=F.TEXT))
        xc(0, F(value_mask=F.IRI, snak_mask=F.VALUE_SNAK))

    def test_language(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(2, F(value_mask=F.TEXT, language='pt', snak_mask=F.VALUE_SNAK))

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(10, F(subject=wd.Brazil))
        xc(6, F(subject=wd.InChIKey))
        xc(3, F(subject=wd.L(46803)))

    def test_value_fp_property(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(2, F(subject=wd.Brazil, property=wd.label))
        xc(1, F(subject=wd.benzene, property=wd.mass))

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(value=Text('Brazil', 'en')))

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(value=ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')))

    def test_value_fp_quantity(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(subject=wd.benzene, property=wd.mass, value=Quantity(
            '78.046950192')))
        xc(1, F(property=wd.mass, value=Quantity('78.046950192')))
        xc(1, F(value=Quantity('78.046950192')))
        xc(1, F(value=Quantity('78.046950192', wd.dalton)))
        xc(0, F(value=Quantity('78.046950192', wd.kilogram)))
        xc(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre)))
        xc(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87')))
        xc(0, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.88')))
        xc(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, None, '.89')))
        xc(1, F(property=wd.density, value=Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89')))

    def test_value_fp_time(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(value=Time('1822-09-07')))
        xc(0, F(value=Time('1822-09-08')))
        xc(1, F(property=wd.inception, value=Time('1822-09-07')))
        xc(1, F(value=Time('1822-09-07', Time.DAY)))
        xc(0, F(value=Time('1822-09-07', Time.YEAR)))
        xc(1, F(value=Time('1822-09-07', None, 0)))
        xc(0, F(value=Time('1822-09-07', None, 9)))
        xc(1, F(value=Time(
            '1822-09-07', None, None, wd.proleptic_Gregorian_calendar)))
        xc(0, F(value=Time(
            '1822-09-07', None, None, wd.proleptic_Julian_calendar)))
        xc(1, F(value=Time(
            '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)))

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(subject=wd.instance_of(wd.type_of_a_chemical_entity),
                property=wd.density))

    def test_snak_fp_property(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(subject=wd.benzene, property=wd.related_property(wd.InChI)))

    def test_snak_fp_value(self) -> None:
        xc, F = self.store_xcount_assertion(self.KB())
        xc(1, F(subject=wd.Brazil,
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
        xc, F = self.store_xcount_assertion(self.KB())
        xc(4, F(subject=wd.Brazil | wd.benzene, property=wd.label | wd.mass))

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
