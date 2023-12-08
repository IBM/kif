# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import Normal, NormalRank

from .tests import kif_TestCase, main


class TestModelNormalRank(kif_TestCase):

    def test__init__(self):
        self.assert_normal_rank(NormalRank())
        self.assert_normal_rank(Normal)


if __name__ == '__main__':
    main()
