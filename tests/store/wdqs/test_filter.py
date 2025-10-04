# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Preferred, Text, Time
from kif_lib.typing import Any
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls, **kwargs: Any):
        import os
        wdqs = os.getenv('WIKIDATA', os.getenv('WDQS'))
        if not wdqs:
            raise cls.SKIP('WIKIDATA is not set')
        else:
            return cls.S('wdqs', wdqs, **kwargs)

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    # -- masks --

    def test_snak_mask_value_snak(self) -> None:
        kb = self.KB()
        kb.best_ranked = False
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

    def test_snak_mask_some_value_snak(self) -> None:
        kb = self.KB()
        kb.best_ranked = False
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Adam, snak_mask=F.SOME_VALUE_SNAK),
           {wd.date_of_birth.some_value(
               wd.Adam, references=[[
                   wd.reference_URL('http://islamqa.info/ar/20907')]],
               rank=Preferred),
            wd.date_of_death.some_value(
                wd.Adam,
                qualifiers=[
                    wd.age_of_subject_at_event(930@wd.Q(24564698))],
                references=[[
                    wd.reference_URL('http://islamqa.info/ar/20907')]],
                rank=Preferred),
            wd.name_in_native_language.some_value(
                wd.Adam, qualifiers=[
                    wd.language_of_work_or_name(wd.Q(351633))])})

    def test_snak_mask_no_value_snak(self) -> None:
        kb = self.KB()
        kb.best_ranked = False
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Adam, snak_mask=F.NO_VALUE_SNAK),
           {wd.family_name.no_value(wd.Adam),
            wd.father.no_value(wd.Adam),
            wd.mother.no_value(wd.Adam)})

    def test_subject_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value=wd.InChIKey, subject_mask=F.PROPERTY),
           {wd.related_property(wd.InChI, wd.InChIKey)})

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(subject=wd.Brazil, value_mask=F.IRI, snak_mask=F.VALUE_SNAK),
           {wd.Lemmy_instance_URL(
               wd.Brazil, 'https://lemmy.eco.br/'),
            wd.Mastodon_instance_URL(
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
                        wd.proleptic_Gregorian_calendar))],
                references=[[
                    wd.archive_URL(
                        'https://web.archive.org/web/20150530030303/'
                        'https://www.cia.gov/library/publications/'
                        'resources/the-world-factbook/geos/br.html'),
                    wd.archive_date(
                        Time('2015-05-30', Time.DAY, 0,
                             wd.proleptic_Gregorian_calendar))]])})

    def test_language(self) -> None:
        kb = self.KB()
        kb.best_ranked = False
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Brazil, property=wd.official_name,
           snak_mask=F.VALUE_SNAK, value_mask=F.TEXT, language='fr'),
           {wd.official_name(
               wd.Brazil, Text('République fédérative du Brésil', 'fr'),
               references=[[
                   wd.reference_URL('http://cnig.gouv.fr/wp-content/'
                                    'uploads/2020/02/CNT-PVM_r%C3%A9vis'
                                    '%C3%A9_2020-01-27-1.pdf')]])})
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
