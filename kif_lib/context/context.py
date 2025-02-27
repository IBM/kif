# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
from typing import TYPE_CHECKING

from ..typing import (
    Callable,
    cast,
    ClassVar,
    Iterable,
    Location,
    Set,
    TracebackType,
    TypeVar,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..model import Item, KIF_Object, Property, Text, TTextLanguage
    from ..store import Store
    from .options import Options
    from .registry import EntityRegistry, IRI_Registry

E = TypeVar('E')
V = TypeVar('V')


class Context:
    """KIF context."""

    #: Context stack.
    _stack: ClassVar[list[Context]] = []

    @classmethod
    def top(cls, context: Context | None = None) -> Context:
        """Gets the current context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        if context is not None:
            return context
        if not cls._stack:
            cls._stack.append(cls())
        assert cls._stack
        return cls._stack[-1]

    __slots__ = (
        '_entities',
        '_iris',
        '_options',
    )

    #: Entity registry.
    _entities: EntityRegistry

    #: IRI registry.
    _iris: IRI_Registry

    #: Options.
    _options: Options

    def __init__(self) -> None:
        from ..namespace import PREFIXES
        from .options import Options
        from .registry import EntityRegistry, IRI_Registry
        self._entities = EntityRegistry()
        self._iris = IRI_Registry({k: str(v) for k, v in PREFIXES.items()})
        self._options = Options()

    def __enter__(self) -> Context:
        self._stack.append(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._stack.pop()

    @property
    def entities(self) -> EntityRegistry:
        """The entity registry."""
        return self.get_entities()

    def get_entities(self) -> EntityRegistry:
        """Gets the entity registry.

        Returns:
           Entity registry.
        """
        return self._entities

    @property
    def iris(self) -> IRI_Registry:
        """The IRI registry."""
        return self.get_iris()

    def get_iris(self) -> IRI_Registry:
        """Gets the IRI registry.

        Returns:
           IRI registry.
        """
        return self._iris

    @property
    def options(self) -> Options:
        """The options of context."""
        return self.get_options()

    def get_options(self) -> Options:
        """Gets the options of context.

        Returns:
           Options.
        """
        return self._options

    def get_entity_label(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool = False,
            function: Location | None = None
    ) -> Text | None:
        """Gets the label of item or property in registry.

        Parameters:
           entity: Item or property.
           language: Language.
           resolve: Whether to resolve label.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Label or ``None``.
        """
        function = function or self.get_entity_label
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_label,
                language=language, function=function),
            functools.partial(
                self.load_entities,
                label=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def get_entity_aliases(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool = False,
            function: Location | None = None
    ) -> Set[Text] | None:
        """Gets the aliases of item or property in registry.

        Parameters:
           entity: Item or property.
           language: Language.
           resolve: Whether to resolve aliases.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Aliases or ``None``.
        """
        function = function or self.get_entity_aliases
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_aliases,
                language=language, function=function),
            functools.partial(
                self.load_entities,
                aliases=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def get_entity_description(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool = False,
            function: Location | None = None
    ) -> Text | None:
        """Gets the description of item or property in registry.

        Parameters:
           entity: Item or property.
           language: Language.
           resolve: Whether to resolve description.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Description or ``None``.
        """
        function = function or self.get_entity_description
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_description,
                language=language, function=function),
            functools.partial(
                self.load_entities,
                description=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def _get_entity_x_helper(
            self,
            entity: E,
            resolve: bool | None,
            resolver: Store | None,
            force: bool,
            get_value: Callable[[E], V | None],
            load_entity: Callable[[tuple[E]], bool]
    ) -> V | None:
        value = get_value(entity)
        if force:
            value = None        # force
        if value is None:
            if resolve is None:
                resolve = self.options.entities.resolve
            if load_entity((entity,)):
                value = get_value(entity)  # update
        return value

    def _check_optional_language(
            self,
            language: TTextLanguage | None,
            function: Location | None
    ) -> str:
        from ..model import String
        language = String.check_optional(
            language, None, function, 'language')
        if language:
            return language.content
        else:
            return self.options.language

    def load_entities(
            self,
            objects: Iterable[KIF_Object],
            resolver: Store | None = None,
            label: bool = False,
            aliases: bool = False,
            description: bool = False,
            language: TTextLanguage | None = None,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            lexeme_language: bool = False,
            all: bool = False,
            force: bool = False,
            function: Location | None = None
    ) -> bool:
        """Loads entity data into context.

        Traverses `objects` recursively and loads the data of every entity
        found.

        If `resolver` is given, uses it to resolve entity data.  Otherwise,
        uses the registered resolver stores (if any).

        If `language` is given, loads only text in `language`.  Otherwise,
        loads text in `language`.

        If `force` is given, loads data even if it already exists in
        registry.

        Parameters:
           objects: KIF objects.
           resolver: Resolver store.
           label: Whether to load labels.
           aliases: Whether to load aliases.
           description: Whether to load descriptions.
           language: Language.
           range: Whether to load ranges.
           inverse: Whether to load inverses.
           lemma: Whether to load lemmas.
           category: Whether to load lexical categories.
           lexeme_language: Whether to load lexeme languages.
           all: Whether to load all data.
           force: Whether to force load.
           function: Function or function name.

        Returns:
           ``True`` if any data was loaded; ``False`` otherwise.
        """
        from .. import itertools
        from ..model import Entity, KIF_Object
        from ..store import Store
        function = function or self.load_entities
        resolver = KIF_Object._check_optional_arg_isinstance(
            resolver, Store, None, function, 'resolver')
        is_entity = (lambda o: isinstance(o, Entity))
        entities: Iterable[Entity] = itertools.chain(
            *map(lambda o: KIF_Object.check(o, function, 'objects').traverse(
                is_entity), objects))
        pairs = cast(Iterable[tuple[Entity, Store]], filter(
            lambda t: t[1] is not None, map(
                lambda e: (
                    e, resolver
                    if resolver is not None else self.iris.lookup_resolver(e)),
                entities)))
        return self.entities.load(
            pairs, label=label, aliases=aliases, description=description,
            language=language, range=range, inverse=inverse,
            lemma=lemma, category=category, lexeme_language=lexeme_language,
            all=all, force=force)
