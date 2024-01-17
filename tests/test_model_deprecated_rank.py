# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import Deprecated, DeprecatedRank

from .tests import kif_TestCase, main


class TestModelDeprecatedRank(kif_TestCase):

    def test__init__(self):
        self.assert_deprecated_rank(DeprecatedRank())
        self.assert_deprecated_rank(Deprecated)


if __name__ == '__main__':
    main()
