# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Entity, EntityTemplate
from kif_lib.typing import assert_type

from ...tests import EntityTemplateTestCase


class Test(EntityTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(EntityTemplate.object_class, type[Entity])
        self.assertIs(EntityTemplate.object_class, Entity)

    def test__init__(self) -> None:
        self.assert_abstract_class(EntityTemplate)


if __name__ == '__main__':
    Test.main()
