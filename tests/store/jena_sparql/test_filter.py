# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import os
        super().setUpClass()
        if not os.getenv('JENA_HOME'):
            raise cls.SKIP('JENA_HOME is not set')

    @classmethod
    def KB(cls):
        return cls.S(
            'sparql-jena',
            'tests/data/adam.ttl',
            'tests/data/andar.ttl',
            'tests/data/benzene.ttl',
            'tests/data/brazil.ttl')

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        ###
        # FIXME: xfilter is not working!
        ###
        xf(F(wd.Brazil), {
            # Brazil
            wd.alias(wd.Brazil, Text('pindorama', 'pt-BR')),  # FIXME: lang
            wd.alias(wd.Brazil, Text('🇧🇷', 'pt-BR')),         # FIXME: lang
            wd.description(wd.Brazil, 'country in South America'),
            wd.description(wd.Brazil, Text(
                'país na América do Sul', 'pt-BR')),
            wd.inception(wd.Brazil, Time(
                '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)),
            wd.instance_of(wd.Brazil, wd.country_),
            wd.label(wd.Brazil, 'Brazil'),
            wd.label(wd.Brazil, Text('Brasil', 'pt-BR')),  # FIXME: lang
            wd.official_name(wd.Brazil, Text(
                'República Federativa do Brasil', 'pt')),
            wd.part_of(wd.Brazil, wd.Latin_America),
        })


if __name__ == '__main__':
    Test.main()
