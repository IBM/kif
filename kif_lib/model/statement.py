# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from .snak import (
    Snak,
    SnakTemplate,
    SnakVariable,
    TSnak,
    ValueSnak,
    VSnak,
    VTSnak,
)
from .term import ClosedTerm, Template, Variable
from .value import (
    Entity,
    EntityTemplate,
    EntityVariable,
    TEntity,
    TProperty,
    TValue,
    VEntity,
    VTEntity,
)

TStatement: TypeAlias =\
    Union['Statement',
          tuple[TEntity, TSnak],
          tuple[TEntity, TProperty, TValue]]
VStatement: TypeAlias =\
    Union['StatementTemplate', 'StatementVariable', 'Statement']
VTStatement: TypeAlias = Union[Variable, VStatement, TStatement]


class StatementTemplate(Template):
    """Statement template.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    object_class: ClassVar[type[Statement]]  # pyright: ignore

    def __init__(self, subject: VTEntity, snak: VTSnak) -> None:
        super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # entity
            if isinstance(arg, Template):
                return EntityTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return EntityVariable.check(arg, type(self), None, i)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        elif i == 2:            # snak
            if isinstance(arg, Template):
                return SnakTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return SnakVariable.check(arg, type(self), None, i)
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

    object_class: ClassVar[type[Statement]]  # pyright: ignore


class Statement(
        ClosedTerm,
        template_class=StatementTemplate,
        variable_class=StatementVariable
):
    """Statement.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    template_class: ClassVar[type[StatementTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[StatementVariable]]  # pyright: ignore

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
        elif isinstance(arg, tuple) and len(arg) >= 2:
            fn = function or cls.check
            if len(arg) == 2:
                return cls(
                    Entity.check(arg[0], fn, name, position),
                    Snak.check(arg[1], fn, name, position))
            else:
                return cls(
                    Entity.check(arg[0], fn, name, position),
                    ValueSnak.check((arg[1], arg[2]), fn, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self, subject: VTEntity, snak: VTSnak) -> None:
        super().__init__(subject, snak)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Entity.check(arg, type(self_), None, i)
        elif i == 2:
            return Snak.check(arg, type(self_), None, i)
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
