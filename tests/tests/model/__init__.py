# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .annotations import RankTestCase
from .descriptor import DescriptorTestCase
from .fingerprint import FingerprintTestCase
from .kif_object import KIF_ObjectTestCase
from .set import KIF_ObjectSetTestCase
from .snak import SnakTemplateTestCase, SnakTestCase, SnakVariableTestCase
from .statement import (
    StatementTemplateTestCase,
    StatementTestCase,
    StatementVariableTestCase,
)
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
    DeepDataValueVariableTestCase,
    EntityTemplateTestCase,
    EntityTestCase,
    EntityVariableTestCase,
    ShallowDataValueTemplateTestCase,
    ShallowDataValueTestCase,
    ShallowDataValueVariableTestCase,
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
    'ShallowDataValueVariableTestCase',

    # deep data value
    'DeepDataValueTemplateTestCase',
    'DeepDataValueTestCase',
    'DeepDataValueVariableTestCase',

    # snak
    'SnakTemplateTestCase',
    'SnakTestCase',
    'SnakVariableTestCase',

    # statement
    'StatementTemplateTestCase',
    'StatementTestCase',
    'StatementVariableTestCase',

    # annotations
    'RankTestCase',

    # descriptor
    'DescriptorTestCase',

    # fingerprint
    'FingerprintTestCase',

    # set
    'KIF_ObjectSetTestCase',
)
