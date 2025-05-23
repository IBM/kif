# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    ItemVariable,
    Property,
    Quantity,
    Statement,
    StatementVariable,
    Variable,
)
from kif_lib.compiler.sparql import SPARQL_Compiler, SPARQL_Mapping
from kif_lib.model import VStatement
from kif_lib.typing import Any, assert_type, Callable, Iterator, Sequence

from ....tests import TestCase


class Empty(SPARQL_Mapping):
    pass


class A(SPARQL_Mapping):

    @SPARQL_Mapping.register([Property('x')(Item('y'), Item('z'))])
    def f1(self, c: SPARQL_Compiler, *args):
        assert len(args) == 0

    @SPARQL_Mapping.register([Property('x')(ItemVariable('y'), Quantity(0))])
    def f2(self, c: SPARQL_Compiler, *args):
        pass

    @SPARQL_Mapping.register([Variable('x')@Statement])
    def f3(self, c: SPARQL_Compiler, x: StatementVariable):
        pass


class Test(TestCase):

    def assert_entry(
            self,
            entry: SPARQL_Mapping.Entry,
            id: SPARQL_Mapping.EntryId,
            patterns: Sequence[VStatement],
            callback: Callable[..., Any]
    ) -> None:
        self.assertIsInstance(entry, SPARQL_Mapping.Entry)
        self.assertEqual(entry.id, id)
        self.assertEqual(entry.get_id(), id)
        self.assertEqual(entry.patterns, tuple(patterns))
        self.assertEqual(entry.get_patterns(), tuple(patterns))
        self.assertEqual(entry.callback, callback)
        self.assertEqual(entry.get_callback(), callback)

    def test__init__(self) -> None:
        assert_type(Empty(), Empty)
        self.assertIsInstance(Empty(), SPARQL_Mapping)
        self.assertIsInstance(A(), SPARQL_Mapping)

    def test__getitem__(self) -> None:
        assert_type(A()[0], A.Entry)
        a = A()
        pat1 = Property('x')(Item('y'), Item('z'))
        pat2 = Property('x')(ItemVariable('y'), Quantity(0))
        pat3 = StatementVariable('x')
        self.assert_entry(a[0], 0, [pat1], A.f1)
        self.assert_entry(a[1], 1, [pat2], A.f2)
        self.assert_entry(a[2], 2, [pat3], A.f3)

    def test__iter__(self) -> None:
        assert_type(iter(A()), Iterator[A.Entry])

    def test__len__(self) -> None:
        assert_type(len(Empty()), int)
        self.assertEqual(len(Empty()), 0)
        self.assertEqual(len(A()), 3)


if __name__ == '__main__':
    Test.main()
