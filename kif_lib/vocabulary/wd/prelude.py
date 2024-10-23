# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...model import (
    AliasProperty,
    DescriptionProperty,
    Entity,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    LexicalCategoryProperty,
    Property,
)
from ...typing import Final
from .registry import WikidataEntityRegistry

__all__ = (
    'alias',
    'description',
    'get_inverse',
    'get_label',
    'L',
    'label',
    'language',
    'lemma',
    'lexical_category',
    'P',
    'Q',
)

_registry: Final[WikidataEntityRegistry] = WikidataEntityRegistry()
Q = _registry.Q  # type: ignore
P = _registry.P  # type: ignore
L = _registry.L  # type: ignore

# Aliases for pseudo-properties.
label = LabelProperty()
alias = AliasProperty()
description = DescriptionProperty()
lemma = LemmaProperty()
lexical_category = LexicalCategoryProperty()
language = LanguageProperty()


def get_label(entity: Entity, default: str | None = None) -> str | None:
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
        default: Property | None = None
) -> Property | None:
    """Gets the inverse property of `property` (if any).

    If entity has no inverse property registered, returns `default`.

    Parameters:
       default: Default inverse property.

    Returns:
       Property.
    """
    return _registry.get_inverse(property, default)
