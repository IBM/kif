# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import Any, ClassVar, override, TypeAlias, Union
from ..template import Template
from ..variable import Variable
from .iri import IRI, IRI_Template, IRI_Variable, V_IRI
from .value import Value, ValueTemplate, ValueVariable

EntityClass: TypeAlias = type['Entity']
EntityTemplateClass: TypeAlias = type['EntityTemplate']
EntityVariableClass: TypeAlias = type['EntityVariable']

VEntity: TypeAlias = Union['EntityTemplate', 'EntityVariable', 'Entity']
VVEntity: TypeAlias = Union[Variable, VEntity]


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

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # iri
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
