# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Snak

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_mask_check(self):
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Snak.Mask.check, 'abc')
        self.assertEqual(Snak.Mask.check(0), Snak.Mask(0))
        self.assertEqual(Snak.Mask.check(Snak.VALUE_SNAK), Snak.VALUE_SNAK)


if __name__ == '__main__':
    Test.main()
