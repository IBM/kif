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
    TValueSnak,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    VTValueSnak,
    VValueSnak,
)

__all__ = (
    # snak
    'Snak',
    'SnakTemplate',
    'SnakVariable',
    'VSnak',
    'VVSnak',

    # value snak
    'TValueSnak',
    'ValueSnak',
    'ValueSnakTemplate',
    'ValueSnakVariable',
    'VTValueSnak',
    'VValueSnak',

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
