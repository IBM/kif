# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section

from ...tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.model.value.text

    def test_language(self) -> None:
        self._test_option_str(
            section=self.section,
            name='language',
            envvars=['KIF_MODEL_VALUE_TEXT_LANGUAGE', 'KIF_LANGUAGE'])


if __name__ == '__main__':
    Test.main()
