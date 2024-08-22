# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Term

from ...tests import kif_TermTestCase


class Test(kif_TermTestCase):

    def test__init__(self):
        self.assert_abstract_class(Term)


if __name__ == '__main__':
    Test.main()
