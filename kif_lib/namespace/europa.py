# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class Europa:
    """The Europa namespace."""

    AUTHORITY: Final[Namespace] = Namespace(
        'http://publications.europa.eu/resource/authority/')

    DATASET: Final[Namespace] = Namespace('http://data.europa.eu/88u/dataset/')
    THEME: Final[Namespace] = Namespace(AUTHORITY['data-theme/'])

    namespaces: Final[dict[str, Namespace]] = {
        str(AUTHORITY): AUTHORITY,
        str(DATASET): DATASET,
        str(THEME): THEME,
    }
