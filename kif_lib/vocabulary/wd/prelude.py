# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib

from typing_extensions import deprecated

from ... import namespace as NS
from ...context import Context
from ...model import (
    AliasProperty,
    Datatype,
    DescriptionProperty,
    Item,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
    Property,
    TDatatype,
    TItem,
    TProperty,
    TText,
)
from ...typing import cast, Final

__all__ = (
    'alias',
    'description',
    'get_label',                # deprecated
    'L',
    'label',
    'language',
    'lemma',
    'lexical_category',
    'P',
    'Q',
)

_CTX: Final[Context] = Context.top()


def _get_vocabulary_wd_dir() -> pathlib.Path:
    from importlib import util
    spec = util.find_spec(__name__)
    assert spec is not None
    assert spec.origin is not None
    return pathlib.Path(cast(str, spec.origin)).parent


def _get_item_cache() -> pathlib.Path | None:
    path = _CTX.options.vocabulary.wd.item_cache
    if path is not None:
        assert isinstance(path, pathlib.Path)
        if path.is_absolute():
            return path
        else:
            return _get_vocabulary_wd_dir() / path
    else:
        return None


def _get_property_cache() -> pathlib.Path | None:
    path = _CTX.options.vocabulary.wd.property_cache
    if path is not None:
        assert isinstance(path, pathlib.Path)
        if path.is_absolute():
            return path
        else:
            return _get_vocabulary_wd_dir() / path
    else:
        return None


def _reload_property_cache(path: pathlib.Path | None = None) -> None:
    try:
        path = path or _get_property_cache()
        if path is None:
            return
        assert path is not None
        with open(path, encoding='utf-8') as fp:
            for line in fp.readlines():
                _, uri, datatype_uri, label_en, inverse_uri = (
                    line[:-1].split('\t'))
                dt = Datatype.check(datatype_uri)
                prop = Property(uri, dt)
                _CTX.registry.set_datatype(prop, dt)
                _CTX.registry.set_label(prop, label_en)
                if inverse_uri:
                    iprop = Property(inverse_uri, dt)
                    _CTX.registry.set_inverse(prop, iprop)
    except FileNotFoundError:
        pass


def P(
        name: int | str,
        label: TText | None = None,
        datatype: TDatatype | None = None,
        inverse: TProperty | None = None
) -> Property:
    if isinstance(name, str) and name[0] == 'P':
        name = str(NS.WD[name])
    else:
        name = str(NS.WD[f'P{name}'])
    return _CTX.registry.make_property(name, label, datatype, inverse)


def Q(
        name: int | str,
        label: TText | None = None
) -> Item:
    if isinstance(name, str) and name[0] == 'Q':
        name = str(NS.WD[name])
    else:
        name = str(NS.WD[f'Q{name}'])
    return _CTX.registry.make_item(name, label)


def L(
        name: int | str,
        lemma: TText | None = None,
        category: TItem | None = None,
        language: TItem | None = None
) -> Lexeme:
    if isinstance(name, str) and name[0] == 'L':
        name = str(NS.WD[name])
    else:
        name = str(NS.WD[f'L{name}'])
    return _CTX.registry.make_lexeme(name, lemma, category, language)


# Aliases for pseudo-properties.
label = LabelProperty()
alias = AliasProperty()
description = DescriptionProperty()
lemma = LemmaProperty()
lexical_category = LexicalCategoryProperty()
language = LanguageProperty()

# Load property cache.
_reload_property_cache()


@deprecated('get_label() is deprecated; use ENTITY.label instead')
def get_label(
        entity: Item | Property,
        default: str | None = None
) -> str | None:
    label = _CTX.registry.get_label(entity, default)
    if label is not None:
        return label.content
    else:
        return default
