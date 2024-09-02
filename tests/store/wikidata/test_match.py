# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    ItemVariable,
    Lexeme,
    LexemeVariable,
    Property,
    PropertyVariable,
    StringDatatype,
    Variable,
)
from kif_lib.typing import TypeVar
from kif_lib.vocabulary import wd

from ...tests import WikidataSPARQL_StoreTestCase

T = TypeVar('T')


class Test(WikidataSPARQL_StoreTestCase):

    def test_subject_is_var(self) -> None:
        kb = self.new_Store()
        # x - shares border with - Brazil
        self.assert_it_contains(
            kb.match(wd.shares_border_with(Variable('x'), wd.Brazil)),
            wd.shares_border_with(wd.Argentina, wd.Brazil),
            wd.shares_border_with(wd.Bolivia, wd.Brazil),
            wd.shares_border_with(wd.Colombia, wd.Brazil),
            wd.shares_border_with(wd.France, wd.Brazil),
            wd.shares_border_with(wd.French_Guiana, wd.Brazil),
            wd.shares_border_with(wd.Guyana, wd.Brazil),
            wd.shares_border_with(wd.Uruguay, wd.Brazil),
            wd.shares_border_with(wd.Venezuela, wd.Brazil))
        # x - instance of - Wikidata property for physical quantities
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Variable('x'), wd.Wikidata_property_for_physical_quantities)),
            wd.instance_of(
                wd.density, wd.Wikidata_property_for_physical_quantities),
            wd.instance_of(
                wd.mass, wd.Wikidata_property_for_physical_quantities))
        # x - homograph lexeme - "change"
        self.assert_it_contains(
            kb.match(wd.homograph_lexeme(Variable('x'), wd.L(33))),
            wd.homograph_lexeme(wd.L(1259), wd.L(33)))

    def test_subject_is_item_var(self) -> None:
        kb = self.new_Store()
        # x: Item - shares border with - Brazil
        self.assert_it_contains(
            kb.match(wd.shares_border_with(ItemVariable('x'), wd.Brazil)),
            wd.shares_border_with(wd.Argentina, wd.Brazil))
        # x: Item - instance of - Wikidata property for physical quantities
        self.assert_it_empty(
            kb.match(wd.instance_of(
                ItemVariable('x'),
                wd.Wikidata_property_for_physical_quantities)))
        # x: Item - homograph lexeme - "change"
        self.assert_it_empty(
            kb.match(wd.homograph_lexeme(ItemVariable('x'), wd.L(33))))

    def test_subject_is_item_tpl(self) -> None:
        kb = self.new_Store()
        # Item(x: IRI) - shares border with - Brazil
        self.assert_it_contains(
            kb.match(wd.shares_border_with(Item(Variable('x')), wd.Brazil)),
            wd.shares_border_with(wd.Argentina, wd.Brazil))
        # Item(IRI(x: String)) - shares border with - Brazil
        self.assert_it_contains(
            kb.match(wd.shares_border_with(
                Item(IRI(Variable('x'))), wd.Brazil)),
            wd.shares_border_with(wd.Argentina, wd.Brazil))

    def test_subject_is_property_var(self) -> None:
        kb = self.new_Store()
        # x: Property - shares border with - Brazil
        self.assert_it_empty(
            kb.match(wd.shares_border_with(PropertyVariable('x'), wd.Brazil)))
        # x: Property - instance of - Wikidata property for physical quantities
        self.assert_it_contains(
            kb.match(wd.instance_of(
                PropertyVariable('x'),
                wd.Wikidata_property_for_physical_quantities)),
            wd.instance_of(
                wd.density, wd.Wikidata_property_for_physical_quantities),
            wd.instance_of(
                wd.mass, wd.Wikidata_property_for_physical_quantities))
        # x: Property - homograph lexeme - "change"
        self.assert_it_empty(
            kb.match(wd.homograph_lexeme(PropertyVariable('x'), wd.L(33))))

    def test_subject_is_property_tpl(self) -> None:
        kb = self.new_Store()
        # Property(x: IRI, y: Datatype)
        # - instance of - Wikidata property for physical quantities
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Property(Variable('x'), Variable('y')),
                wd.Wikidata_property_for_physical_quantities)),
            wd.instance_of(
                wd.density, wd.Wikidata_property_for_physical_quantities),
            wd.instance_of(
                wd.mass, wd.Wikidata_property_for_physical_quantities))
        # Property(x: IRI, y: StringDatatype)
        # - instance of - Wikidata property related to chemistry
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Property(Variable('x'), StringDatatype()),
                wd.Wikidata_property_related_to_chemistry)),
            wd.instance_of(
                wd.element_symbol, wd.Wikidata_property_related_to_chemistry))
        # Property(IRI(x: String), y: StringDatatype)
        # - instance of - Wikidata property related to chemistry
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Property(IRI(Variable('x')), StringDatatype()),
                wd.Wikidata_property_related_to_chemistry)),
            wd.instance_of(
                wd.element_symbol, wd.Wikidata_property_related_to_chemistry))
        # Property("element symbol", y: Datatype)
        # - instance of - Wikidata property related to chemistry
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Property(wd.element_symbol.iri, Variable('y')),
                wd.Wikidata_property_related_to_chemistry)),
            wd.instance_of(
                wd.element_symbol, wd.Wikidata_property_related_to_chemistry))

    def test_subject_is_lexeme_var(self) -> None:
        kb = self.new_Store()
        # x: Lexeme - shares border with - Brazil
        self.assert_it_empty(
            kb.match(wd.shares_border_with(LexemeVariable('x'), wd.Brazil)))
        # x: Lexeme - instance of - Wikidata property for physical quantities
        self.assert_it_empty(
            kb.match(wd.instance_of(
                LexemeVariable('x'),
                wd.Wikidata_property_for_physical_quantities)))
        # x: Lexeme - homograph lexeme - "change"
        self.assert_it_contains(
            kb.match(wd.homograph_lexeme(LexemeVariable('x'), wd.L(33))),
            wd.homograph_lexeme(wd.L(1259), wd.L(33)))

    def test_subject_is_lexeme_tpl(self) -> None:
        kb = self.new_Store()
        # Lexeme(x: IRI) - homograph lexeme - "change"
        self.assert_it_contains(
            kb.match(wd.homograph_lexeme(Lexeme(Variable('x')), wd.L(33))),
            wd.homograph_lexeme(wd.L(1259), wd.L(33)))
        # Lexeme(IRI(x: String)) - homograph lexeme - "change"
        self.assert_it_contains(
            kb.match(wd.homograph_lexeme(
                Lexeme(IRI(Variable('x'))), wd.L(33))),
            wd.homograph_lexeme(wd.L(1259), wd.L(33)))


if __name__ == '__main__':
    Test.main()
