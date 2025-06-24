# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Quantity, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_empty(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        c(0, F(snak_mask=F.SnakMask(0)))
        c_s(0, F(snak_mask=F.SnakMask(0)))
        c_p(0, F(snak_mask=F.SnakMask(0)))
        c_v(0, F(snak_mask=F.SnakMask(0)))
        c_sp(0, F(snak_mask=F.SnakMask(0)))
        c_sv(0, F(snak_mask=F.SnakMask(0)))
        c_pv(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        c(43, F())
        c_s(27, F())
        c_p(21, F())
        c_v(40, F())
        c_sp(30, F())
        c_sv(40, F())
        c_pv(40, F())

    # -- masks --

    def test_snak_mask(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        # value
        c(40, F(snak_mask=F.VALUE_SNAK))
        c_s(25, F(snak_mask=F.VALUE_SNAK))
        c_p(18, F(snak_mask=F.VALUE_SNAK))
        c_v(40, F(snak_mask=F.VALUE_SNAK))
        c_sp(27, F(snak_mask=F.VALUE_SNAK))
        c_sv(40, F(snak_mask=F.VALUE_SNAK))
        c_pv(40, F(snak_mask=F.VALUE_SNAK))
        # some value
        c(1, F(snak_mask=F.SOME_VALUE_SNAK))
        # no value
        c(2, F(snak_mask=F.NO_VALUE_SNAK))

    def test_subject_mask(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        c(6, F(subject_mask=F.PROPERTY))
        c_s(4, F(subject_mask=F.PROPERTY))
        c_p(4, F(subject_mask=F.PROPERTY))
        c_v(6, F(subject_mask=F.PROPERTY))
        c_sp(4, F(subject_mask=F.PROPERTY))
        c_sv(6, F(subject_mask=F.PROPERTY))
        c_pv(6, F(subject_mask=F.PROPERTY))

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        c(32, F(value_mask=F.TEXT))
        c(0, F(value_mask=F.IRI, snak_mask=F.VALUE_SNAK))
        c_s(18, F(value_mask=F.TEXT))
        c_p(11, F(value_mask=F.TEXT))
        c_v(29, F(value_mask=F.TEXT))
        c_sp(19, F(value_mask=F.TEXT))
        c_sv(29, F(value_mask=F.TEXT))
        c_pv(29, F(value_mask=F.TEXT))

    def test_language(self) -> None:
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        f = F(value_mask=F.TEXT, language='pt', snak_mask=F.VALUE_SNAK)
        c(8, f)
        c_s(7, f)
        c_p(5, f)
        c_v(8, f)
        c_sp(7, f)
        c_sv(8, f)
        c_pv(8, f)

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(10, F(subject=wd.Brazil))
        c(6, F(subject=wd.InChIKey))
        c(3, F(subject=wd.L(46803)))

    def test_value_fp_property(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(subject=wd.Brazil, property=wd.label))
        c(1, F(subject=wd.benzene, property=wd.mass))

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(value=Text('Brazil', 'en')))

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(value=ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')))

    def test_value_fp_quantity(self) -> None:
        c, F = self.store_count_assertion(self.KB())
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
        c, F = self.store_count_assertion(self.KB())
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
        c, F = self.store_count_assertion(self.KB())
        c(1, F(subject=wd.instance_of(wd.type_of_a_chemical_entity),
               property=wd.density))

    def test_snak_fp_property(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(subject=wd.benzene, property=wd.related_property(wd.InChI)))

    def test_snak_fp_value(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(subject=wd.Brazil,
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
        c, c_s, c_p, c_v, c_sp, c_sv, c_pv, F =\
            self.store_count_assertion_with_projection(self.KB())
        f = F(subject=wd.Brazil | wd.benzene, property=wd.label | wd.mass)
        c(4, f)
        c_s(3, f)
        c_p(2, f)
        c_v(4, f)
        c_sp(3, f)
        c_sv(4, f)
        c_pv(4, f)

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
