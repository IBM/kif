# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, override, TypeAlias, Union
from .kif_object import KIF_Object
from .snak import Snak, VSnak, VVSnak
from .template import Template
from .value import Entity, VEntity, VVEntity
from .variable import Variable

VStatement: TypeAlias =\
    Union['StatementTemplate', 'StatementVariable', 'Statement']


class StatementTemplate(Template):
    """Statement template.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    def __init__(self, subject: VVEntity, snak: VVSnak):
        super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # entity
            if Template.test(arg):
                return self._preprocess_arg_entity_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_entity_variable(
                    arg, i, self.__class__)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        elif i == 2:            # snak
            if Template.test(arg):
                return self._preprocess_arg_snak_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_snak_variable(
                    arg, i, self.__class__)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def subject(self) -> VEntity:
        """The subject of statement template."""
        return self.get_subject()

    def get_subject(self) -> VEntity:
        """Gets the subject of statement template.

        Returns:
           Subject, entity template or entity variable.
        """
        return self.args[0]

    @property
    def snak(self) -> VSnak:
        """The snak of statement template."""
        return self.get_snak()

    def get_snak(self) -> VSnak:
        """Gets the snak of statement template.

        Returns:
           Snak, snak template, or snak variable.
        """
        return self.args[1]


class StatementVariable(Variable):
    """Statement variable.

    Parameters:
       name: Name.
    """


class Statement(
        KIF_Object,
        template_class=StatementTemplate,
        variable_class=StatementVariable
):
    """Statement.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    def __init__(self, subject: VVEntity, snak: VVSnak):
        super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return self_._preprocess_arg_entity(arg, i)
        elif i == 2:
            return self_._preprocess_arg_snak(arg, i)
        else:
            raise self_._should_not_get_here()

    @property
    def subject(self) -> Entity:
        """The subject of statement."""
        return self.get_subject()

    def get_subject(self) -> Entity:
        """Gets the subject of statement.

        Returns:
           Subject.
        """
        return self.args[0]

    @property
    def snak(self) -> Snak:
        """The snak of statement."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets the snak of statement.

        Returns:
           Snak.
        """
        return self.args[1]
