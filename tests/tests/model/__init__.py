# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .snak import kif_SnakTemplateTestCase, kif_SnakTestCase
from .statement import kif_StatementTemplateTestCase, kif_StatementTestCase
from .template import kif_TemplateTestCase
from .value import (
    kif_DatatypeTestCase,
    kif_DataValueTemplateTestCase,
    kif_DataValueTestCase,
    kif_DeepDataValueTemplateTestCase,
    kif_DeepDataValueTestCase,
    kif_EntityTemplateTestCase,
    kif_EntityTestCase,
    kif_ShallowDataValueTemplateTestCase,
    kif_ShallowDataValueTestCase,
    kif_ValueTemplateTestCase,
    kif_ValueTestCase,
)
from .variable import kif_VariableTestCase

__all__ = (
    # template
    'kif_TemplateTestCase',

    # variable
    'kif_VariableTestCase',

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

    # snak
    'kif_SnakTemplateTestCase',
    'kif_SnakTestCase',

    # statement
    'kif_StatementTemplateTestCase',
    'kif_StatementTestCase',
)
