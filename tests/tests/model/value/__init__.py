# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .data_value import kif_DataValueTemplateTestCase, kif_DataValueTestCase
from .datatype import kif_DatatypeTestCase
from .deep_data_value import (
    kif_DeepDataValueTemplateTestCase,
    kif_DeepDataValueTestCase,
)
from .entity import kif_EntityTemplateTestCase, kif_EntityTestCase
from .shallow_data_value import (
    kif_ShallowDataValueTemplateTestCase,
    kif_ShallowDataValueTestCase,
)
from .value import kif_ValueTemplateTestCase, kif_ValueTestCase

__all__ = (
    # datatype
    'kif_DatatypeTestCase',

    # value
    'kif_ValueTemplateTestCase',
    'kif_ValueTestCase',

    # entity
    'kif_EntityTemplateTestCase',
    'kif_EntityTestCase',

    # data value
    'kif_DataValueTemplateTestCase',
    'kif_DataValueTestCase',

    # shallow data value
    'kif_ShallowDataValueTemplateTestCase',
    'kif_ShallowDataValueTestCase',

    # deep data value
    'kif_DeepDataValueTemplateTestCase',
    'kif_DeepDataValueTestCase',
)
