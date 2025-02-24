# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import IRI, Item, Property
from kif_lib.context.registry import IRI_Registry, Registry
from kif_lib.typing import Any, assert_type

from ...tests import TestCase


class Test(TestCase):

    def assert_register(
            self,
            r: IRI_Registry,
            iri: IRI,
            **kwargs: Any
    ) -> None:
        self.assertEqual(r.register(iri, **kwargs), iri)

    def test__init__(self) -> None:
        r = IRI_Registry()
        assert_type(r, IRI_Registry)
        self.assertIsInstance(r, IRI_Registry)
        self.assertIsInstance(r, Registry)

    def test_register(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Property into IRI',
            r.register, Property('x'))

    def test_unregister(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.unregister, Item('x'))

if __name__ == '__main__':
    Test.main()
