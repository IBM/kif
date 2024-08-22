# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import OpenTerm

from ...tests import kif_OpenTermTestCase


class Test(kif_OpenTermTestCase):

    def test__init__(self):
        self.assert_abstract_class(OpenTerm)


if __name__ == '__main__':
    Test.main()
