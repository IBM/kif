# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import Any
from .abc import Store


class EmptyStore(Store, store_name='empty', store_description='Empty store'):
    """Empty store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
    """

    def __init__(self, store_name: str, *args, **kwargs: Any) -> None:
        assert store_name == self.store_name
        super().__init__(*args, **kwargs)
