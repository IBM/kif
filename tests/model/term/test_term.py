# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Value

from ...tests import kif_ObjectTestCase


class Test(kif_ObjectTestCase):

    def test__init__(self):
        self.assert_abstract_class(Value)


if __name__ == '__main__':
    Test.main()
