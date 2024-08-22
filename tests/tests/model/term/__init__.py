# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .template import kif_TemplateTestCase
from .term import (
    kif_ClosedTermTestCase,
    kif_OpenTermTestCase,
    kif_TermTestCase,
)
from .variable import kif_VariableTestCase

__all__ = (
    'kif_ClosedTermTestCase',
    'kif_OpenTermTestCase',
    'kif_TemplateTestCase',
    'kif_TermTestCase',
    'kif_VariableTestCase',
)
