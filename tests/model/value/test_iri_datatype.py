# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import (
    Datatype,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    String,
    Value,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(
            IRI_Datatype, 0, IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, {}, IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, IRI('x'), IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, ItemDatatype(), IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, Item, IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, String, IRI_Datatype.check)
        self.assert_raises_check_error(
            IRI_Datatype, Value, IRI_Datatype.check)
        # success
        assert_type(IRI_Datatype.check(IRI_Datatype()), IRI_Datatype)
        self.assertEqual(
            IRI_Datatype.check(IRI_Datatype()), IRI.datatype)
        self.assertEqual(
            IRI_Datatype.check(Datatype(IRI_Datatype)), IRI.datatype)
        self.assertEqual(
            IRI_Datatype.check(Datatype(IRI)), IRI.datatype)
        self.assertEqual(
            IRI_Datatype.check(IRI), IRI.datatype)

    def test__init__(self) -> None:
        self.assert_raises_check_error(IRI_Datatype, 0)
        # success
        assert_type(IRI_Datatype(), IRI_Datatype)
        self.assert_iri_datatype(IRI_Datatype())
        self.assert_iri_datatype(Datatype(IRI_Datatype))
        self.assert_iri_datatype(Datatype(IRI))


if __name__ == '__main__':
    Test.main()
