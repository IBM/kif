# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib.namespace import Namespace

from kif.namespace import WIKIBASE, Wikidata

from .tests import kif_TestCase, main


class TestNamespaceWikidata(kif_TestCase):

    def assert_namespace_value(self, ns, val):
        self.assertIsInstance(ns, Namespace)
        self.assertIsInstance(val, str)
        self.assertEqual(str(ns), val)

    def test_namespace(self):
        wd = 'http://www.wikidata.org/'
        self.assert_namespace_value(
            Wikidata.WIKIDATA, wd)
        self.assert_namespace_value(
            Wikidata.P, f'{wd}prop/')
        self.assert_namespace_value(
            Wikidata.PQ, f'{wd}prop/qualifier/')
        self.assert_namespace_value(
            Wikidata.PQN, f'{wd}prop/qualifier/value-normalized/')
        self.assert_namespace_value(
            Wikidata.PQV, f'{wd}prop/qualifier/value/')
        self.assert_namespace_value(
            Wikidata.PR, f'{wd}prop/reference/')
        self.assert_namespace_value(
            Wikidata.PRN, f'{wd}prop/reference/value-normalized/')
        self.assert_namespace_value(
            Wikidata.PRV, f'{wd}prop/reference/value/')
        self.assert_namespace_value(
            Wikidata.PS, f'{wd}prop/statement/')
        self.assert_namespace_value(
            Wikidata.PSN, f'{wd}prop/statement/value-normalized/')
        self.assert_namespace_value(
            Wikidata.PSV, f'{wd}prop/statement/value/')
        self.assert_namespace_value(
            Wikidata.WD, f'{wd}entity/')
        self.assert_namespace_value(
            Wikidata.WDATA, f'{wd}wiki/Special:EntityData/')
        self.assert_namespace_value(
            Wikidata.WDGENID, f'{wd}.well-known/genid/')
        self.assert_namespace_value(
            Wikidata.WDNO, f'{wd}prop/novalue/')
        self.assert_namespace_value(
            Wikidata.WDREF, f'{wd}reference/')
        self.assert_namespace_value(
            Wikidata.WDS, f'{wd}entity/statement/')
        self.assert_namespace_value(
            Wikidata.WDT, f'{wd}prop/direct/')
        self.assert_namespace_value(
            Wikidata.WDV, f'{wd}value/')

    def test_is_wikidata_uri(self):
        self.assertTrue(Wikidata.is_wikidata_uri(Wikidata.P))
        self.assertTrue(Wikidata.is_wikidata_uri(Wikidata.P.value))
        self.assertTrue(Wikidata.is_wikidata_uri(str(Wikidata.P)))
        self.assertFalse(Wikidata.is_wikidata_uri('http://www.x.org/'))
        self.assertFalse(Wikidata.is_wikidata_uri('abc'))

    def test_split_wikidata_uri(self):
        # bad argument
        self.assertRaises(
            ValueError, Wikidata.split_wikidata_uri,
            'http://www.wikidata.org')
        self.assertRaises(
            ValueError, Wikidata.split_wikidata_uri, 'abc')
        # good arguments
        self.assertEqual(
            Wikidata.split_wikidata_uri(Wikidata.P),
            (Wikidata.P, ''))
        self.assertEqual(
            Wikidata.split_wikidata_uri(Wikidata.WD.Q155),
            (Wikidata.WD, 'Q155'))
        self.assertEqual(
            Wikidata.split_wikidata_uri(Wikidata.WDS.abc),
            (Wikidata.WDS, 'abc'))

    def test_get_wikidata_namespace(self):
        # bad argument
        self.assertRaises(
            ValueError, Wikidata.get_wikidata_namespace, 'x')
        # good arguments
        self.assertEqual(
            Wikidata.get_wikidata_namespace(Wikidata.WD.Q155),
            Wikidata.WD)
        self.assertEqual(
            Wikidata.get_wikidata_namespace(Wikidata.WDGENID.abc),
            Wikidata.WDGENID)

    def test_get_wikidata_name(self):
        # bad argument
        self.assertRaises(
            ValueError, Wikidata.get_wikidata_name, 'x')
        # good arguments
        self.assertEqual(
            Wikidata.get_wikidata_name(Wikidata.WD.Q155), 'Q155')
        self.assertEqual(
            Wikidata.get_wikidata_name(Wikidata.WDGENID.abc), 'abc')

    def test_is_wd_entity(self):
        self.assertTrue(Wikidata.is_wd_entity(Wikidata.WD.Q155))
        self.assertTrue(Wikidata.is_wd_entity(Wikidata.WD.P31))
        self.assertFalse(Wikidata.is_wd_entity(Wikidata.P.P31))
        self.assertFalse(Wikidata.is_wd_entity(Wikidata.WDS.abc))
        self.assertFalse(Wikidata.is_wd_entity(WIKIBASE.PreferredRank))

    def test_is_wd_item(self):
        self.assertTrue(Wikidata.is_wd_item(Wikidata.WD.Q155))
        self.assertFalse(Wikidata.is_wd_item(Wikidata.WD.P31))
        self.assertFalse(Wikidata.is_wd_item(Wikidata.P.P31))
        self.assertFalse(Wikidata.is_wd_item(Wikidata.WDS.abc))
        self.assertFalse(Wikidata.is_wd_item(WIKIBASE.PreferredRank))

    def test_is_wd_property(self):
        self.assertFalse(Wikidata.is_wd_property(Wikidata.WD.Q155))
        self.assertTrue(Wikidata.is_wd_property(Wikidata.WD.P31))
        self.assertFalse(Wikidata.is_wd_property(Wikidata.P.P31))
        self.assertFalse(Wikidata.is_wd_property(Wikidata.WDS.abc))
        self.assertFalse(Wikidata.is_wd_property(WIKIBASE.PreferredRank))

    def test_is_wd_some_value(self):
        self.assertTrue(Wikidata.is_wd_some_value(Wikidata.WDGENID.abc))
        self.assertFalse(Wikidata.is_wd_some_value(Wikidata.WD.Q155))
        self.assertFalse(Wikidata.is_wd_some_value(Wikidata.WD.P31))
        self.assertFalse(Wikidata.is_wd_some_value(Wikidata.P.P31))
        self.assertFalse(Wikidata.is_wd_some_value(Wikidata.WDS.abc))
        self.assertFalse(Wikidata.is_wd_some_value(WIKIBASE.PreferredRank))

    def test_is_wikibase_preferred_rank(self):
        self.assertTrue(Wikidata.is_wikibase_preferred_rank(
            WIKIBASE.PreferredRank))
        self.assertFalse(Wikidata.is_wikibase_preferred_rank(
            WIKIBASE.NormalRank))
        self.assertFalse(Wikidata.is_wikibase_preferred_rank(
            Wikidata.WD.Q155))

    def test_is_wikibase_normal_rank(self):
        self.assertTrue(Wikidata.is_wikibase_normal_rank(
            WIKIBASE.NormalRank))
        self.assertFalse(Wikidata.is_wikibase_normal_rank(
            WIKIBASE.PreferredRank))
        self.assertFalse(Wikidata.is_wikibase_normal_rank(
            Wikidata.WD.Q155))

    def test_is_wikibase_deprecated_rank(self):
        self.assertTrue(Wikidata.is_wikibase_deprecated_rank(
            WIKIBASE.DeprecatedRank))
        self.assertFalse(Wikidata.is_wikibase_deprecated_rank(
            WIKIBASE.PreferredRank))
        self.assertFalse(Wikidata.is_wikibase_deprecated_rank(
            Wikidata.WD.Q155))


if __name__ == '__main__':
    main()
