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
    IRI,
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
from ...typing import cast

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
    'reload',
)


def _get_vocabulary_wd_dir() -> pathlib.Path:
    from importlib import util
    spec = util.find_spec(__name__)
    assert spec is not None
    assert spec.origin is not None
    return pathlib.Path(cast(str, spec.origin)).parent


def _get_item_cache(context: Context | None = None) -> pathlib.Path | None:
    ctx = Context.top(context)
    path = ctx.options.vocabulary.wd.item_cache
    if path is not None:
        assert isinstance(path, pathlib.Path)
        if path.is_absolute():
            return path
        else:
            return _get_vocabulary_wd_dir() / path
    else:
        return None


def _get_property_cache(
        context: Context | None = None
) -> pathlib.Path | None:
    ctx = Context.top(context)
    path = ctx.options.vocabulary.wd.property_cache
    if path is not None:
        assert isinstance(path, pathlib.Path)
        if path.is_absolute():
            return path
        else:
            return _get_vocabulary_wd_dir() / path
    else:
        return None


def _reload_property_cache(
        path: pathlib.Path | None = None,
        context: Context | None = None
) -> None:
    ctx = Context.top(context)
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
                iprop = Property(inverse_uri, dt) if inverse_uri else None
                prop = Property(uri, dt)
                assert ctx.entities.register(
                    prop, range=dt, label=label_en, inverse=iprop) == prop
    except FileNotFoundError:
        pass


def P(
        name: int | str,
        label: TText | None = None,
        datatype: TDatatype | None = None,
        inverse: TProperty | None = None,
        context: Context | None = None
) -> Property:
    ctx = Context.top(context)
    if isinstance(name, str) and name[0] == 'P':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'P{name}']))
    return ctx.entities.register(
        Property(iri), label=label, range=datatype, inverse=inverse)


def Q(
        name: int | str,
        label: TText | None = None,
        context: Context | None = None
) -> Item:
    ctx = Context.top(context)
    if isinstance(name, str) and name[0] == 'Q':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'Q{name}']))
    return ctx.entities.register(Item(iri), label=label)


def L(
        name: int | str,
        lemma: TText | None = None,
        category: TItem | None = None,
        language: TItem | None = None,
        context: Context | None = None
) -> Lexeme:
    ctx = Context.top(context)
    if isinstance(name, str) and name[0] == 'L':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'L{name}']))
    return ctx.entities.register(
        Lexeme(iri), lemma=lemma, category=category, language=language)


# Aliases for pseudo-properties.
label = LabelProperty()
alias = AliasProperty()
description = DescriptionProperty()
lemma = LemmaProperty()
lexical_category = LexicalCategoryProperty()
language = LanguageProperty()


@deprecated('get_label() is deprecated; use ENTITY.label instead')
def get_label(
        entity: Item | Property,
        default: str | None = None
) -> str | None:
    label = entity.context.entities.get_label(entity)
    if label is not None:
        return label.content
    else:
        return default


def reload() -> None:
    """Reloads the whole wd module."""
    import importlib

    from . import item, property
    _reload_property_cache()
    importlib.reload(item)
    importlib.reload(property)


_reload_property_cache()
