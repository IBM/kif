# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Entity, EntityTemplate, EntityVariable, IRI, Item
from kif_lib.typing import assert_type

from ...tests import kif_EntityTestCase


class Test(kif_EntityTestCase):

    def test_template_class(self) -> None:
        assert_type(Entity.template_class, type[EntityTemplate])

    def test_variable_class(self) -> None:
        assert_type(Entity.variable_class, type[EntityVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(Entity, 0, Entity.check)
        self.assert_raises_check_error(Entity, {}, Entity.check)
        self.assert_raises_check_error(Entity, 'x', Entity.check)
        self.assert_raises_check_error(Entity, IRI('x'), Entity.check)
        # success
        assert_type(Entity.check(Item('x')), Entity)
        self.assertEqual(Entity.check(Item('x')), Item('x'))

    def test__init__(self):
        self.assert_abstract_class(Entity)


if __name__ == '__main__':
    Test.main()
