# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, IRI_Datatype
from kif_lib.typing import assert_type

from ...tests import kif_DatatypeTestCase


class Test(kif_DatatypeTestCase):

    def test_value_class(self) -> None:
        assert_type(IRI_Datatype.value_class, type[IRI])

    def test_check(self) -> None:
        assert_type(IRI_Datatype.check(IRI_Datatype()), IRI_Datatype)
        self._test_check(IRI_Datatype)

    def test__init__(self) -> None:
        assert_type(IRI_Datatype(), IRI_Datatype)
        self._test__init__(IRI_Datatype, self.assert_iri_datatype)


if __name__ == '__main__':
    Test.main()
