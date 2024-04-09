# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable


class Template(KIF_Object):
    """Abstract base class for templates."""


class Variable(KIF_Object):
    """Base class for variables.

    Parameters:
        name: String.
    """

    @classmethod
    def _preprocess_arg_variable(
            cls,
            arg: 'Variable',
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Variable', NoReturn]:
        arg = cast(Variable, Variable.check(
            arg, function or cls, None, i))
        return arg._coerce(cls, function or cls, None, i)

    def __init__(self, name: str):
        super().__init__(name)

    def __call__(self, value1, value2=None):
        return self.coerce(self._PropertyVariable)(value1, value2)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def name(self) -> str:
        """The name of variable."""
        return self.get_name()

    def get_name(self) -> str:
        """Gets the name of variable.

        Returns:
           String.
        """
        return self.args[0]

    def coerce(self, variable_class: type['Variable']) -> 'Variable':
        """Coerces variable to `variable_class`.

        Parameters:
           variable_class: Subclass of :class:`Variable`.

        Returns:
           The resulting variable.
        """
        return self._coerce(variable_class, self.coerce, 'variable_class', 1)

    def _coerce(
            self,
            variable_class: type['Variable'],
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Variable':
        self._check_arg_isinstance(
            variable_class, type, function, name, position)
        if issubclass(self.__class__, variable_class):
            return self         # nothing to do
        if issubclass(variable_class, self.__class__):
            return variable_class(self.name)
        else:
            src = self.__class__.__qualname__
            dest = variable_class.__qualname__
            raise self._arg_error(
                f'cannot coerce {src} into {dest}',
                function, name, position, TypeError)


class Pattern(KIF_Object):
    """Abstract base class for patterns."""
