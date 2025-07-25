# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .abc import Search
from .empty import EmptySearch

__all__ = (
    'EmptySearch',
    'Search',
)
