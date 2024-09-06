# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .descriptor import DescriptorTestCase
from .fingerprint import FingerprintTestCase
from .kif_object import KIF_ObjectTestCase
from .set import KIF_ObjectSetTestCase
from .snak import SnakTemplateTestCase, SnakTestCase
from .statement import StatementTemplateTestCase, StatementTestCase
from .term import (
    ClosedTermTestCase,
    OpenTermTestCase,
    TemplateTestCase,
    TermTestCase,
    VariableTestCase,
)
from .value import (
    DatatypeTestCase,
    DataValueTemplateTestCase,
    DataValueTestCase,
    DataValueVariableTestCase,
    DeepDataValueTemplateTestCase,
    DeepDataValueTestCase,
    EntityTemplateTestCase,
    EntityTestCase,
    EntityVariableTestCase,
    ShallowDataValueTemplateTestCase,
    ShallowDataValueTestCase,
    ValueTemplateTestCase,
    ValueTestCase,
    ValueVariableTestCase,
)

__all__ = (
    # kif object
    'KIF_ObjectTestCase',

    # term
    'ClosedTermTestCase',
    'OpenTermTestCase',
    'TemplateTestCase',
    'TermTestCase',
    'VariableTestCase',

    # datatype
    'DatatypeTestCase',

    # value
    'ValueTemplateTestCase',
    'ValueTestCase',
    'ValueVariableTestCase',

    # entity
    'EntityTemplateTestCase',
    'EntityTestCase',
    'EntityVariableTestCase',

    # data value
    'DataValueTemplateTestCase',
    'DataValueTestCase',
    'DataValueVariableTestCase',

    # shallow data value
    'ShallowDataValueTemplateTestCase',
    'ShallowDataValueTestCase',

    # deep data value
    'DeepDataValueTemplateTestCase',
    'DeepDataValueTestCase',

    # snak
    'SnakTemplateTestCase',
    'SnakTestCase',

    # statement
    'StatementTemplateTestCase',
    'StatementTestCase',

    # descriptor
    'DescriptorTestCase',

    # fingerprint
    'FingerprintTestCase',

    # set
    'KIF_ObjectSetTestCase',
)
