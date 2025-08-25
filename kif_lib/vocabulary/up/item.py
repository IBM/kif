# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .prelude import taxonomy

# autopep8: off
# flake8: noqa

Bacteria = taxonomy(2, 'Bacteria')
Cellvibrio = taxonomy(10, 'Cellvibrio')

__all__ = (
    'Bacteria',
    'Cellvibrio',
)
