# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AnnotatedStatement,
    Filter,
    Preferred,
    Statement,
    Text,
    Time,
)
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
            'tests/data/brazil.ttl')

    def test_subject(self) -> None:
        kb = self.KB()
        kb.subject = wd.Brazil
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(property=wd.instance_of),
           {wd.instance_of(wd.Brazil, wd.country_)})

    def test_property(self) -> None:
        kb = self.KB()
        kb.property = wd.instance_of
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Brazil),
           {wd.instance_of(wd.Brazil, wd.country_)})

    def test_value(self) -> None:
        kb = self.KB()
        kb.value = wd.country_
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Brazil),
           {wd.instance_of(wd.Brazil, wd.country_)})

    def test_snak_mask(self) -> None:
        kb = self.KB()
        kb.snak_mask = Filter.NO_VALUE_SNAK
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(subject=wd.Adam),
           {wd.father.no_value(wd.Adam),
            wd.date_of_birth.no_value(
                wd.Adam, references=[[
                    wd.reference_URL('http://islamqa.info/ar/20907')]],
                rank=Preferred)})

    def test_subject_mask(self) -> None:
        kb = self.KB()
        kb.subject_mask = Filter.LEXEME
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(),
           {wd.lexical_category(wd.L(46803), wd.verb),
            wd.language(wd.L(46803), wd.Portuguese),
            wd.lemma(wd.L(46803), Text('andar', 'pt'))})

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        kb = self.KB()
        kb.value_mask = Filter.TIME
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(wd.Brazil), {wd.inception(wd.Brazil, Time(
            '1822-09-07', Time.DAY, 0,
            wd.proleptic_Gregorian_calendar))})

    def test_rank_mask(self) -> None:
        raise self.TODO()

    def test_language(self) -> None:
        kb = self.KB()
        kb.language = 'pt'
        kb.snak_mask = Filter.VALUE_SNAK
        kb.value_mask = Filter.TEXT
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(),
           {wd.lemma(wd.L(46803), Text('andar', 'pt')),
            wd.official_name(wd.Brazil, Text(
                'República Federativa do Brasil', 'pt'))})

    def test_annotated(self) -> None:
        kb = self.KB()
        kb.annotated = True
        self.assertIsInstance(next(kb.filter(wd.Brazil)), AnnotatedStatement)
        kb.annotated = False
        self.assertIsInstance(next(kb.filter(wd.Brazil)), Statement)
        self.assertIsInstance(
            next(kb.filter(wd.Brazil, annotated=True)), AnnotatedStatement)


if __name__ == '__main__':
    Test.main()
