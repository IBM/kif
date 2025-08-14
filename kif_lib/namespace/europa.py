# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class Europa:
    """The Europa namespace."""

    EUROPA: Final[Namespace] = Namespace('http://data.europa.eu/')
    DATASET: Final[Namespace] = Namespace(EUROPA['88u/dataset/'])

    namespaces: Final[dict[str, Namespace]] = {
        str(DATASET): DATASET,
    }
