# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from kif_lib.context import Section
from kif_lib.typing import Any, assert_type

from ..tests import TestCase


@dataclasses.dataclass
class B(Section, name='b'):
    z: bool = True


@dataclasses.dataclass
class A(Section, name='a'):
    x: str
    y: int
    b: B = dataclasses.field(default_factory=B)


class Test(TestCase):

    def test_name(self) -> None:
        assert_type(A.name, str)
        self.assertEqual(A.name, 'a')
        self.assertEqual(B.name, 'b')

    def test_getenv(self) -> None:
        import os
        self.assertEqual(os.getenv('PWD'), Section.getenv('PWD'))

    def test__init__(self) -> None:
        a = A(x='abc', y=0)
        assert_type(a, A)
        self.assertIsInstance(a, A)
        assert_type(a.b, B)
        self.assertIsInstance(a.b, B)
        self.assertEqual(a.x, 'abc')
        self.assertEqual(a.y, 0)
        self.assertEqual(a.b, B())
        self.assertIs(a.b.z, True)

    def test_from_ast(self) -> None:
        assert_type(B.from_ast({}), B)
        self.assertEqual(B.from_ast({}), B())
        self.assertEqual(B.from_ast({'z': True}), B())
        self.assertEqual(B.from_ast({'z': False}), B(False))
        self.assertRaises(TypeError, A.from_ast, {})
        self.assertEqual(A.from_ast({'x': 'abc', 'y': 0}), A('abc', 0))
        self.assertEqual(
            A.from_ast({'x': 'def', 'y': 1, 'b': {'z': False}}),
            A('def', 1, B(False)))

    def test_to_ast(self) -> None:
        assert_type(B().to_ast(), dict[str, Any])
        self.assertEqual(B().to_ast(), {'z': True})
        self.assertEqual(B(False).to_ast(), {'z': False})
        self.assertEqual(
            A('abc', 0).to_ast(),
            {'x': 'abc', 'y': 0, 'b': {'z': True}})
        self.assertEqual(
            A('abc', 0, B(False)).to_ast(),
            {'x': 'abc', 'y': 0, 'b': {'z': False}})

    def test_to_str(self) -> None:
        assert_type(B().to_str(), str)
        self.assertEqual(B().to_str(), 'b.z: bool = True')
        self.assertEqual(A('abc', 0).to_str(), '''\
a.b.z: bool = True
a.x: str = abc
a.y: int = 0''')


if __name__ == '__main__':
    Test.main()
