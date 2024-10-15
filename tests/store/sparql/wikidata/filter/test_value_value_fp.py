# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    ExternalId,
    Filter,
    IRI,
    Statement,
    String,
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

    # -- item --

    def test_item_item(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.Pico_da_Neblina,
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

    def test_lexeme_item(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.Q(56648699),
            equals=[
                ((wd.L(305364), wd.has_effect),  # VV
                 (wd.L(305364), wd.has_effect)),
                ((wd.L(305364), None),  # VF
                 (wd.L(305364), wd.has_effect)),
            ],
            contains=[
                ((None, wd.has_effect), [  # FV
                    (wd.L(305364), wd.has_effect),
                    (wd.L(630659), wd.has_effect),
                ]),
            ])

    def test_property_item(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.mass_,
            equals=[
                ((wd.mass, wd.Wikidata_item_of_this_property),  # VV
                 (wd.mass, wd.Wikidata_item_of_this_property)),
                ((None, wd.Wikidata_item_of_this_property),  # FV
                 (wd.mass, wd.Wikidata_item_of_this_property)),
            ],
            contains=[
                ((wd.mass, None), [  # VF
                    (wd.mass, wd.Wikidata_item_of_this_property),
                    (wd.mass, wd.class_of_non_item_property_value),
                ]),
            ])

    # -- property --

    def test_item_property(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.mass,
            equals=[
                ((wd.mass_, wd.Wikidata_property),  # VV
                 (wd.mass_, wd.Wikidata_property)),
                ((wd.mass_, None),  # VF
                 (wd.mass_, wd.Wikidata_property))
            ],
            contains=[
                ((None, wd.Wikidata_property), [  # FV
                    (wd.Q(6753082), wd.Wikidata_property),
                    (wd.Q(938476), wd.Wikidata_property),
                    (wd.Q(582695), wd.Wikidata_property),
                ]),
            ])

    def test_lexeme_property(self) -> None:
        ###
        # FIXME: This will break, eventually, as it is bad usage.
        ###
        self._test_filter_with_fixed_value(
            value=wd.P(641),
            equals=[
                ((wd.L(723018), wd.Wikidata_property),  # VV
                 (wd.L(723018), wd.Wikidata_property)),
                ((wd.L(723018), None),  # VF
                 (wd.L(723018), wd.Wikidata_property)),
            ],
            contains=[
                ((None, wd.Wikidata_property), [  # FV
                    (wd.L(723018), wd.Wikidata_property),
                    (wd.Q(349), wd.Wikidata_property),
                ]),
            ])

    def test_property_property(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.grammatical_gender,
            empty=[
                (wd.sex_or_gender, wd.subproperty_of),
            ],
            equals=[
                ((wd.sex_or_gender, wd.related_property),  # VV
                 (wd.sex_or_gender, wd.related_property)),
                ((wd.sex_or_gender, None),  # VF
                 (wd.sex_or_gender, wd.related_property)),
            ],
            contains=[
                ((None, wd.related_property), [  # FV
                    (wd.P(10339), wd.related_property),
                    (wd.P(5109), wd.related_property),
                    (wd.P(5713), wd.related_property),
                    (wd.sex_or_gender, wd.related_property),
                ]),
            ])

    # -- lexeme --

    def test_item_lexeme(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.L(22478),
            equals=[
                ((wd.Q(57012243), wd.subject_lexeme),  # VV
                 (wd.Q(57012243), wd.subject_lexeme)),
                ((wd.Q(57012243), None),  # VF
                 (wd.Q(57012243), wd.subject_lexeme)),
                ((None, wd.subject_lexeme),  # FV
                 (wd.Q(57012243), wd.subject_lexeme)),
            ])

    def test_lexeme_lexeme(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.L(4760),
            equals=[
                ((wd.L(4761), wd.derived_from_lexeme),  # VV
                 (wd.L(4761), wd.derived_from_lexeme)),
                ((None, wd.derived_from_lexeme),  # FV
                 (wd.L(4761), wd.derived_from_lexeme)),

            ],
            contains=[
                ((wd.L(4761), None), [  # VF
                    (wd.L(4761), wd.derived_from_lexeme),
                    (wd.L(4761), wd.homograph_lexeme),
                ]),
            ])

    def test_property_lexeme(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.L(991702),
            equals=[
                ((wd.P(11785), wd.Wikidata_property_example_for_lexemes),  # VV
                 (wd.P(11785), wd.Wikidata_property_example_for_lexemes)),
                ((wd.P(11785), None),  # VF
                 (wd.P(11785), wd.Wikidata_property_example_for_lexemes)),
                ((None, wd.Wikidata_property_example_for_lexemes),  # FV
                 (wd.P(11785), wd.Wikidata_property_example_for_lexemes)),
            ])

    # -- iri --

    def test_item_iri(self) -> None:
        self._test_filter_with_fixed_value(
            value=IRI('https://www.ibm.com/'),
            equals=[
                ((wd.IBM, wd.official_website),  # VV
                 (wd.IBM, wd.official_website)),
                ((wd.IBM, None),  # VF
                 (wd.IBM, wd.official_website)),
                ((None, wd.official_website),  # FV
                 (wd.IBM, wd.official_website)),
            ],
            contains=[
                ((wd.IBM, None), [
                    (wd.IBM, wd.official_website),
                ]),
            ])

    def test_lexeme_iri(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_iri(self) -> None:
        self._test_filter_with_fixed_value(
            value=IRI('https://transparency-register.europa.eu/'),
            equals=[
                ((wd.EU_Transparency_Register_ID,  # VV
                  wd.source_website_for_the_property),
                 (wd.EU_Transparency_Register_ID,
                  wd.source_website_for_the_property)),
                ((wd.EU_Transparency_Register_ID,  # VF
                  None),
                 (wd.EU_Transparency_Register_ID,
                  wd.source_website_for_the_property)),
                ((None,         # FV
                  wd.source_website_for_the_property),
                 (wd.EU_Transparency_Register_ID,
                  wd.source_website_for_the_property)),
            ])

    # -- text --

    def test_item_text(self) -> None:
        self._test_filter_with_fixed_value(
            value=Text('République du Chili', 'fr'),
            equals=[
                ((wd.Chile, wd.official_name),  # VV
                 (wd.Chile, wd.official_name)),
                ((wd.Chile, None),  # VF
                 (wd.Chile, wd.official_name)),
                ((None, wd.official_name),  # FV
                 (wd.Chile, wd.official_name)),
            ])

    def test_lexeme_text(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_text(self) -> None:
        self._test_filter_with_fixed_value(
            value=Text('Bionomia ID', 'en'),
            equals=[
                ((wd.P(6944), wd.official_name),  # VV
                 (wd.P(6944), wd.official_name)),
                ((wd.P(6944), None),  # VF
                 (wd.P(6944), wd.official_name)),
                ((None, wd.official_name),  # FV
                 (wd.P(6944), wd.official_name)),
            ])

    # -- string --

    def test_item_string(self) -> None:
        self._test_filter_with_fixed_value(
            value=String('🇧🇷'),
            equals=[
                ((wd.Brazil, wd.Unicode_character),  # VV
                 (wd.Brazil, wd.Unicode_character)),
                ((wd.Brazil, None),  # VF
                 (wd.Brazil, wd.Unicode_character)),
            ],
            contains=[
                ((None, wd.Unicode_character), [  # FV
                    (wd.Brazil, wd.Unicode_character),
                ]),
            ])

    def test_lexeme_string(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_string(self) -> None:
        self._test_filter_with_fixed_value(
            value=String('Key:height'),
            equals=[
                ((wd.height, wd.OpenStreetMap_tag_or_key),  # VV
                 (wd.height, wd.OpenStreetMap_tag_or_key)),
                ((wd.height, None),  # VF
                 (wd.height, wd.OpenStreetMap_tag_or_key)),
            ],
            contains=[
                ((None, wd.OpenStreetMap_tag_or_key), [  # FV
                    (wd.height, wd.OpenStreetMap_tag_or_key),
                    (wd.height_, wd.OpenStreetMap_tag_or_key),
                ]),
            ])

    # -- external id --

    def test_item_external_id(self) -> None:
        self._test_filter_with_fixed_value(
            value=ExternalId('/m/09_c5v'),
            equals=[
                ((wd.Adam, wd.Freebase_ID),  # VV
                 (wd.Adam, wd.Freebase_ID)),
                ((wd.Adam, None),  # VF
                 (wd.Adam, wd.Freebase_ID)),
                ((None, wd.Freebase_ID),  # FV
                 (wd.Adam, wd.Freebase_ID)),
            ])

    def test_lexeme_external_id(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_external_id(self) -> None:
        self._test_filter_with_fixed_value(
            value=ExternalId('RO_0002411'),
            equals=[
                ((wd.has_cause, wd.Relations_Ontology_ID),  # VV
                 (wd.has_cause, wd.Relations_Ontology_ID)),
                ((wd.has_cause, None),  # VF
                 (wd.has_cause, wd.Relations_Ontology_ID)),
                ((None, wd.Relations_Ontology_ID),  # FV
                 (wd.has_cause, wd.Relations_Ontology_ID)),
            ])

    # -- quantity --

    def test_item_quantity(self) -> None:
        self._test_filter_with_fixed_value(
            value='78.046950192'@wd.dalton,
            equals=[
                ((wd.benzene, wd.mass),  # VV
                 (wd.benzene, wd.mass)),
                ((wd.benzene, None),  # VF
                 (wd.benzene, wd.mass)),
            ],
            contains=[
                ((None, wd.mass), [  # FV
                    (wd.benzene, wd.mass),
                    (wd.Q(82466736), wd.mass),
                    (wd.Q(82002936), wd.mass),
                    (wd.Q(83011151), wd.mass),
                    (wd.Q(82526818), wd.mass),
                ]),
            ])

    def test_lexeme_quantity(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_quantity(self) -> None:
        self._test_filter_with_fixed_value(
            value=484@wd._1,
            equals=[
                ((wd.TheCocktailDB_ingredient_ID, wd.number_of_records),  # VV
                 (wd.TheCocktailDB_ingredient_ID, wd.number_of_records)),
                ((wd.TheCocktailDB_ingredient_ID, None),  # VF
                 (wd.TheCocktailDB_ingredient_ID, wd.number_of_records)),
                ((None, wd.number_of_records),  # FV
                 (wd.TheCocktailDB_ingredient_ID, wd.number_of_records)),
            ])

    # -- time --

    def test_item_time(self) -> None:
        self._test_filter_with_fixed_value(
            value=Time('1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar),
            equals=[
                ((wd.Brazil, wd.inception),  # VV
                 (wd.Brazil, wd.inception)),
                ((wd.Brazil, None),  # VF
                 (wd.Brazil, wd.inception)),
            ],
            contains=[          # FV
                ((None, wd.inception), [
                    (wd.Brazil, wd.inception),
                    (wd.Q(113474333), wd.inception),
                    (wd.Q(217230), wd.inception),
                ]),
            ])

    def test_lexeme_time(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_time(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    # -- some value --

    def test_item_some_value(self) -> None:
        self._test_filter(
            equals=[
                (Filter(wd.Adam, wd.family_name),  # VV
                 Statement(wd.Adam, wd.family_name.some_value())),
            ],
            contains=[
                (Filter(wd.Adam, None), [  # VF
                    Statement(wd.Adam, wd.date_of_birth.some_value()),
                    Statement(wd.Adam, wd.date_of_death.some_value()),
                    Statement(wd.Adam, wd.family_name.some_value()),
                ]),
            ])

    def test_lexeme_some_value(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    def test_property_some_value(self) -> None:
        ###
        # TODO: No example in Wikidata.
        ###
        pass

    # -- no value --

    def test_item_no_value(self) -> None:
        self._test_filter(
            equals=[
                (Filter(wd.Adam, wd.father),  # VV
                 Statement(wd.Adam, wd.father.no_value())),
            ],
            contains=[
                (Filter(wd.Adam, None), [  # VF
                    Statement(wd.Adam, wd.father.no_value()),
                    Statement(wd.Adam, wd.mother.no_value()),
                ]),
            ])

    def test_lexeme_no_value(self) -> None:
        self._test_filter(
            equals=[
                (Filter(wd.L(1118648), wd.combines_lexemes,
                        snak_mask=Filter.NO_VALUE_SNAK),  # VV
                 Statement(wd.L(1118648), wd.combines_lexemes.no_value())),
                (Filter(wd.L(1118648), None,
                        snak_mask=Filter.NO_VALUE_SNAK),  # VF
                 Statement(wd.L(1118648), wd.combines_lexemes.no_value())),
            ],
            contains=[
                (Filter(
                    None, wd.combines_lexemes,
                    snak_mask=Filter.NO_VALUE_SNAK), [  # FV
                        Statement(
                            wd.L(1118648), wd.combines_lexemes.no_value()),
                ]),
            ])

    def test_property_no_value(self) -> None:
        self._test_filter(
            equals=[
                (Filter(        # VV
                    wd.subclass_of, wd.property_proposal_discussion),
                 Statement(wd.subclass_of,
                           wd.property_proposal_discussion.no_value())),
                (Filter(        # VF
                    wd.subclass_of, None, snak_mask=Filter.NO_VALUE_SNAK),
                 Statement(wd.subclass_of,
                           wd.property_proposal_discussion.no_value())),
            ],
            contains=[
                (Filter(        # FV
                    None, wd.property_proposal_discussion,
                    snak_mask=Filter.NO_VALUE_SNAK), [
                        Statement(wd.subclass_of,
                                  wd.property_proposal_discussion.no_value())
                ]),
            ])


if __name__ == '__main__':
    Test.main()
