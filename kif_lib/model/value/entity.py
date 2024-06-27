# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import (
    Any,
    Callable,
    ClassVar,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..template import Template
from ..variable import Variable
from .iri import IRI, IRI_Template, IRI_Variable, T_IRI, V_IRI
from .value import Value, ValueTemplate, ValueVariable

EntityClass: TypeAlias = type['Entity']
EntityTemplateClass: TypeAlias = type['EntityTemplate']
EntityVariableClass: TypeAlias = type['EntityVariable']

TEntity: TypeAlias = Union['Entity', T_IRI]
VEntity: TypeAlias = Union['EntityTemplate', 'EntityVariable', 'Entity']
VTEntity: TypeAlias = Union[Variable, VEntity, TEntity]


class EntityTemplate(ValueTemplate):
    """Abstract base class for entity templates."""

    object_class: ClassVar[EntityClass]  # pyright: ignore

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            if Template.test(arg):
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

    object_class: ClassVar[EntityClass]  # pyright: ignore


class Entity(
        Value,
        template_class=EntityTemplate,
        variable_class=EntityVariable
):
    """Abstract base class for entities."""

    template_class: ClassVar[EntityTemplateClass]  # pyright: ignore
    variable_class: ClassVar[EntityVariableClass]  # pyright: ignore

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        if cls is not Entity:   # concrete subclass?
            return cls(IRI.check(arg, function or cls.check, name, position))
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

    def get_value(self) -> str:
        return self.args[0].value

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
