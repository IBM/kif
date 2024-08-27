# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Union
from unittest import main, TestCase

from kif_lib.compiler.sparql.builder import (
    BNode,
    Call,
    Literal,
    NumericExpression,
    NumericLiteral,
    Query,
    STR,
    Symbol,
    URIRef,
    Variable,
)

NL = NumericLiteral


class Test(TestCase):

    def assert_call(
            self,
            obj: Call,
            cls: type[Call],
            op: Union[URIRef, str],
            *args: NumericExpression
    ):
        self.assertIsInstance(obj, cls)
        self.assertEqual(obj.operator, op)
        self.assertEqual(obj.args, args)

    def assert_str(self, obj: Call, arg: NumericExpression):
        self.assert_call(obj, STR, Symbol.STR, arg)
        self.assertEqual(str(obj), f'{Symbol.STR}({arg})')

    def test_str(self) -> None:
        q = Query()
        self.assert_str(q.str(URIRef('x')), NL(URIRef('x')))
        b = BNode()
        self.assert_str(q.str(b), NL(b))
        self.assert_str(q.str(Literal(0)), NL(Literal(0)))
        self.assert_str(q.str(Variable('x')), NL(Variable('x')))
        self.assert_str(q.str(0), NL(Literal(0)))
        self.assert_str(q.str(''), NL(Literal('')))


if __name__ == '__main__':
    main()
