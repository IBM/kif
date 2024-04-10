# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..itertools import chain
from ..typing import cast, Iterable, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable


class Template(KIF_Object):
    """Abstract base class for templates."""


class Variable(KIF_Object):
    """Base class for variables.

    Parameters:
       name: Name.
       object_class: Object class.
    """

    def __new__(
            cls,
            name: str,
            object_class: Optional[type[KIF_Object]] = None
    ):
        if (object_class is not None
                and hasattr(object_class, 'variable_class')):
            return object_class.variable_class(name)
        else:
            return super().__new__(cls)

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

    def __init__(
            self,
            name: str,
            object_class: Optional[type[KIF_Object]] = None
    ):
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


def Variables(
        name: str,
        *names: Union[str, type[KIF_Object]],
) -> Iterable[Variable]:
    """Constructs one or more variables.

    Parameters:
       name: Name.
       names: Remaining strings or object class.

    Returns:
       The resulting variables
    """
    def it(args):
        vars = []
        for x in args:
            if isinstance(x, str):
                vars.append(x)
            elif vars:
                yield (vars, x)
                vars = []
        if vars:
            yield (vars, None)
    for xs, object_class in it(chain((name,), names)):
        for x in xs:
            yield Variable(x, object_class)


class Pattern(KIF_Object):
    """Abstract base class for patterns."""
