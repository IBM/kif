# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    ExternalId,
    Filter,
    IRI,
    Item,
    Property,
    Quantity,
    Statement,
    Text,
    Time,
    Variables,
)
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
from kif_lib.store.sparql2 import SPARQL_Store2
from kif_lib.typing import Any, Final, override
from kif_lib.vocabulary import wd

from .....tests import SPARQL_Store2TestCase

w, x, y, z = Variables(*'wxyz')


class Test(SPARQL_Store2TestCase):

    WIKIDATA: Final[str | None] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls) -> None:
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args: Any, **kwargs: Any) -> SPARQL_Store2:
        assert cls.WIKIDATA is not None
        return SPARQL_Store2(
            'sparql2', cls.WIKIDATA,
            WikidataMapping(strict=True), *args, **kwargs)

    def test_property_dt_item(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.part_of,
            empty=[
                (wd.Brazil, wd.Bolivia),  # VV
                (wd.instance_of, None),   # VF
                (None, wd.Adam),          # FV
            ],
            equals=[
                ((wd.Brazil, wd.South_America),  # VV
                 (wd.Brazil, wd.South_America)),
                ((wd.Adam, None),  # VF
                 (wd.Adam, wd.Adam_and_Eve)),
            ],
            contains=[
                ((None, wd.Adam_and_Eve), [  # FV
                    (wd.Adam, wd.Adam_and_Eve),
                    (wd.Eve, wd.Adam_and_Eve),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(property=wd.part_of, snak_mask=Filter.VALUE_SNAK),
            Statement(Item(x), wd.part_of(y)))
        self._test_filter_matches(
            Filter(
                property=Property(wd.part_of.iri),  # no datatype
                snak_mask=Filter.VALUE_SNAK),
            Statement(Item(x), wd.part_of(y)))

    def test_property_dt_property(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.properties_for_this_type,
            empty=[
                (wd.benzene, wd.educated_at),                          # VV
                (wd.part_of, None),                                    # VF
                (None, wd.Dictionary_of_American_Regional_English_ID),  # FV
            ],
            equals=[
                ((wd.scientist, wd.educated_at),  # VV
                 (wd.scientist, wd.educated_at)),
            ],
            contains=[
                ((wd.bridge, None), [  # VF
                    (wd.bridge, wd.country),
                    (wd.bridge, wd.crosses),
                    (wd.bridge, wd.made_from_material),
                    (wd.bridge, wd.width),
                ]),
                ((None, wd.educated_at), [  # FV
                    (wd.scientist, wd.educated_at),
                ]),
            ])

    def test_property_dt_lexeme(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.homograph_lexeme,
            empty=[
                (wd.L(3), wd.L(33)),  # VV
                (wd.part_of, None),   # VF
                (None, wd.L(18)),     # FV
            ],
            equals=[
                ((wd.L(3), wd.L(338238)),  # VV
                 (wd.L(3), wd.L(338238))),
            ],
            contains=[
                ((wd.L(3773), None), [  # VF
                    (wd.L(3773), wd.L(3772)),
                    (wd.L(3773), wd.L(333647)),
                ]),
                ((None, wd.L(3772)), [  # FV
                    (wd.L(3773), wd.L(3772)),
                ]),
            ])

    def test_property_dt_iri(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.official_website,
            empty=[
                (wd.IBM, IRI('x')),  # VV
                (wd.part_of, None),  # VF
                (None, IRI('x')),    # FV
            ],
            equals=[
                ((wd.IBM, IRI('https://www.ibm.com/')),  # VV
                 (wd.IBM, IRI('https://www.ibm.com/'))),
                ((wd.IBM, None),  # VF
                 (wd.IBM, IRI('https://www.ibm.com/'))),
                ((None, IRI('https://www.ibm.com/')),  # FV
                 (wd.IBM, IRI('https://www.ibm.com/'))),
            ])

    def test_property_dt_text(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.official_name,
            empty=[
                (wd.Brazil, Text('x')),  # VV
                (wd.part_of, None),      # VF
                (None, Text('x')),       # FV
            ],
            equals=[            # VV
                ((wd.Brazil, Text('República Federativa do Brasil', 'pt')),
                 (wd.Brazil, Text('República Federativa do Brasil', 'pt'))),
                ((wd.Brazil, None),  # VF
                 (wd.Brazil, Text('República Federativa do Brasil', 'pt'))),
                ((None, Text('República Federativa do Brasil', 'pt')),  # FV
                 (wd.Brazil, Text('República Federativa do Brasil', 'pt'))),
            ])

    def test_property_dt_string(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.chemical_formula,
            empty=[
                (wd.benzene, 'x'),  # VV
                (wd.part_of, None),  # VF
                (None, 'x'),         # FV
            ],
            equals=[
                ((wd.benzene, 'C₆H₆'),  # VV
                 (wd.benzene, 'C₆H₆')),
                ((wd.benzene, None),  # VF
                 (wd.benzene, 'C₆H₆')),
            ])

    def test_property_dt_external_id(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.PubChem_CID,
            empty=[
                (wd.benzene, 'x'),  # VV
                (wd.part_of, None),  # VF
                (None, 'x'),         # FV
            ],
            ###
            # TODO: Make (wd.benzene, '241') work.
            ###
            equals=[
                ((wd.benzene, ExternalId('241')),  # VV
                 (wd.benzene, '241')),
                ((wd.benzene, None),  # VF
                 (wd.benzene, '241')),
            ])

    def test_property_dt_quantity(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.mass,
            empty=[
                (wd.benzene, 10**10),     # VV
                (wd.part_of, None),       # VF
                (None, 10**10@wd.dalton),  # FV
            ],
            equals=[
                ((wd.benzene, '78.046950192'@wd.dalton),  # VV
                 (wd.benzene, '78.046950192'@wd.dalton)),
                ((wd.benzene, Quantity('78.046950192')),
                 (wd.benzene, '78.046950192'@wd.dalton)),
                ((wd.benzene, Quantity('78.046950192')),
                 (wd.benzene, '78.046950192'@wd.dalton)),
            ],
            contains=[
                ((wd.lion, None), [  # VF
                    (wd.lion, '1.65'@wd.kilogram),
                    (wd.lion, 188@wd.kilogram),
                    (wd.lion, 126@wd.kilogram),
                ]),
            ])
        self._test_filter_with_fixed_property(
            property=wd.density,
            empty=[             # VV
                (wd.benzene, Quantity('.89')),
                (wd.benzene, Quantity('.88', wd.kilogram)),
                (wd.benzene, Quantity('.88', None, '.89')),
                (wd.benzene, Quantity('.88', None, None, '.87')),
            ],
            equals=[            # VV
                ((wd.benzene, Quantity('.88')),
                 (wd.benzene, Quantity(
                     '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))),
                ((wd.benzene, '.88'@wd.gram_per_cubic_centimetre),
                 (wd.benzene, Quantity(
                     '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))),
                ((wd.benzene, Quantity('.88', None, '.87')),
                 (wd.benzene, Quantity(
                     '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))),
                ((wd.benzene, Quantity('.88', None, None, '.89')),
                 (wd.benzene, Quantity(
                     '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))),
                ((wd.benzene, Quantity('.88', None, '.87', '.89')),
                 (wd.benzene, Quantity(
                     '.88', wd.gram_per_cubic_centimetre, '.87', '.89'))),
            ])

    def test_property_dt_time(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.inception,
            empty=[
                (wd.Brazil, Time('2024-09-26')),  # VV
                (wd.Brazil, Time('1822-09-07', 10)),
                (wd.Brazil, Time('1822-09-07', None, 1)),
                (wd.Brazil, Time(
                    '1822-09-07', None, None, wd.proleptic_Julian_calendar)),
                (wd.part_of, None),               # VF
                (None, Time('1322-09-26')),       # FV
            ],
            equals=[
                ((wd.Brazil, Time('1822-09-07')),  # VV
                 (wd.Brazil, Time(
                     '1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar))),
                ((wd.Brazil, Time('1822-09-07', 11)),
                 (wd.Brazil, Time(
                     '1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar))),
                ((wd.Brazil, Time('1822-09-07', None, 0)),
                 (wd.Brazil, Time(
                     '1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar))),
                ((wd.Brazil, Time(
                    '1822-09-07', None, None,
                    wd.proleptic_Gregorian_calendar)),
                 (wd.Brazil, Time(
                     '1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar))),
            ])


if __name__ == '__main__':
    Test.main()
