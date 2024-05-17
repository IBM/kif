# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import cast, NoReturn, Optional, override, TypeAlias, Union
from ..kif_object import TCallable
from ..template import Template
from ..variable import Variable
from .iri import IRI, V_IRI
from .value import Value, ValueTemplate, ValueVariable

EntityClass: TypeAlias = type['Entity']
EntityTemplateClass: TypeAlias = type['EntityTemplate']
EntityVariableClass: TypeAlias = type['EntityVariable']

VEntity: TypeAlias = Union['EntityTemplate', 'EntityVariable', 'Entity']
VVEntity: TypeAlias = Union[Variable, VEntity]


class EntityTemplate(ValueTemplate):
    """Abstract base class for entity templates."""

    object_class: EntityClass

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # iri
            if Template.test(arg):
                return self._preprocess_arg_iri_template(arg, i)
            else:
                return self._preprocess_arg_iri_variable(
                    arg, i, self.__class__)
        else:
            raise self._should_not_get_here()

    @property
    def iri(self) -> V_IRI:
        """The iri of entity template."""
        return self.get_iri()

    def get_iri(self) -> V_IRI:
        """Gets the iri of entity template.

        Returns:
           IRI template or IRI variable.
        """
        return self.args[0]


class EntityVariable(ValueVariable):
    """Entity variable.

    Parameters:
       name: Name.
    """

    object_class: EntityClass

    @classmethod
    def _preprocess_arg_entity_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['EntityVariable', NoReturn]:
        return cast(EntityVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class Entity(
        Value,
        template_class=EntityTemplate,
        variable_class=EntityVariable
):
    """Abstract base class for entities."""

    template_class: EntityTemplateClass
    variable_class: EntityVariableClass

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # iri
            return self._preprocess_arg_iri(
                arg.args[0] if isinstance(arg, Entity) else arg, i)
        else:
            raise self._should_not_get_here()

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
