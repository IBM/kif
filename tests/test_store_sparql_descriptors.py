# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Lexeme, Property, Store, Text
import kif_lib.vocabulary as wd


from .tests import (
    kif_StoreTestCase,
    main,
    skip_if_not_set,
    WIKIDATA,
)

skip_if_not_set('WIKIDATA')


class TestStoreSPARQL_Descriptors(kif_StoreTestCase):

    @classmethod
    def new_Store_SPARQL(self, iri=WIKIDATA, **kwargs):
        return Store('sparql', iri, **kwargs)

# -- get_descriptor --------------------------------------------------------

    def test_get_descriptor_sanity(self):
        kb = self.new_Store_SPARQL()
        self.sanity_check_get_descriptor(kb)

    def test_get_descriptor_single_entity(self):
        kb = self.new_Store_SPARQL()
        ds = list(kb.get_descriptor(wd.IBM))
        self.assertEqual(len(ds), 1)
        ((item, desc),) = ds
        self.assertEqual(item, wd.IBM)
        self.assertEqual(desc.label, Text('IBM'))
        self.assertIn(Text('I.B.M.'), desc.aliases)
        self.assertEqual(
            desc.description,
            Text('American multinational technology corporation'))

    def test_get_descriptor_multiple_entities(self):
        kb = self.new_Store_SPARQL()
        ds = list(kb.get_descriptor([
            wd.IBM, Item('x'),
            wd.L(4471), Lexeme('x'),
            wd.mass, Property('x')]))
        self.assertEqual(len(ds), 6)


if __name__ == '__main__':
    main()
