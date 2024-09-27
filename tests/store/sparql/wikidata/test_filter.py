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
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    SomeValueSnak,
    Statement,
    String,
    Text,
    Time,
    ValueSnak,
    Variables,
)
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
from kif_lib.store.sparql2 import SPARQL_Store2
from kif_lib.typing import Any, Final, override
from kif_lib.vocabulary import wd

from ....tests import SPARQL_Store2TestCase

w, x, y, z = Variables(*'wxyz')


class Test(SPARQL_Store2TestCase):

    WIKIDATA: Final[str | None] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls):
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args: Any, **kwargs: Any) -> SPARQL_Store2:
        assert cls.WIKIDATA is not None
        return SPARQL_Store2(
            'sparql2', cls.WIKIDATA,
            WikidataMapping(strict=True), *args, **kwargs)

    def test_empty(self) -> None:
        self._test_filter_preset_empty()

    def test_subject_item(self) -> None:
        self._test_filter(
            empty=[
                Filter(Item('x')),    # bad item IRI
                Filter(wd.Q('xxx')),  # bad item IRI
                Filter(wd.Q(10**10)),  # no such item
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.Adam,
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            equals=[
                ((wd.part_of, wd.Adam_and_Eve),  # VV
                 wd.part_of(wd.Adam_and_Eve)),
                ((wd.date_of_birth, None),  # VF
                 wd.date_of_birth.some_value()),
                ((wd.father, None),
                 wd.father.no_value()),
                ((wd.part_of, None),
                 wd.part_of(wd.Adam_and_Eve)),
                ((None, Text('אָדָם', 'he')),  # FV
                 wd.name_in_native_language(Text('אָדָם', 'he'))),
            ],
            contains=[
                ((None, None), [  # FF
                    wd.instance_of(wd.human_biblical_figure),
                    wd.instance_of(wd.protoplast),
                    wd.instance_of(wd.mythical_character),
                    wd.part_of(wd.Adam_and_Eve),
                    wd.sex_or_gender(wd.male),
                    wd.name_in_native_language(Text('אָדָם', 'he')),
                    wd.family_name.some_value(),
                    wd.date_of_birth.some_value(),
                    wd.place_of_birth(wd.Garden_of_Eden),
                    wd.father.no_value(),
                    wd.mother.no_value(),
                    wd.spouse(wd.Eve),
                    wd.participant_in(wd.Fall_of_man),
                    wd.Freebase_ID('/m/09_c5v'),
                    wd.WordNet_31_Synset_ID('09609728-n'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.ITEM), Statement(Item(x), y))

    def test_subject_property(self) -> None:
        self._test_filter(
            empty=[
                Filter(Property('x')),  # bad property IRI
                Filter(wd.P('xxx')),    # bad property IRI
                Filter(wd.P(10**10)),   # no such property
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.mass,
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            equals=[
                ((wd.Wikidata_item_of_this_property, wd.mass_),  # VV
                 wd.Wikidata_item_of_this_property(wd.mass_)),
                ((wd.equivalent_property, IRI('https://schema.org/weight')),
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
                ((wd.equivalent_property, None),  # VF
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
                ((None, IRI('https://schema.org/weight')),  # FV
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
            ],
            contains=[          # FF
                ((None, None), [
                    wd.instance_of(
                        wd.Wikidata_property_for_physical_quantities),
                    wd.instance_of(
                        wd.Wikidata_property_related_to_animals_and_zoology),
                    wd.Wikidata_item_of_this_property(wd.mass_),
                    wd.equivalent_property(IRI('https://schema.org/weight')),
                    wd.type_of_unit_for_this_property(wd.unit_of_mass),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.PROPERTY),
            Statement(Property(x, y), z))

    def test_subject_lexeme(self) -> None:
        self._test_filter(
            empty=[
                Filter(Lexeme('x')),  # bad lexeme IRI
                Filter(wd.L('xxx')),  # bad lexeme IRI
                Filter(wd.L(10**10)),  # no such lexeme
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.L(4129),
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            contains=[          # FF
                ((None, None), [
                    wd.described_by_source(wd.Q(58489371)),
                    wd.derived_from_lexeme(wd.L(348331)),
                    wd.homograph_lexeme(wd.L(333796)),
                    wd.homograph_lexeme(wd.L(16927)),
                    wd.homograph_lexeme(wd.L(337374)),
                    wd.Dictionary_of_American_Regional_English_ID(
                        'ID_00029294'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.LEXEME), Statement(Lexeme(x), y))

    def test_subject_some_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.SOME_VALUE_SNAK),
            Statement(wd.Adam, SomeValueSnak(y)))

    def test_subject_no_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.NO_VALUE_SNAK),
            Statement(wd.Adam, NoValueSnak(y)))

    def test_property(self) -> None:
        self._test_filter(
            empty=[
                Filter(property=Property('x')),  # bad property IRI
                Filter(property=wd.P('xxx')),    # bad property IRI
                Filter(property=wd.P(10**10)),   # no such property
            ])

    def test_property_item(self) -> None:
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

    def test_property_property(self) -> None:
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

    def test_property_lexeme(self) -> None:
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

    def test_property_iri(self) -> None:
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

    def test_property_text(self) -> None:
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

    def test_property_string(self) -> None:
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

    def test_property_external_id(self) -> None:
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

    def test_property_quantity(self) -> None:
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

    def test_property_time(self) -> None:
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

    def test_property_some_value(self) -> None:
        self._test_filter_matches(
            Filter(None, wd.date_of_birth, snak_mask=Filter.SOME_VALUE_SNAK),
            Statement(x, SomeValueSnak(wd.date_of_birth)))

    def test_property_no_value(self) -> None:
        self._test_filter_matches(
            Filter(None, wd.father, snak_mask=Filter.NO_VALUE_SNAK),
            Statement(x, NoValueSnak(wd.father)))

    def test_value_item(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.Pico_da_Neblina,
            empty=[
                (wd.Brazil, wd.country),  # VV
                (wd.Adam, None),          # VF
                (None, wd.country),       # FV
            ],
            equals=[
                ((wd.Brazil, wd.highest_point),  # VV
                 (wd.Brazil, wd.highest_point)),
                ((wd.Brazil, None),  # VF
                 (wd.Brazil, wd.highest_point)),
                ((None, wd.parent_peak),  # FV
                 (wd.Pico_31_de_Março, wd.parent_peak)),
            ],
            contains=[
                ((None, None), [  # FF
                    (wd.Amazonas, wd.highest_point),
                    (wd.Brazil, wd.highest_point),
                    (wd.Pico_31_de_Março, wd.parent_peak),
                ]),
            ])
        self._test_filter_matches(
            Filter(value_mask=Filter.ITEM, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Item(z))))

    def test_value_property(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.PROPERTY, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Property(z).generalize())))

    def test_value_lexeme(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.LEXEME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Lexeme(z))))

    def test_value_iri(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.IRI, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, IRI(z))))

    def test_value_text(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TEXT, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Text(z, w))))

    def test_value_string(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.STRING, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, String(z))))

    def test_value_external_id(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.EXTERNAL_ID, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, ExternalId(z))))

    def test_value_quantity(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.QUANTITY, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Quantity(z).generalize())))

    def test_value_time(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TIME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Time(z).generalize())))


if __name__ == '__main__':
    Test.main()
