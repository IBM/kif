# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any, ClassVar, Iterable
from .abc import Store


class EmptyStore(
        Store,
        store_name='empty',
        store_description='Empty store'
):
    """Empty store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
    """

    @dataclasses.dataclass
    class Options(Store.Options, name='empty'):
        """Empty store options."""

        _v_best_ranked: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_EMPTY_STORE_BEST_RANKED',), None)

        _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_EMPTY_STORE_DEBUG',), None)

        _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_EMPTY_STORE_DISTINCT',), None)

        _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_EMPTY_STORE_MAX_LIMIT',), None)

        _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_EMPTY_STORE_LIMIT',), None)

        _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_EMPTY_STORE_LOOKAHEAD',), None)

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

    def __init__(self, store_name: str, *args: Any, **kwargs: Any) -> None:
        assert store_name == self.store_name
        super().__init__(*args, **kwargs)
