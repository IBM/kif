# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from functools import cache

from ..typing import Mapping, NoReturn, Optional, Set, TypeAlias, Union
from .kif_object import KIF_Object, TCallable
from .variable import Variable

TemplateClass: TypeAlias = type['Template']
TTemplateClass: TypeAlias = Union[TemplateClass, type[KIF_Object]]


class Template(KIF_Object):
    """Abstract base class for templates."""

    #: Object class associated with this template class.
    object_class: type[KIF_Object]

    @classmethod
    def _check_arg_template_class(
            cls,
            arg: TTemplateClass,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TemplateClass, NoReturn]:
        if issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'template_class'),
                f'no template class for {arg.__qualname__}',
                function, name, position), 'template_class')

    @classmethod
    def _check_optional_arg_template_class(
            cls,
            arg: Optional[TTemplateClass],
            default: Optional[TemplateClass] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[TemplateClass], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_template_class(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_template_class(
            cls,
            arg: TTemplateClass,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[TemplateClass, NoReturn]:
        return cls._check_arg_template_class(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_template_class(
            cls,
            arg: Optional[TTemplateClass],
            i: int,
            default: Optional[TemplateClass] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[TemplateClass], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_template_class(arg, i, function)

    @property
    def variables(self) -> Set[Variable]:
        """The set of variables occurring in template."""
        return self.get_variables()

    @cache
    def get_variables(self) -> Set[Variable]:
        """Gets the set of variables occurring in template.

        Returns:
           Set of variables.
        """
        return frozenset(self._traverse(
            Variable.test,
            KIF_Object._isinstance_template_or_variable))

    def instantiate(
            self,
            theta: Mapping[Variable, Optional[KIF_Object]]
    ) -> KIF_Object:
        """Applies variable instantiation `theta` to template.

        Parameters:
           theta: A mapping of variables to objects or ``None``.

        Returns:
           The resulting object.
        """
        self._check_arg_isinstance(
            theta, Mapping, self.instantiate, 'theta', 1)
        return self._instantiate(theta) if theta else self

    def _instantiate(
            self,
            theta: Mapping[Variable, Optional[KIF_Object]]
    ) -> KIF_Object:
        return self.__class__(*map(
            lambda arg: arg._instantiate(theta)
            if isinstance(arg, (Template, Variable)) else arg, self.args))
