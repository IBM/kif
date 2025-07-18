# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
from collections.abc import (
    AsyncIterable,
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
    Coroutine,
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
    ContextManager,
    Literal,
    NotRequired,
    overload,
    override,
    Protocol,
    Self,
    TypeAlias,
    TypedDict,
    TypeVar,
)

PathLike = os.PathLike

# Common aliases.
Location: TypeAlias = Union[Callable[..., Any], str]
Path: TypeAlias = os.PathLike[str]

__all__ = (
    'Any',
    'assert_type',
    'AsyncIterable',
    'AsyncIterator',
    'Awaitable',
    'BinaryIO',
    'Callable',
    'cast',
    'ClassVar',
    'Collection',
    'ContextManager',
    'Coroutine',
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
    'NotRequired',
    'Optional',
    'overload',
    'override',
    'Path',
    'PathLike',
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
