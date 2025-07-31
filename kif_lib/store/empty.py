# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any, ClassVar, Iterable
from .abc import Store, StoreOptions


@dataclasses.dataclass
class EmptyStoreOptions(StoreOptions, name='empty'):
    """Empty store options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_STORE_DEBUG',), None)

    _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_STORE_DISTINCT',), None)

    _v_max_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            (('KIF_EMPTY_STORE_MAX_DISTINCT_WINDOW_SIZE',), None))

    _v_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            (('KIF_EMPTY_STORE_DISTINCT_WINDOW_SIZE',), None))

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_LOOKAHEAD',), None)

    _v_omega: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_OMEGA',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_STORE_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_STORE_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Empty store ===========================================================


class EmptyStore(
        Store[EmptyStoreOptions],
        store_name='empty',
        store_description='Empty store'
):
    """Empty store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
    """

    def __init__(self, store_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(store_name, *args, **kwargs)
