# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Datatype,
    DatatypeVariable,
    ExternalId,
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemVariable,
    LexemeDatatype,
    PropertyDatatype,
    QuantityDatatype,
    QuantityVariable,
    StatementVariable,
    String,
    StringDatatype,
    Term,
    TextDatatype,
    Theta,
    TimeDatatype,
    ValueSnakVariable,
    Variable,
)
from kif_lib.namespace import WIKIBASE
from kif_lib.typing import assert_type, cast, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(DatatypeVariable.object_class, type[Datatype])
        self.assertIs(DatatypeVariable.object_class, Datatype)

    def test_check(self) -> None:
        assert_type(
            DatatypeVariable.check(DatatypeVariable('x')), DatatypeVariable)
        assert_type(
            DatatypeVariable.check(Variable('x', Datatype)), DatatypeVariable)
        self._test_check(DatatypeVariable)

    def test__init__(self) -> None:
        assert_type(DatatypeVariable('x'), DatatypeVariable)
        self._test__init__(DatatypeVariable, self.assert_datatype_variable)

    def test_variables(self) -> None:
        assert_type(DatatypeVariable('x').variables, Set[Variable])
        self._test_variables(DatatypeVariable)

    def test_instantiate(self) -> None:
        assert_type(
            DatatypeVariable('x').instantiate({}), Optional[Term])
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): String('y')
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): ExternalId('y')
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): IRI('y')
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): 'y'  # type: ignore
            })))

    def test_instantiate_uri(self) -> None:
        self.assert_item_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.WikibaseItem  # type: ignore
            })))
        self.assert_property_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'):
                WIKIBASE.WikibaseProperty  # type: ignore
            })))
        self.assert_lexeme_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'):
                WIKIBASE.WikibaseLexeme  # type: ignore
            })))
        self.assert_iri_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.Url  # type: ignore
            })))
        self.assert_text_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'):
                WIKIBASE.Monolingualtext  # type: ignore
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.String  # type: ignore
            })))
        self.assert_external_id_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.ExternalId  # type: ignore
            })))
        self.assert_quantity_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.Quantity  # type: ignore
            })))
        self.assert_time_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): WIKIBASE.Time  # type: ignore
            })))

    def test_instantiate_and_match(self) -> None:
        assert_type(
            DatatypeVariable('x').instantiate({}), Optional[Term])
        assert_type(
            DatatypeVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            DatatypeVariable,
            success=[
                DatatypeVariable('x'),
                ItemDatatype(),
                PropertyDatatype(),
                LexemeDatatype(),
                IRI_Datatype(),
                TextDatatype(),
                StringDatatype(),
                ExternalIdDatatype(),
                QuantityDatatype(),
                TimeDatatype(),
            ],
            failure=[
                IRI_Variable('x'),
                Item('x'),
                ItemVariable('x'),
                QuantityVariable('x'),
                StatementVariable('x'),
                ValueSnakVariable('x'),
            ])


if __name__ == '__main__':
    Test.main()
