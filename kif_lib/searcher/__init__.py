# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .abc import Searcher
from .empty import EmptySearcher

__all__ = (
    'EmptySearcher',
    'Searcher',
)
