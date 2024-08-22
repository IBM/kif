# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.store.sparql_results import SPARQL_Results

from .tests import TestCase


class TestStoreSPARQL_Results(TestCase):

    def test__init__(self) -> None:
        res = SPARQL_Results(
            {'head': {'vars': {}}, 'results': {'bindings': {}}})
        self.assertIsInstance(res, SPARQL_Results)


if __name__ == '__main__':
    TestStoreSPARQL_Results.main()
