# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Context, Filter, Item, Property
from kif_lib.context import Section
from kif_lib.typing import Callable, Final

from ....tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.compiler.sparql.mapping.wikidata

    def test_blazegraph(self) -> None:
        self._test_option_bool(
            section=self.section,
            name='blazegraph',
            envvars=['KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_BLAZEGRAPH'])

    def test_strict(self) -> None:
        self._test_option_bool(
            section=self.section,
            name='strict',
            envvars=['KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_STRICT'])

    def test_truthy(self) -> None:
        self._test_option(
            section=self.section,
            name='truthy',
            values=[
                (Filter.ITEM.value, Filter.ITEM),
                (Property.datatype, Filter.PROPERTY),
                (Filter.ENTITY, Filter.ENTITY)],
            type_error={})


if __name__ == '__main__':
    Test.main()
