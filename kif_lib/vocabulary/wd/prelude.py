# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...model import Entity
from ...typing import Final, Optional
from .registry import WikidataEntityRegistry

_registry: Final[WikidataEntityRegistry] = WikidataEntityRegistry()
Q = _registry.Q  # type: ignore
P = _registry.P  # type: ignore
L = _registry.L  # type: ignore


def get_entity_label(entity: Entity) -> Optional[str]:
    return _registry.get_entity_label(entity)
