# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import TYPE_CHECKING

from ... import itertools
from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Iterator,
    Mapping,
    Optional,
    Self,
    Set,
    TypeAlias,
    Union,
)
from ..kif_object import KIF_Object

if TYPE_CHECKING:               # pragma: no cover
    from .template import Template
    from .variable import Variable


class Term(KIF_Object):
    """Abstract base class for terms."""

    def __new__(cls, *args, **kwargs) -> Self:
        has_tpl_or_var_arg = any(map(
            cls.is_open, itertools.chain(args, kwargs.values())))
        if cls._is_proper_subclass_of_closed_term(cls) and has_tpl_or_var_arg:
            return cast(
                Self, cls.template_class(*args, **kwargs))  # type:ignore
        elif (cls._is_proper_subclass_of_template(cls)
              and not has_tpl_or_var_arg):
            return cast(
                Self, cls.object_class(*args, **kwargs))  # type: ignore
        else:
            return super().__new__(cls)

    @classmethod
    def _is_proper_subclass_of_closed_term(cls, arg: Any) -> bool:
        return (isinstance(arg, type)
                and arg is not ClosedTerm
                and issubclass(arg, ClosedTerm))

    @classmethod
    def _is_proper_subclass_of_template(cls, arg: Any) -> bool:
        from .template import Template
        return (isinstance(arg, type)
                and arg is not Template
                and issubclass(arg, Template))

    @classmethod
    def is_closed(cls, arg: Any) -> bool:
        """Tests whether argument is a closed term.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return isinstance(arg, ClosedTerm)

    @classmethod
    def is_open(cls, arg: Any) -> bool:
        """Tests whether argument is an open term.

        Returns:
           ``True`` if successful; ``False`` otherwise."""
        return isinstance(arg, OpenTerm)


class ClosedTerm(Term):
    """Abstract base class for closed (ground) terms."""

    #: Template class associated with this closed-term class.
    template_class: ClassVar[type['Template']]

    #: Variable class associated with this closed-term class.
    variable_class: ClassVar[type['Variable']]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        from .template import Template
        from .variable import Variable
        assert not issubclass(cls, OpenTerm)
        if 'template_class' in kwargs:
            cls.template_class = kwargs['template_class']
            assert issubclass(cls.template_class, Template)
            cls.template_class.object_class = cls  # pyright: ignore
        if 'variable_class' in kwargs:
            cls.variable_class = kwargs['variable_class']
            assert issubclass(cls.variable_class, Variable)
            cls.variable_class.object_class = cls  # pyright: ignore


#: The type of variable instantiations.
Theta: TypeAlias = Mapping['Variable', Optional[Term]]


class OpenTerm(Term):
    """Abstract base class for open terms."""

    #: Closed-term class associated with this open-term class.
    object_class: ClassVar[type[ClosedTerm]]

    class InstantiationError(ValueError):
        """Bad instantiation attempt."""

    @property
    def variables(self) -> Set['Variable']:
        """The set of variables occurring in open term."""
        return self.get_variables()

    def get_variables(self) -> Set['Variable']:
        """Gets the set of variables occurring in open term.

        Returns:
           Set of variables.
        """
        return frozenset(self._iterate_variables())

    @abc.abstractmethod
    def _iterate_variables(self) -> Iterator['Variable']:
        raise NotImplementedError

    def instantiate(
            self,
            theta: Theta,
            coerce: bool = True
    ) -> Optional[Term]:
        """Applies variable instantiation `theta` to open term.

        Parameters:
           theta: Variable instantiation.
           coerce: Whether to consider coercible variables equal.

        Returns:
           Term or ``None``.
        """
        self._check_arg_isinstance(
            theta, Mapping, self.instantiate, 'theta', 1)
        return self._instantiate(
            theta, coerce, self.instantiate) if theta else self

    @abc.abstractmethod
    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Term]:
        raise NotImplementedError
