# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Preferred, PreferredRank

from .tests import kif_TestCase, main


class TestModelPreferredRank(kif_TestCase):

    def test__init__(self):
        self.assert_preferred_rank(PreferredRank())
        self.assert_preferred_rank(Preferred)


if __name__ == '__main__':
    main()
