# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal

from kif_lib import (
    Entity,
    Filter,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    KIF_Object,
    PreferredRank,
    PropertyVariable,
    Quantity,
    ValueSnak,
    Variable,
)
from kif_lib.error import EncoderError
from kif_lib.typing import cast

from ..tests import TestCase


class Test(TestCase):

    def test__init__(self) -> None:
        self.assert_abstract_class(KIF_Object)

    def test__new__(self) -> None:
        self.assertIsInstance(Item('x'), Item)
        self.assertIsInstance(ItemTemplate('x'), Item)
        self.assertIsInstance(Item(iri='x'), Item)
        self.assertIsInstance(ItemTemplate(iri='x'), Item)
        self.assertIsInstance(Item(IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(ItemTemplate(IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(Item(iri=IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(
            ItemTemplate(iri=IRI_Variable('x')), ItemTemplate)

    def test__repr_markdown_(self) -> None:
        self.assertEqual(Item('x')._repr_markdown_(), '(**Item** x)')

    def test_traverse(self) -> None:
        obj = Variable('p')(Item('x'), Quantity(5, Item('u')))
        self.assert_statement_template(
            obj, Item('x'), Variable('p')(Quantity(5, Item('u'))))
        self.assert_raises_bad_argument(
            TypeError, 1, 'filter', 'expected callable, got int',
            obj.traverse, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'visit', 'expected callable, got int',
            obj.traverse, None, 0)
        self.assertEqual(
            list(obj.traverse()), [
                obj,
                Item('x'),
                IRI('x'),
                'x',
                obj.snak,
                PropertyVariable('p'),
                'p',
                Quantity(5, Item('u')),
                decimal.Decimal(5),
                Item('u'),
                IRI('u'),
                'u',
                None,
                None])
        self.assertEqual(
            list(obj.traverse(lambda x: isinstance(x, IRI))),
            [IRI('x'), IRI('u')])
        self.assertEqual(
            list(obj.traverse(lambda x: isinstance(x, str))),
            ['x', 'p', 'u'])
        self.assertEqual(
            list(obj.traverse(None, lambda x: not isinstance(x, Entity))),
            [obj,
             obj.snak,
             PropertyVariable('p'),
             'p',
             cast(ValueSnak, obj.snak).value,
             decimal.Decimal(5),
             None,
             None])

    def test_repr_decoder_extensions(self) -> None:
        from kif_lib.model.kif_object import KIF_ReprDecoder
        dec = KIF_ReprDecoder()
        self.assertEqual(dec.decode('5'), 5)
        self.assertEqual(
            dec.decode('datetime.datetime(2024, 2, 6)'),
            datetime.datetime(2024, 2, 6))
        self.assertEqual(dec.decode("Decimal('.5')"), decimal.Decimal('.5'))
        self.assertEqual(dec.decode("set()"), set())

    def test_repr_encoder_extensions(self) -> None:
        from kif_lib.model.kif_object import KIF_ReprEncoder
        enc = KIF_ReprEncoder()
        self.assertEqual(enc.encode(IRI('x')), "IRI('x')")
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),  # type: ignore
            'datetime.datetime(2024, 2, 6, 0, 0)')
        self.assertEqual(
            enc.encode(decimal.Decimal(0)), "Decimal('0')")  # type: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(3.5)),  # type: ignore
            "Decimal('3.5')")
        self.assertEqual(
            enc.encode(Filter.SnakMask.ALL), '7')    # type: ignore
        self.assertEqual(enc.encode(set()), 'set()')     # type: ignore

    def test_json_encoder_extensions(self) -> None:
        from kif_lib.model.kif_object import KIF_JSON_Encoder
        enc = KIF_JSON_Encoder()
        self.assertEqual(
            enc.encode(IRI('x')), '{"class": "IRI", "args": ["x"]}')
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),  # type: ignore
            '"2024-02-06 00:00:00"')
        self.assertEqual(enc.encode(
            decimal.Decimal(0)), '"0"')  # type: ignore
        self.assertEqual(enc.encode(
            decimal.Decimal(3.5)), '"3.5"')  # type: ignore
        self.assertEqual(
            enc.encode(Filter.SnakMask.ALL), '"7"')        # type: ignore
        self.assertRaises(EncoderError, enc.encode, set())  # type: ignore

    def test_sexp_encoder_extensions(self) -> None:
        from kif_lib.model.kif_object import KIF_SExpEncoder
        enc = KIF_SExpEncoder()
        self.assertEqual(enc.encode(PreferredRank()), 'PreferredRank')
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),     # type: ignore
            '2024-02-06 00:00:00')                         # type: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(0)), '0')  # type: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(3.5)), '3.5')       # type: ignore
        self.assertEqual(
            enc.encode(Filter.SnakMask.ALL), '7')          # type: ignore
        self.assertRaises(EncoderError, enc.encode, set())  # type: ignore


if __name__ == '__main__':
    Test.main()
