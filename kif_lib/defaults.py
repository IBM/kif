# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from .typing import Final

KIF_MODEL_TEXT_DEFAULT_LANGUAGE: Final[str] = os.getenv(
    'KIF_MODEL_TEXT_DEFAULT_LANGUAGE', 'en')
