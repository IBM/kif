# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Preferred, Quantity, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_unannotated(self) -> None:
        c = self.store_contains_assertion(self.KB())
        c(True, wd.label(wd.Adam, 'Adam'))
        c(False, wd.label(wd.Adam, 'Adamx'))
        c(True, wd.alias(wd.Adam, Text('Adánico', 'es')))
        c(False, wd.alias(wd.Adam, Text('Adánico', 'en')))
        c(True, wd.description(wd.Adam, Text(
            'figura bíblica do livro de Gênesis', 'pt')))
        c(False, wd.description(wd.Adam, Text(
            'figura bíblica do livro de Gênesis', 'en')))
        c(True, wd.date_of_birth.no_value(wd.Adam))
        c(False, wd.date_of_birth.some_value(wd.Adam))
        c(True, wd.family_name.some_value(wd.Adam))
        c(False, wd.family_name.no_value(wd.Adam))
        c(True, wd.instance_of(
            wd.InChIKey, wd.Wikidata_property_to_identify_substances))
        c(False, wd.instance_of(wd.InChIKey, wd.type_of_a_chemical_entity))
        c(True, wd.mass(wd.benzene, Quantity('78.046950192', wd.dalton)))
        c(False, wd.mass(wd.benzene, Quantity('78.046950192')))
        c(True, wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89')))
        c(False, wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre)))
        c(False, wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.88', '.89')))
        c(True, wd.official_name(wd.Brazil, Text(
            'República Federativa do Brasil', 'pt')))
        c(False, wd.official_name(wd.Argentina, Text(
            'República Federativa do Brasil', 'pt')))
        c(True, wd.related_property(wd.InChIKey, wd.InChI))
        c(False, wd.related_property(wd.InChI, wd.InChIKey))

    def test_annotated(self) -> None:
        c = self.store_contains_assertion(self.KB())
        c(True, wd.label(wd.Adam, 'Adam').annotate())
        c(False, wd.label(wd.Adam, 'Adamx').annotate())
        c(True, wd.alias(wd.Adam, Text('Adánico', 'es')).annotate())
        c(False, wd.alias(wd.Adam, Text('Adánico', 'en')).annotate())
        c(True, wd.description(wd.Adam, Text(
            'figura bíblica do livro de Gênesis', 'pt')).annotate())
        c(False, wd.description(wd.Adam, Text(
            'figura bíblica do livro de Gênesis', 'en')).annotate())
        c(True, wd.date_of_birth.no_value(wd.Adam).annotate(
            references=[[
                wd.reference_URL('http://islamqa.info/ar/20907')]],
            rank=Preferred))
        c(False, wd.date_of_birth.some_value(wd.Adam).annotate())
        c(True, wd.family_name.some_value(wd.Adam).annotate())
        c(False, wd.family_name.no_value(wd.Adam).annotate())
        c(True, wd.instance_of(
            wd.InChIKey, wd.Wikidata_property_to_identify_substances
        ).annotate())
        c(False, wd.instance_of(
            wd.InChIKey, wd.type_of_a_chemical_entity).annotate())
        c(True, wd.mass(
            wd.benzene, Quantity('78.046950192', wd.dalton)).annotate(
                references=[[
                    wd.title('benzene'),
                    wd.stated_in(wd.PubChem),
                    wd.language_of_work_or_name(wd.English),
                    wd.PubChem_CID('241'),
                    wd.retrieved(Time('2016-10-19', Time.DAY, 0,
                                      wd.proleptic_Gregorian_calendar))]]))
        c(False, wd.mass(
            wd.benzene, Quantity('78.046950192')).annotate(
                references=[[
                    wd.title('benzene'),
                    wd.stated_in(wd.PubChem),
                    wd.language_of_work_or_name(wd.English),
                    wd.PubChem_CID('241'),
                    wd.retrieved(Time('2016-10-19', Time.DAY, 0,
                                      wd.proleptic_Gregorian_calendar))]]))
        c(True, wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, '.87', '.89')).annotate(
                qualifiers=[
                    wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
                    wd.phase_of_matter(wd.liquid)],
                references=[[
                    wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                    wd.stated_in(wd.Q(5687720))]]))
        c(False, wd.density(wd.benzene, Quantity(
            '.88', wd.gram_per_cubic_centimetre, None, '.89')).annotate(
                qualifiers=[
                    wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
                    wd.phase_of_matter(wd.liquid)],
                references=[[
                    wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                    wd.stated_in(wd.Q(5687720))]]))
        c(True, wd.official_name(wd.Brazil, Text(
            'República Federativa do Brasil', 'pt')).annotate())
        c(False, wd.official_name(wd.Argentina, Text(
            'República Federativa do Brasil', 'pt')).annotate())
        c(True, wd.related_property(wd.InChIKey, wd.InChI).annotate())
        c(False, wd.related_property(wd.InChI, wd.InChIKey).annotate())


if __name__ == '__main__':
    Test.main()
