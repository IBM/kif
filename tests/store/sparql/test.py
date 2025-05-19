# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio

from kif_lib import Store
from kif_lib.typing import Any
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls, **kwargs: Any) -> Store:
        from ..wdqs.test_filter import Test as WDQS_TestFilter
        return WDQS_TestFilter.KB(**kwargs)

    def test_afilter_httpx_2959_issue(self) -> None:
        ###
        # Tests the use of async requests in multiple event loop.  For this
        # to work, we must use the header {'Connection': 'close'}, which
        # makes httpx not to store the underlying connection in the
        # connection pool.  See
        # <https://github.com/encode/httpx/discussions/2959>.
        ###
        kb = self.KB(headers={'Connection': 'close'})

        async def f():
            it = kb.afilter(
                wd.Brazil, wd.shares_border_with, wd.Argentina, limit=1)
            self.assertEqual(
                await it.__anext__(),
                wd.shares_border_with(wd.Brazil, wd.Argentina))

        for i in range(3):
            asyncio.run(f())


if __name__ == '__main__':
    Test.main()
