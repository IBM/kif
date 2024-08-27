# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import OpenTerm

from ...tests import OpenTermTestCase


class Test(OpenTermTestCase):

    def test__init__(self) -> None:
        self.assert_abstract_class(OpenTerm)


if __name__ == '__main__':
    Test.main()
