# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Preferred, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        import os
        wdqs = os.getenv('WIKIDATA', os.getenv('WDQS'))
        if not wdqs:
            raise cls.SKIP('WIKIDATA is not set')
        else:
            return cls.S('wdqs', wdqs)

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    # -- masks --

    def test_snak_mask(self) -> None:
        kb = self.KB()
        kb.unset_flags(kb.BEST_RANK)
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Adam,
             property=wd.date_of_birth,
             snak_mask=F.VALUE_SNAK),
           {wd.date_of_birth(
               wd.Adam, Time(
                   '4003-01-01', Time.YEAR, 0,
                   wd.proleptic_Julian_calendar),
               qualifiers=[wd.statement_supported_by(wd.Q(746069))],
               references=[[wd.reference_URL(
                   'https://amazingbibletimeline.com/timeline_online/')]])})
        xf(F(subject=wd.Adam, snak_mask=F.SOME_VALUE_SNAK | F.NO_VALUE_SNAK),
           {wd.date_of_birth.some_value(
               wd.Adam, references=[[
                   wd.reference_URL('http://islamqa.info/ar/20907')]],
               rank=Preferred),
            wd.date_of_death.some_value(
                wd.Adam, references=[[
                    wd.reference_URL('http://islamqa.info/ar/20907')]],
                rank=Preferred),
            wd.family_name.some_value(wd.Adam),
            wd.family_name.no_value(wd.Adam),
            wd.father.no_value(wd.Adam),
            wd.mother.no_value(wd.Adam),
            wd.name_in_native_language.some_value(
                wd.Adam, qualifiers=[
                    wd.statement_is_subject_of(wd.Q(351633))])})

    def test_subject_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value=wd.InChIKey, subject_mask=F.PROPERTY),
           {wd.related_property(wd.InChI, wd.InChIKey)})

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.Brazil, value_mask=F.IRI, snak_mask=F.VALUE_SNAK),
           {wd.Mastodon_instance_URL(
               wd.Brazil, 'https://masto.donte.com.br'),
            wd.Mastodon_instance_URL(
                wd.Brazil, 'https://mastodon.com.br', references=[[
                    wd.title(Text('Explorar - Mastodon Brasil', 'pt-br')),
                    wd.retrieved(Time(
                        '2023-06-20', Time.DAY, 0,
                        wd.proleptic_Gregorian_calendar)),
                    wd.reference_URL('https://mastodon.com.br/explore')]]),
            wd.external_data_available_at_URL(
                wd.Brazil, 'http://dados.gov.br'),
            wd.official_website(
                wd.Brazil, 'https://www.gov.br', qualifiers=[
                    wd.language_of_work_or_name(wd.Brazilian_Portuguese)]),
            wd.described_at_URL(
                wd.Brazil,
                'https://www.cia.gov/library/publications/'
                'resources/the-world-factbook/geos/br.html',
                qualifiers=[
                    wd.language_of_work_or_name(wd.English),
                    wd.retrieved(Time(
                        '2020-07-11', Time.DAY, 0,
                        wd.proleptic_Gregorian_calendar))])})

    def test_language(self) -> None:
        kb = self.KB()
        kb.unset_flags(kb.BEST_RANK)
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Brazil, property=wd.official_name,
           snak_mask=F.VALUE_SNAK, value_mask=F.TEXT, language='fr'),
           {wd.official_name(
               wd.Brazil, Text('République fédérative du Brésil', 'fr'),
               references=[[
                   wd.reference_URL('http://cnig.gouv.fr/wp-content/'
                                    'uploads/2020/02/CNT-PVM_r%C3%A9vis'
                                    '%C3%A9_2020-01-27-1.pdf')]])})

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        kb = self.KB()
        kb.page_size = 2
        xf, F = self.store_xfilter_assertion(kb)
        s = wd.Ginga
        xf(F(subject=s, snak_mask=F.VALUE_SNAK, value_mask=F.ITEM),
           {wd.copyright_license(s, wd.GNU_General_Public_License),
            wd.copyright_status(s, wd.copyrighted),
            wd.country_of_origin(s, wd.Brazil),
            wd.different_from(s, wd.Q(1411420)),
            wd.instance_of(s, wd.system_software),
            wd.named_after(s, wd.Q(1411420)),
            wd.subclass_of(s, wd.middleware)})

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


if __name__ == '__main__':
    Test.main()
