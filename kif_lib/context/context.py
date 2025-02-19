# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ..typing import ClassVar, TracebackType

if TYPE_CHECKING:  # pragma: no cover
    from .options import Options
    from .registry2 import EntityRegistry, IRI_Registry


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
        from .registry2 import EntityRegistry, IRI_Registry
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
