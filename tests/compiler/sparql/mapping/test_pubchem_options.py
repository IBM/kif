# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ....tests import OptionsTestCase


class Test(OptionsTestCase):

    def test_normalize_casrn(self) -> None:
        self._test_option_bool(
            section=lambda ctx: ctx.options.compiler.sparql.mapping.pubchem,
            name='normalize_casrn',
            envvars=['KIF_COMPILER_SPARQL_MAPPING_PUBCHEM_NORMALIZE_CASRN'])


if __name__ == '__main__':
    Test.main()
