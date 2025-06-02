# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib

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
    TTextSet,
)
from ...typing import cast

__all__ = (
    'alias',
    'description',
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


def _load_property_cache(
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


def _install_resolver(context: Context | None = None) -> None:
    ctx = Context.top(context)
    resolver_iri = ctx.options.vocabulary.wd.resolver
    if resolver_iri is not None:
        from ...store import Store
        ctx.iris.register(IRI(NS.WD), resolver=Store('wdqs', resolver_iri))


def _install_schema(context: Context | None = None) -> None:
    ctx = Context.top(context)
    ctx.iris.register(IRI(NS.WD), schema=cast(Property.Schema, {
        k: IRI(str(v)) for k, v in NS.Wikidata.prefixes.items()}))


def P(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        range: TDatatype | None = None,
        inverse: TProperty | None = None,
        context: Context | None = None
) -> Property:
    """Creates a Wikidata property with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       range: Datatype.
       inverse: Inverse property.
       context: KIF context.

    Returns:
       Property.
    """
    if isinstance(name, str) and name[0] == 'P':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'P{name}']))
    return Context.top(context).entities.register(
        Property(iri),
        label=label, aliases=aliases, description=description,
        range=range, inverse=inverse)


def Q(
        name: int | str,
        label: TText | None = None,
        aliases: TTextSet | None = None,
        description: TText | None = None,
        context: Context | None = None
) -> Item:
    """Creates a Wikidata item with the given descriptors.

    Parameters:
       name: Name.
       label: Label.
       aliases: Aliases.
       description: Description.
       context: KIF context.

    Returns:
       Item.
    """
    if isinstance(name, str) and name[0] == 'Q':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'Q{name}']))
    return Context.top(context).entities.register(
        Item(iri), label=label, aliases=aliases, description=description)


def L(
        name: int | str,
        lemma: TText | None = None,
        category: TItem | None = None,
        language: TItem | None = None,
        context: Context | None = None
) -> Lexeme:
    """Creates a Wikidata lexeme with the given descriptors.

    Parameters:
       lemma: Lemma.
       category: Lexical category.
       language: Language.
       context: KIF context.

    Returns:
       Lexeme.
    """
    if isinstance(name, str) and name[0] == 'L':
        iri = IRI(str(NS.WD[name]))
    else:
        iri = IRI(str(NS.WD[f'L{name}']))
    return Context.top(context).entities.register(
        Lexeme(iri), lemma=lemma, category=category, language=language)


# Aliases for pseudo-properties.
label = LabelProperty()
alias = AliasProperty()
description = DescriptionProperty()
lemma = LemmaProperty()
lexical_category = LexicalCategoryProperty()
language = LanguageProperty()


def reload(
        load_property_cache: bool = True,
        install_resolver: bool = True,
        install_schema: bool = True,
        force: bool = True,
        context: Context | None = None
) -> None:
    """Reloads the `wd` module.

    Parameters:
       force: Force reload.
       context: KIF context.
    """
    if load_property_cache:
        _load_property_cache(context=context)
    if install_resolver:
        _install_resolver(context=context)
    if install_schema:
        _install_schema(context=context)
    if force:
        import importlib

        from . import item, property
        importlib.reload(item)
        importlib.reload(property)


reload(force=False)
