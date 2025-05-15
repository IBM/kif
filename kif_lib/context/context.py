# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import collections
import functools
from typing import TYPE_CHECKING

from typing_extensions import overload

from .. import itertools
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Iterable,
    Location,
    Optional,
    Sequence,
    Set,
    TracebackType,
    TypeVar,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..model import (
        Datatype,
        Entity,
        IRI,
        Item,
        Lexeme,
        Property,
        T_IRI,
        Text,
        TTextLanguage,
    )
    from ..store import Store
    from .options import Options
    from .registry import EntityRegistry, IRI_Registry

E = TypeVar('E')
T = TypeVar('T')
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

    def get_option_by_name(self, name: str | Sequence[str]) -> Any:
        """Gets option by name.

        Parameters:
           name: Option name.

        Returns:
           The option value.

        Raises:
           `KeyError`: No such option.
        """
        if isinstance(name, str):
            path = collections.deque(name.split('.'))
        else:
            path = collections.deque(name)
        if not path:
            path = collections.deque((self.options.name,))
        cur = path.popleft()
        if cur != self.options.name:
            raise KeyError(cur)
        res = self.options
        while path:
            cur = path.popleft()
            if not hasattr(res, cur):
                raise KeyError(cur)
            res = getattr(res, cur)
        return res

    def get_option_description_by_name(self, name: str | Sequence[str]) -> Any:
        """Gets option description by name.

        Parameters:
           name: Option name.

        Returns:
           The option description.

        Raises:
           `KeyError`: No such option.
        """
        if isinstance(name, str):
            path: tuple[str, ...] = tuple(name.split('.'))
        else:
            path = tuple(name)
        if not path or path == (self.options.name,):
            return self.options.describe()
        else:
            from .options import Section
            section = self.get_option_by_name(path[:-1])
            if isinstance(section, Section):
                try:
                    return section.describe(path[-1])
                except AttributeError as err:
                    raise KeyError('.'.join(path)) from err
            else:
                raise KeyError('.'.join(path))

    @overload
    def describe(
            self,
            value: Item,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Item.Descriptor | None:
        """Gets the descriptor of item in registry.

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in all languages.

        If `resolve` is ``True``, resolves item data.

        If `resolver` is given, uses it to resolve item data.
        Otherwise, uses the resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           value: Item.
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Item descriptor or ``None``.
        """
        ...                     # pragma: no cover

    @overload
    def describe(
            self,
            value: Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Property.Descriptor | None:
        """Gets the descriptor of property in registry.

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in all languages.

        If `resolve` is ``True``, resolves property data.

        If `resolver` is given, uses it to resolve property data.
        Otherwise, uses the resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           value: Property.
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Property descriptor or ``None``.
        """
        ...                     # pragma: no cover

    @overload
    def describe(
            self,
            value: Lexeme,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Lexeme.Descriptor | None:
        """Gets the descriptor of lexeme in registry.

        If `resolve` is ``True``, resolves lexeme data.

        If `resolver` is given, uses it to resolve lexeme data.
        Otherwise, uses resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           value: Lexeme.
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Lexeme descriptor or ``None``.
        """
        ...                     # pragma: no cover

    @overload
    def describe(
            self,
            value: T_IRI,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> IRI.Descriptor | None:
        """Gets the descriptor of IRI in registry.

        Parameters:
           value: IRI.
           function: Function or function name.

        Returns:
           IRI descriptor or ``None``.
        """
        ...                     # pragma: no cover

    def describe(
            self,
            value: Item | Property | Lexeme | T_IRI,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Optional[Union[
        Item.Descriptor, Property.Descriptor,
            Lexeme.Descriptor, IRI.Descriptor]]:
        from ..model import Entity, IRI
        function = function or self.describe
        if isinstance(value, Entity):
            return self._get_entity_x_helper(
                value, resolve, resolver, force,
                functools.partial(
                    self.entities.describe, function=function),  # type: ignore
                functools.partial(
                    self.resolve, all=True,
                    language=language, resolver=resolver, force=force))
        else:
            return self.iris.describe(
                IRI.check(value, function, 'value'),
                function=function)

    def get_label(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
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
        function = function or self.get_label
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_label,
                language=language, function=function),
            functools.partial(
                self.resolve, label=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def get_aliases(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
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
        function = function or self.get_aliases
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_aliases,
                language=language, function=function),
            functools.partial(
                self.resolve, aliases=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def get_description(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
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
        function = function or self.get_description
        return self._get_entity_x_helper(
            entity, resolve, resolver, force,
            functools.partial(
                self.entities.get_description,
                language=language, function=function),
            functools.partial(
                self.resolve, description=True,
                language=self._check_optional_language(language, function),
                resolver=resolver, force=force))

    def get_range(
            self,
            property: Property,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Datatype | None:
        """Gets the range of property in registry.

        Parameters:
           property: Property.
           resolve: Whether to resolve range.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Range or ``None``.
        """
        function = function or self.get_range
        return self._get_entity_x_helper(
            property, resolve, resolver, force,
            functools.partial(self.entities.get_range, function=function),
            functools.partial(
                self.resolve, range=True, resolver=resolver, force=force))

    def get_inverse(
            self,
            property: Property,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Property | None:
        """Gets the inverse of property in registry.

        Parameters:
           property: Property.
           resolve: Whether to resolve inverse.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Property or ``None``.
        """
        function = function or self.get_inverse
        return self._get_entity_x_helper(
            property, resolve, resolver, force,
            functools.partial(self.entities.get_inverse, function=function),
            functools.partial(
                self.resolve, inverse=True, resolver=resolver, force=force))

    def get_lemma(
            self,
            lexeme: Lexeme,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Text | None:
        """Gets the lemma of lexeme in registry.

        Parameters:
           lexeme: Lexeme.
           resolve: Whether to resolve lemma.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Text or ``None``.
        """
        function = function or self.get_lemma
        return self._get_entity_x_helper(
            lexeme, resolve, resolver, force,
            functools.partial(self.entities.get_lemma, function=function),
            functools.partial(
                self.resolve, lemma=True, resolver=resolver, force=force))

    def get_category(
            self,
            lexeme: Lexeme,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Item | None:
        """Gets the lexical category of lexeme in registry.

        Parameters:
           lexeme: Lexeme.
           resolve: Whether to resolve lexical category.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Item or ``None``.
        """
        function = function or self.get_category
        return self._get_entity_x_helper(
            lexeme, resolve, resolver, force,
            functools.partial(self.entities.get_category, function=function),
            functools.partial(
                self.resolve, category=True, resolver=resolver, force=force))

    def get_language(
            self,
            lexeme: Lexeme,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None,
            function: Location | None = None
    ) -> Item | None:
        """Gets the language of lexeme in registry.

        Parameters:
           lexeme: Lexeme.
           resolve: Whether to resolve language.
           resolver: Resolver store.
           force: Whether to force resolution.
           function: Function or function name.

        Returns:
           Item or ``None``.
        """
        function = function or self.get_category
        return self._get_entity_x_helper(
            lexeme, resolve, resolver, force,
            functools.partial(self.entities.get_language, function=function),
            functools.partial(
                self.resolve, lexeme_language=True,
                resolver=resolver, force=force))

    def _get_entity_x_helper(
            self,
            entity: E,
            resolve: bool | None,
            resolver: Store | None,
            force: bool | None,
            get_value: Callable[[E], V | None],
            resolve_entity: Callable[[tuple[E]], Any]
    ) -> V | None:
        value = get_value(entity)
        if force:
            value = None        # force
        if value is None:
            if resolve is None:
                resolve = self.options.entities.resolve
            if resolve and resolve_entity((entity,)):
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

    def get_prefix(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> str | None:
        """Gets the prefix of IRI in registry.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Prefix or ``None``.
        """
        return self.iris.get_prefix(iri, function)

    def get_resolver(
            self,
            iri: T_IRI | Entity,
            function: Location | None = None
    ) -> Store | None:
        """Gets the entity resolver of IRI or entity in registry.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Store or ``None``.
        """
        return self.iris.lookup_resolver(iri, function)

    def get_schema(
            self,
            iri: T_IRI | Property,
            function: Location | None = None
    ) -> Property.Schema | None:
        """Gets the property schema of IRI or property in registry.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Property schema or ``None``.
        """
        return self.iris.lookup_schema(iri, function)

    def resolve(
            self,
            objects: Iterable[T],
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
            force: bool | None = None,
            function: Location | None = None
    ) -> Iterable[T]:
        """Resolves entity data.

        Traverses `objects` recursively and resolves the data of every
        entity found into context's entity registry.

        If `resolver` is given, uses it to resolve entity data.
        Otherwise, uses the resolver registered in context (if any).

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in all languages.

        If `force` is given, forces resolution.

        Parameters:
           objects: Objects.
           resolver: Resolver store.
           label: Whether to resolve labels.
           aliases: Whether to resolve aliases.
           description: Whether to resolve descriptions.
           language: Language.
           range: Whether to resolve ranges.
           inverse: Whether to resolve inverses.
           lemma: Whether to resolve lemmas.
           category: Whether to resolve lexical categories.
           lexeme_language: Whether to resolve lexeme languages.
           all: Whether to resolve all data.
           force: Whether to force resolve.
           function: Function or function name.

        Returns:
           `objects`.
        """
        from ..model import Entity, KIF_Object
        from ..store import Store
        function = function or self.resolve
        resolver = KIF_Object._check_optional_arg_isinstance(
            resolver, Store, None, function, 'resolver')
        it1, it2 = itertools.tee(objects, 2)
        is_entity = (lambda o: isinstance(o, Entity))
        entities: Iterable[Entity] = itertools.chain(*map(
            lambda o: cast(KIF_Object, o).traverse(is_entity), filter(
                lambda o: isinstance(o, KIF_Object), it1)))
        pairs = cast(Iterable[tuple[Entity, Store]], filter(
            lambda t: t[1] is not None, map(
                lambda e: (
                    e, resolver
                    if resolver is not None else self.iris.lookup_resolver(e)),
                entities)))
        self.entities.resolve(
            pairs, label=label, aliases=aliases, description=description,
            language=language, range=range, inverse=inverse,
            lemma=lemma, category=category, lexeme_language=lexeme_language,
            all=all, force=bool(force))
        return it2
