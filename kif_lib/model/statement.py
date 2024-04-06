# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import override, TypeAlias, Union
from .kif_object import KIF_Object
from .pattern import Template, Variable
from .snak import Snak, VSnak
from .value import Entity, VEntity

VStatement: TypeAlias =\
    Union['StatementTemplate', 'StatementVariable', 'Statement']


class StatementTemplate(Template):
    """Statement template.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    def __init__(self, subject: VEntity, snak: VSnak):
        return super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # entity
            if Template.test(arg):
                return self._preprocess_arg_entity_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_entity_variable(arg, i)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        elif i == 2:            # snak
            if Template.test(arg):
                return self._preprocess_arg_snak_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_snak_variable(arg, i)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class StatementVariable(Variable):
    """Statement variable.

    Parameters:
       name: String.
    """


class Statement(KIF_Object):
    """Statement.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    template_class: type[Template] = StatementTemplate

    variable_class: type[Variable] = StatementVariable

    def __init__(self, subject: VEntity, snak: VSnak):
        return super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_entity(arg, i)
        elif i == 2:
            return self._preprocess_arg_snak(arg, i)
        else:
            raise self._should_not_get_here()

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
