# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Generator,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Set,
)
from types import ModuleType, TracebackType
from typing import (
    BinaryIO,
    cast,
    ClassVar,
    Final,
    Generic,
    IO,
    NoReturn,
    Optional,
    TextIO,
    Union,
)

from typing_extensions import (
    Any,
    assert_type,
    Literal,
    overload,
    override,
    Protocol,
    Self,
    TypeAlias,
    TypedDict,
    TypeVar,
)

# Common aliases.
Location: TypeAlias = Union[Callable[..., Any], str]

__all__ = (
    'Any',
    'assert_type',
    'AsyncIterator',
    'Awaitable',
    'BinaryIO',
    'Callable',
    'cast',
    'ClassVar',
    'Collection',
    'Final',
    'Generator',
    'Generic',
    'Hashable',
    'IO',
    'Iterable',
    'Iterator',
    'Literal',
    'Location',
    'Mapping',
    'ModuleType',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'NoReturn',
    'Optional',
    'overload',
    'override',
    'Protocol',
    'Self',
    'Sequence',
    'Set',
    'TextIO',
    'TracebackType',
    'TypeAlias',
    'TypedDict',
    'TypeVar',
    'Union',
)
