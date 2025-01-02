# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import Any, cast, Location, override, Self, TypeAlias, Union
from .constraint import Constraint, TConstraint
from .kif_object import KIF_Object
from .term import ClosedTerm, Template, Variable

TPattern: TypeAlias = Union['Pattern', 'TClosedPattern', 'TOpenPattern']
TClosedPattern: TypeAlias = Union['ClosedPattern', 'ClosedTerm']
TOpenPattern: TypeAlias =\
    Union['OpenPattern', 'TTemplatePattern', 'TVariablePattern']
TTemplatePattern: TypeAlias = Union['TemplatePattern', 'Template']
TVariablePattern: TypeAlias = Union['VariablePattern', 'Variable']


class Pattern(KIF_Object):
    """Abstract base class for patterns."""

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
        elif isinstance(arg, ClosedTerm):
            return cast(Self, ClosedPattern.check(
                arg, function or cls.check, name, position))
        else:
            return cast(Self, OpenPattern.check(
                arg, function or cls.check, name, position))

    @property
    def constraint(self) -> Constraint:
        """The constraint of pattern."""
        return self.get_constraint()

    def get_constraint(self) -> Constraint:
        """Gets the constraint of pattern.

        Returns:
           Constraint.
        """
        return self.args[1]


class ClosedPattern(Pattern):
    """Closed (ground) pattern.

    Parameters:
       object: Closed term.
       constraint: Constraint.
    """

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
        elif isinstance(arg, ClosedTerm):
            return cls(arg)
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            object: ClosedTerm,
            constraint: TConstraint | None = None
    ) -> None:
        super().__init__(object, constraint)

    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # object
            return ClosedTerm.check(arg, type(self), None, i)
        elif i == 2:            # constraint
            return Constraint.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def object(self) -> ClosedTerm:
        """The object of closed pattern."""
        return self.get_object()

    def get_object(self) -> ClosedTerm:
        """Gets the object of closed pattern.

        Returns:
           Object (closed term).
        """
        return self.args[0]


class OpenPattern(Pattern):
    """Abstract base class for open patterns."""

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
        elif isinstance(arg, Template):
            return cast(Self, TemplatePattern.check(
                arg, function or cls.check, name, position))
        else:
            return cast(Self, VariablePattern.check(
                arg, function or cls.check, name, position))


class TemplatePattern(OpenPattern):
    """Template pattern.

    Parameters:
       template: Template.
       constraint: Constraint.
    """

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
        elif isinstance(arg, Template):
            return cls(arg)
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            template: Template,
            constraint: TConstraint | None = None
    ) -> None:
        super().__init__(template, constraint)

    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # template
            return Template.check(arg, type(self), None, i)
        elif i == 2:            # constraint
            return Constraint.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def template(self) -> Template:
        """The template of template pattern."""
        return self.get_template()

    def get_template(self) -> Template:
        """Gets the template of template pattern.

        Returns:
           Template.
        """
        return self.args[0]


class VariablePattern(OpenPattern):
    """Variable pattern.

    Parameters:
       variable: Variable.
       constraint: Constraint.
    """

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
        elif isinstance(arg, Variable):
            return cls(arg)
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            variable: Variable,
            constraint: TConstraint | None = None
    ) -> None:
        super().__init__(variable, constraint)

    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # variable
            return Variable.check(arg, type(self), None, i)
        elif i == 2:            # constraint
            return Constraint.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def variable(self) -> Variable:
        """The variable pattern."""
        return self.get_variable()

    def get_variable(self) -> Variable:
        """Gets variable of pattern.

        Returns:
           Variable.
        """
        return self.args[0]
