# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...model import Entity, Property
from ...typing import Final, Optional
from .registry import WikidataEntityRegistry

__all__ = (
    'get_inverse',
    'get_label',
    'L',
    'P',
    'Q',
)

_registry: Final[WikidataEntityRegistry] = WikidataEntityRegistry()
Q = _registry.Q  # type: ignore
P = _registry.P  # type: ignore
L = _registry.L  # type: ignore


def get_label(entity: Entity, default: Optional[str] = None) -> Optional[str]:
    """Gets the registered label of `entity`.

    If entity has no label registered, returns `default`.

    Parameters:
       default: Default label.

    Returns:
       Label.
    """
    return _registry.get_label(entity, default)


def get_inverse(
        property: Property,
        default: Optional[Property] = None
) -> Optional[Property]:
    """Gets the inverse property of `property` (if any).

    If entity has no inverse property registered, returns `default`.

    Parameters:
       default: Default inverse property.

    Returns:
       Property.
    """
    return _registry.get_inverse(property, default)
