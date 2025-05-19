# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio

from kif_lib import ExternalId, Graph, Preferred, Quantity, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        kb = Store('jsonl-reader', 'tests/data/benzene.jsonl')
        expected = set(Store('rdf', 'tests/data/benzene.ttl').filter(
            annotated=True))
        self.assertEqual(set(kb.filter(annotated=True)), expected)
        loop = asyncio.get_event_loop()

        async def afilter():
            return {stmt async for stmt in kb.afilter(annotated=True)}
        self.assertEqual(loop.run_until_complete(afilter()), expected)


if __name__ == '__main__':
    Test.main()
