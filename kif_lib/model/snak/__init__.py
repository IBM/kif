# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .no_value_snak import (
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    VNoValueSnak,
    VVNoValueSnak,
)
from .snak import Snak, SnakTemplate, SnakVariable, VSnak, VVSnak
from .some_value_snak import (
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    VSomeValueSnak,
    VVSomeValueSnak,
)
from .value_snak import (
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    VValueSnak,
    VVValueSnak,
)

__all__ = (
    # snak
    'Snak',
    'SnakTemplate',
    'SnakVariable',
    'VSnak',
    'VVSnak',

    # value snak
    'ValueSnak',
    'ValueSnakTemplate',
    'ValueSnakVariable',
    'VValueSnak',
    'VVValueSnak',

    # some value snak
    'SomeValueSnak',
    'SomeValueSnakTemplate',
    'SomeValueSnakVariable',
    'VSomeValueSnak',
    'VVSomeValueSnak',

    # no value snak
    'NoValueSnak',
    'NoValueSnakTemplate',
    'NoValueSnakVariable',
    'VNoValueSnak',
    'VVNoValueSnak',
)
