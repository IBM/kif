# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime

from kif_lib import (
    Context,
    ExternalId,
    Filter,
    IRI,
    Item,
    Lexeme,
    Property,
    Quantity,
    String,
    Text,
    Time,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    EmptyFingerprint,
    Fingerprint,
    FullFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import FingerprintTestCase


class Test(FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(ValueFingerprint.check('x'), ValueFingerprint)
        super()._test_check(
            ValueFingerprint,
            success=[
                (ValueFingerprint(Item('x')), ValueFingerprint(Item('x'))),
                (Item('x'), ValueFingerprint(Item('x'))),
                (Property('x'), ValueFingerprint(Property('x'))),
                (Lexeme('x'), ValueFingerprint(Lexeme('x'))),
                (IRI('x'), ValueFingerprint(IRI('x'))),
                (Text('x'), ValueFingerprint(Text('x'))),
                (String('x'), ValueFingerprint(String('x'))),
                (ExternalId('x'), ValueFingerprint(ExternalId('x'))),
                (Quantity(0), ValueFingerprint(Quantity(0))),
                (Time('2024-07-27'), ValueFingerprint(Time('2024-07-27'))),
                ('x', ValueFingerprint(String('x'))),
                (0, ValueFingerprint(Quantity(0))),
            ],
            failure=[
                AndFingerprint(EmptyFingerprint()),
                FullFingerprint(),
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(ValueFingerprint(0), ValueFingerprint)
        super()._test__init__(
            ValueFingerprint,
            self.assert_value_fingerprint,
            success=[
                ([Item('x')], ValueFingerprint(Item('x'))),
                ([Property('x')], ValueFingerprint(Property('x'))),
                ([Lexeme('x')], ValueFingerprint(Lexeme('x'))),
                ([IRI('x')], ValueFingerprint(IRI('x'))),
                ([Text('x', 'y')], ValueFingerprint(Text('x', 'y'))),
                ([String('x')], ValueFingerprint(String('x'))),
                (['x'], ValueFingerprint(String('x'))),
                ([ExternalId('x')], ValueFingerprint(ExternalId('x'))),
                ([Quantity(0)], ValueFingerprint(Quantity(0))),
                ([0], ValueFingerprint(Quantity(0))),
                ([Time('2024-07-27')], ValueFingerprint(Time('2024-07-27'))),
            ],
            failure=[
                [FullFingerprint()],
                [None],
                [Property('p')(Item('x'))],
                [Variable('x', Item)],
            ])

    def test_datatype_mask(self) -> None:
        assert_type(ValueFingerprint('x').datatype_mask, Filter.DatatypeMask)
        self.assertEqual(
            ValueFingerprint(Item('x')).datatype_mask, Filter.ITEM)
        self.assertEqual(
            ValueFingerprint(Property('x')).datatype_mask, Filter.PROPERTY)
        self.assertEqual(
            ValueFingerprint(Lexeme('x')).datatype_mask, Filter.LEXEME)
        self.assertEqual(
            ValueFingerprint(IRI('x')).datatype_mask, Filter.IRI)
        self.assertEqual(
            ValueFingerprint(Text('x')).datatype_mask, Filter.TEXT)
        self.assertEqual(
            ValueFingerprint(String('x')).datatype_mask, Filter.STRING)
        self.assertEqual(
            ValueFingerprint(ExternalId('x')).datatype_mask,
            Filter.EXTERNAL_ID)
        self.assertEqual(
            ValueFingerprint(Quantity(0)).datatype_mask, Filter.QUANTITY)
        self.assertEqual(
            ValueFingerprint(Time('2024-07-27')).datatype_mask, Filter.TIME)

    def test_match(self) -> None:
        assert_type(ValueFingerprint(Item('x')).match('x'), bool)
        # item
        self.assert_match(ValueFingerprint(Item('x')), Item('x'))
        self.assert_not_match(
            ValueFingerprint(Item('x')),
            Item('y'), Property('x'), IRI('x'), String('x'), Quantity(0))
        # property
        self.assert_match(ValueFingerprint(Property('x')), Property('x'))
        self.assert_not_match(ValueFingerprint(Property('x')), Property('y'))
        self.assert_match(
            ValueFingerprint(Property('x', Item)), Property('x'))
        self.assert_match(
            ValueFingerprint(Property('x')), Property('x', Item))
        # lexeme
        self.assert_not_match(
            ValueFingerprint(Property('x', Lexeme)),
            Property('x', Item), Property('y', Lexeme))
        self.assert_match(
            ValueFingerprint(Property('x', Lexeme)), Property('x', Lexeme))
        self.assert_match(ValueFingerprint(Lexeme('x')), Lexeme('x'))
        self.assert_not_match(
            ValueFingerprint(Lexeme('x')),
            Lexeme('y'), IRI('x'), Item('x'), Quantity(0))
        # iri
        self.assert_match(ValueFingerprint(IRI('x')), IRI('x'))
        self.assert_not_match(
            ValueFingerprint(IRI('x')), IRI('y'), Lexeme('x'))
        # text
        self.assert_match(ValueFingerprint(Text('x')), Text('x'))
        self.assert_not_match(
            ValueFingerprint(Text('x')), Text('y'), Text('x', 'pt'))
        self.assert_match(
            ValueFingerprint(Text(
                'x', Context.top().options.language)), Text('x'))
        self.assert_match(
            ValueFingerprint(Text('x')), Text(
                'x', Context.top().options.language))
        # string
        self.assert_match(ValueFingerprint('x'), String('x'))
        self.assert_match(ValueFingerprint(String('x')), String('x'))
        self.assert_not_match(
            ValueFingerprint(String('x')),
            Item('x'), IRI('x'), ExternalId('x'))
        # external id
        self.assert_match(
            ValueFingerprint(ExternalId('x')),
            ExternalId('x'), String('x'))
        self.assert_not_match(
            ValueFingerprint(ExternalId('x')),
            Item('x'), IRI('x'), ExternalId('y'), String('y'), Quantity(0))
        # quantity
        self.assert_match(
            ValueFingerprint(Quantity(0)),
            Quantity(0), Quantity(0, Item('x'), 1, 2))
        self.assert_not_match(
            ValueFingerprint(Quantity(0)),
            Quantity(1), Item('x'), IRI('x'), Time('2024-07-27'))
        self.assert_match(
            ValueFingerprint(Quantity(0, Item('x'))),
            Quantity(0, Item('x')), Quantity(0, Item('x'), 1, 2))
        self.assert_not_match(
            ValueFingerprint(Quantity(0, Item('x'))),
            Quantity(0), Quantity(1), Quantity(0, Item('y'), 1, 2))
        self.assert_match(
            ValueFingerprint(Quantity(0, None, 1)),
            Quantity(0, None, 1), Quantity(0, Item('x'), 1, 2))
        self.assert_not_match(
            ValueFingerprint(Quantity(0, None, 1)),
            Quantity(0), Quantity(1, None, 1), Quantity(0, Item('x'), 2, 2))
        self.assert_match(
            ValueFingerprint(Quantity(0, None, None, 2)),
            Quantity(0, None, None, 2), Quantity(0, Item('x'), 1, 2))
        self.assert_not_match(
            ValueFingerprint(Quantity(0, None, None, 1)),
            Quantity(0), Quantity(1, None, None, 1),
            Quantity(0, Item('x'), 1, 2))
        # time
        self.assert_match(
            ValueFingerprint(Time('2024-07-27')),
            Time('2024-07-27'),
            Time('2024-07-27', Time.Precision.DAY, 0, Item('x')))
        self.assert_match(
            ValueFingerprint(datetime.datetime(2024, 7, 27)),
            Time('2024-07-27'),
            Time('2024-07-27', Time.Precision.DAY, 0, Item('x')))
        self.assert_not_match(
            ValueFingerprint(Time('2024-07-27')),
            Time('2024-07-28'),
            Time(datetime.datetime(2024, 7, 27)))
        self.assert_match(
            ValueFingerprint(Time('2024-07-27', Time.Precision.DAY)),
            Time('2024-07-27', 11), Time('2024-07-27', 11, 0, Item('x')))
        self.assert_not_match(
            ValueFingerprint(Time('2024-07-27', Time.Precision.DAY)),
            Time('2024-07-27'), Time('2024-07-28'),
            Time('2024-07-27', 12, 0, Item('x')))
        self.assert_match(
            ValueFingerprint(Time('2024-07-27', None, 0)),
            Time('2024-07-27', None, 0),
            Time('2024-07-27', 11, 0, Item('x')))
        self.assert_not_match(
            ValueFingerprint(Time('2024-07-27', None, 0)),
            Time('2024-07-27'), Time('2024-07-28', None, 0),
            Time('2024-07-27', 12, 1, Item('x')))
        self.assert_match(
            ValueFingerprint(Time('2024-07-27', None, None, Item('x'))),
            Time('2024-07-27', None, None, Item('x')),
            Time('2024-07-27', 11, 0, Item('x')))
        self.assert_not_match(
            ValueFingerprint(Time('2024-07-27', None, None, Item('x'))),
            Time('2024-07-27'), Time('2024-07-28', None, None, Item('x')),
            Time('2024-07-27', 12, 1, Item('y')))

    def test_normalize(self) -> None:
        assert_type(ValueFingerprint('x').normalize(), Fingerprint)
        self.assert_value_fingerprint(
            ValueFingerprint(Item('x')).normalize(), Item('x'))
        self.assert_value_fingerprint(
            ValueFingerprint(Item('x')).normalize(Filter.ENTITY), Item('x'))
        self.assert_empty_fingerprint(
            ValueFingerprint(Item('x')).normalize(Filter.DEEP_DATA_VALUE))


if __name__ == '__main__':
    Test.main()
