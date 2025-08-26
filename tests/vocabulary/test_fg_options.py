# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.vocabulary.fg

    def test_resolver(self) -> None:
        self._test_option_iri(
            section=self.section,
            name='resolver',
            envvars=['KIF_VOCABULARY_FG_RESOLVER', 'FACTGRID'],
            optional=True)


if __name__ == '__main__':
    Test.main()
