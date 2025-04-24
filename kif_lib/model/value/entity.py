# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ...typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from ..term import Template, Variable
from .iri import IRI, IRI_Template, IRI_Variable, T_IRI, V_IRI
from .string import TString
from .value import Value, ValueTemplate, ValueVariable

TEntity: TypeAlias = Union['Entity', T_IRI]
VEntity: TypeAlias = Union['EntityTemplate', 'EntityVariable', 'Entity']
VTEntity: TypeAlias = Union[Variable, VEntity, TEntity]

if TYPE_CHECKING:               # pragma: no cover
    from ...store import Store


class EntityTemplate(ValueTemplate):
    """Abstract base class for entity templates."""

    object_class: ClassVar[type[Entity]]  # pyright: ignore

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            if isinstance(arg, Template):
                return IRI_Template.check(arg, type(self), None, i)
            else:
                return IRI_Variable.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def iri(self) -> V_IRI:
        """The iri of entity template."""
        return self.get_iri()

    def get_iri(self) -> V_IRI:
        """Gets the iri of entity template.

        Returns:
           IRI, IRI template, or IRI variable.
        """
        return self.args[0]


class EntityVariable(ValueVariable):
    """Entity variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Entity]]  # pyright: ignore


class Entity(
        Value,
        template_class=EntityTemplate,
        variable_class=EntityVariable
):
    """Abstract base class for entities."""

    template_class: ClassVar[type[EntityTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[EntityVariable]]  # pyright: ignore

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif cls is not Entity:  # concrete subclass?
            return cls(IRI.check(arg, function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            if isinstance(arg, type(self_)):
                assert isinstance(arg, Entity)
                return arg.iri
            else:
                return IRI.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @property
    def iri(self) -> IRI:
        """The iri of entity."""
        return self.get_iri()

    def get_iri(self) -> IRI:
        """Gets the iri of entity.

        Returns:
           IRI.
        """
        return self.args[0]

    @property
    def resolver(self) -> Store | None:
        """The resolver of entity in KIF context."""
        return self.get_resolver()

    def get_resolver(self) -> Store | None:
        """Gets the resolver of entity in KIF context.

        Returns:
           Store or ``None``.
        """
        return self.context.get_resolver(self, function=self.get_resolver)

    @abc.abstractmethod
    def display(self, language: TString | None = None) -> str:
        """Gets the display-name of entity in KIF context.

        Parameters:
           language: Language.

        Returns:
           Display name.
        """
        return (
            self.context.iris.curie(self.iri, self.display)
            or self.iri.content)
