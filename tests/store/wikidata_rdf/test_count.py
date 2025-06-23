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
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        xc(0, F(snak_mask=F.SnakMask(0)))
        xc_s(0, F(snak_mask=F.SnakMask(0)))
        xc_p(0, F(snak_mask=F.SnakMask(0)))
        xc_v(0, F(snak_mask=F.SnakMask(0)))
        xc_sp(0, F(snak_mask=F.SnakMask(0)))
        xc_sv(0, F(snak_mask=F.SnakMask(0)))
        xc_pv(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        xc(43, F())
        xc_s(27, F())
        xc_p(21, F())
        xc_v(40, F())
        xc_sp(30, F())
        xc_sv(40, F())
        xc_pv(40, F())

    # -- masks --

    def test_snak_mask(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        # value
        xc(40, F(snak_mask=F.VALUE_SNAK))
        xc_s(25, F(snak_mask=F.VALUE_SNAK))
        xc_p(18, F(snak_mask=F.VALUE_SNAK))
        xc_v(40, F(snak_mask=F.VALUE_SNAK))
        xc_sp(27, F(snak_mask=F.VALUE_SNAK))
        xc_sv(40, F(snak_mask=F.VALUE_SNAK))
        xc_pv(40, F(snak_mask=F.VALUE_SNAK))
        # some value
        xc(1, F(snak_mask=F.SOME_VALUE_SNAK))
        # no value
        xc(2, F(snak_mask=F.NO_VALUE_SNAK))

    def test_subject_mask(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        xc(6, F(subject_mask=F.PROPERTY))
        xc_s(4, F(subject_mask=F.PROPERTY))
        xc_p(4, F(subject_mask=F.PROPERTY))
        xc_v(6, F(subject_mask=F.PROPERTY))
        xc_sp(4, F(subject_mask=F.PROPERTY))
        xc_sv(6, F(subject_mask=F.PROPERTY))
        xc_pv(6, F(subject_mask=F.PROPERTY))

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        xc(32, F(value_mask=F.TEXT))
        xc(0, F(value_mask=F.IRI, snak_mask=F.VALUE_SNAK))
        xc_s(18, F(value_mask=F.TEXT))
        xc_p(11, F(value_mask=F.TEXT))
        xc_v(29, F(value_mask=F.TEXT))
        xc_sp(19, F(value_mask=F.TEXT))
        xc_sv(29, F(value_mask=F.TEXT))
        xc_pv(29, F(value_mask=F.TEXT))

    def test_language(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        f = F(value_mask=F.TEXT, language='pt', snak_mask=F.VALUE_SNAK)
        xc(8, f)
        xc_s(7, f)
        xc_p(5, f)
        xc_v(8, f)
        xc_sp(7, f)
        xc_sv(8, f)
        xc_pv(8, f)

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

    # -- and fp --

    def test_and_fp_subject(self) -> None:
        raise self.TODO()

    def test_and_fp_property(self) -> None:
        raise self.TODO()

    def test_and_fp_value(self) -> None:
        raise self.TODO()

    # -- or fp --

    def test_or_fp_subject(self) -> None:
        raise self.TODO()

    def test_or_fp_subject_property(self) -> None:
        xc, xc_s, xc_p, xc_v, xc_sp, xc_sv, xc_pv, F =\
            self.store_xcount_assertion_with_projection(self.KB())
        f = F(subject=wd.Brazil | wd.benzene, property=wd.label | wd.mass)
        xc(4, f)
        xc_s(3, f)
        xc_p(2, f)
        xc_v(4, f)
        xc_sp(3, f)
        xc_sv(4, f)
        xc_pv(4, f)

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
