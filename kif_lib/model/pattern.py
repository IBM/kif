# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import (
    Any,
    Callable,
    cast,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from .constraint import Constraint, TConstraint
from .kif_object import KIF_Object
from .term import Template, Variable

TPattern: TypeAlias = Union['Pattern', 'TTemplatePattern', 'TVariablePattern']
TTemplatePattern: TypeAlias = Union['TemplatePattern', 'Template']
TVariablePattern: TypeAlias = Union['VariablePattern', 'Variable']


class Pattern(KIF_Object):
    """Abstract base class for patterns."""

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
        elif isinstance(arg, Template):
            return cast(Self, TemplatePattern.check(
                arg, function or cls.check, name, position))
        elif isinstance(arg, Variable):
            return cast(Self, VariablePattern.check(
                arg, function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

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


class TemplatePattern(Pattern):
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
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
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
            constraint: Optional[TConstraint] = None
    ):
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


class VariablePattern(Pattern):
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
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
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
            constraint: Optional[TConstraint] = None
    ):
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
