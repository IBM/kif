# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys
from collections.abc import (
    Callable,
    Collection,
    Generator,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
    Set,
)
from typing import (
    Any,
    BinaryIO,
    cast,
    Final,
    IO,
    NoReturn,
    Optional,
    TextIO,
    TypeVar,
    Union,
)

from typing_extensions import override

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

__all__ = (
    'Any',
    'BinaryIO',
    'Callable',
    'cast',
    'Collection',
    'Final',
    'Generator',
    'Hashable',
    'IO',
    'Iterable',
    'Iterator',
    'Mapping',
    'NoReturn',
    'Optional',
    'override',
    'Sequence',
    'Set',
    'TextIO',
    'TypeAlias',
    'TypeVar',
    'Union',
)
