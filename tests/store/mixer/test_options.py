# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.store import MixerStore
from kif_lib.typing import override

from ..test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.store.mixer

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_MIXER_STORE_DEBUG'])

    @override
    def test_distinct(self) -> None:
        self._test_distinct(['KIF_MIXER_STORE_DISTINCT'])

    @override
    def test_max_distinct_window_size(self) -> None:
        self._test_max_distinct_window_size(
            ['KIF_MIXER_STORE_MAX_DISTINCT_WINDOW_SIZE'])

    @override
    def test_distinct_window_size(self) -> None:
        self._test_distinct_window_size(
            ['KIF_MIXER_STORE_DISTINCT_WINDOW_SIZE'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_MIXER_STORE_MAX_LIMIT'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_MIXER_STORE_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_MIXER_STORE_LOOKAHEAD'])

    @override
    def test_omega(self) -> None:
        self._test_omega(['KIF_MIXER_STORE_OMEGA'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_MIXER_STORE_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_MIXER_STORE_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_MIXER_STORE_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_MIXER_STORE_TIMEOUT'])

    def test_sync_flags(self) -> None:
        self._test_option(
            section=self.section,
            name='sync_flags',
            values=[
                (0, MixerStore._mk_sync_flags(0)),
                (MixerStore.DEBUG | MixerStore.LIMIT,
                 MixerStore.DEBUG | MixerStore.LIMIT)],
            type_error={})


if __name__ == '__main__':
    Test.main()
