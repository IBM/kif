# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Preferred, Statement, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    _stmts: set[Statement] | None = None

    @classmethod
    def KB(cls) -> Store:
        if cls._stmts is None:
            cls._stmts = set(cls.S(
                'wikidata-rdf',
                'tests/data/adam.ttl',
                'tests/data/andar.ttl',
                'tests/data/benzene.ttl',
                'tests/data/brazil.ttl'))
        assert cls._stmts is not None
        return cls.S('memory', *cls._stmts)

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        graph = self.S('rdf', 'tests/data/andar.ttl').filter_annotated()
        xf, F = self.store_xfilter_assertion(self.S('memory', graph=graph))
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


if __name__ == '__main__':
    Test.main()
