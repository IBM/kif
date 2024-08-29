# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Variable
from kif_lib.typing import TypeVar
from kif_lib.vocabulary import wd

from ...tests import WikidataSPARQL_StoreTestCase

T = TypeVar('T')


class Test(WikidataSPARQL_StoreTestCase):

    def test_subject_is_var(self) -> None:
        kb = self.new_Store()
        # x shares border with Brazil
        self.assert_it_contains(
            kb.match(wd.shares_border_with(Variable('x'), wd.Brazil)),
            wd.shares_border_with(wd.Argentina, wd.Brazil),
            wd.shares_border_with(wd.Bolivia, wd.Brazil),
            wd.shares_border_with(wd.Colombia, wd.Brazil),
            wd.shares_border_with(wd.France, wd.Brazil),
            wd.shares_border_with(wd.French_Guiana, wd.Brazil),
            wd.shares_border_with(wd.Guyana, wd.Brazil),
            wd.shares_border_with(wd.Uruguay, wd.Brazil),
            wd.shares_border_with(wd.Venezuela, wd.Brazil))
        # x instance of Wikidata property for physical quantities
        self.assert_it_contains(
            kb.match(wd.instance_of(
                Variable('x'), wd.Wikidata_property_for_physical_quantities)),
            wd.instance_of(
                wd.mass, wd.Wikidata_property_for_physical_quantities))
        # x homograph lexeme "change"
        self.assert_it_contains(
            kb.match(wd.homograph_lexeme(Variable('x'), wd.L(33))),
            wd.homograph_lexeme(wd.L(1259), wd.L(33)))


if __name__ == '__main__':
    Test.main()
