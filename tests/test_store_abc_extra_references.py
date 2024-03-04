# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Property, ReferenceRecord, ReferenceRecordSet

from .tests import kif_EmptyStoreTestCase


class TestStoreExtraReferences(kif_EmptyStoreTestCase):

    def test_extra_references_default(self):
        kb = self.new_Store()
        self.assertEqual(kb.default_extra_references, ReferenceRecordSet())

    ref1 = ReferenceRecord(
        Property('p')('abc'),
        Property('q')(Property('p')))

    ref2 = ReferenceRecord(Property('r')(0))

    ref3 = ReferenceRecord()

    refs = ReferenceRecordSet(ref1, ref2, ref3)

    def test_extra_references_init(self):
        kb = self.new_Store()
        self.assertEqual(kb.extra_references, kb.default_extra_references)
        kb = self.new_Store(extra_references=list(self.refs))
        self.assertEqual(kb.extra_references, self.refs)
        kb = self.new_Store(extra_references=[self.ref3])
        self.assertEqual(kb.extra_references, ReferenceRecordSet(self.ref3))
        kb = self.new_Store(extra_references=None)
        self.assertEqual(kb.extra_references, kb.default_extra_references)

    def test_get_extra_references(self):
        kb = self.new_Store()
        self.assertEqual(
            kb.get_extra_references(), kb.default_extra_references)
        self.assertEqual(kb.get_extra_references(self.refs), self.refs)
        kb = self.new_Store(extra_references=ReferenceRecordSet())
        self.assertEqual(
            kb.get_extra_references(self.refs), ReferenceRecordSet())
        kb = self.new_Store(extra_references=None)
        self.assertEqual(kb.get_extra_references(self.refs), self.refs)
        kb = self.new_Store(extra_references=self.refs)
        self.assertEqual(
            kb.get_extra_references(ReferenceRecordSet()), self.refs)

    def test_set_extra_references(self):
        kb = self.new_Store()
        self.assert_raises_bad_argument(
            TypeError, 1, 'references', 'expected KIF_ObjectSet, got int',
            kb.set_extra_references, 0)
        self.assertEqual(
            kb.get_extra_references(), kb.default_extra_references)
        kb.extra_references = self.refs
        self.assertEqual(kb.extra_references, self.refs)
        kb.extra_references = None
        self.assertEqual(kb.extra_references, kb.default_extra_references)
        kb.extra_references = ReferenceRecordSet()
        self.assertEqual(kb.extra_references, ReferenceRecordSet())
        kb.extra_references = self.refs
        kb.set_extra_references()
        self.assertEqual(kb.extra_references, kb.default_extra_references)
        kb.set_extra_references(self.refs)
        self.assertEqual(kb.extra_references, self.refs)


if __name__ == '__main__':
    TestStoreExtraReferences.main()
