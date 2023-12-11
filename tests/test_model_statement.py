# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import (
    IRI,
    Item,
    NoValueSnak,
    Property,
    SomeValueSnak,
    Statement,
    ValueSnak,
)

from .tests import kif_TestCase, main


class TestModelStatement(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, Statement, 0, 0)
        self.assertRaises(TypeError, Statement, IRI('x'), 0)
        self.assertRaises(TypeError, Statement, Item('x'), IRI('x'))
        # good arguments
        self.assert_statement(
            Statement(Item('x'), ValueSnak(Property('p'), IRI('u'))),
            Item('x'), ValueSnak(Property('p'), IRI('u')))
        self.assert_statement(
            Statement(Property('x'), ValueSnak(Property('p'), Item('u'))),
            Property('x'), ValueSnak(Property('p'), Item('u')))
        self.assert_statement(
            Statement(Property('x'), SomeValueSnak(Property('p'))),
            Property('x'), SomeValueSnak(Property('p')))
        self.assert_statement(
            Statement(Property('x'), NoValueSnak(Property('p'))),
            Property('x'), NoValueSnak(Property('p')))


if __name__ == '__main__':
    main()
