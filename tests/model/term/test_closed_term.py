# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ClosedTerm

from ...tests import ClosedTermTestCase


class Test(ClosedTermTestCase):

    def test__init__(self) -> None:
        self.assert_abstract_class(ClosedTerm)


if __name__ == '__main__':
    Test.main()
