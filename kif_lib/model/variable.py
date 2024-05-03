# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..itertools import chain
from ..typing import (
    cast,
    Iterator,
    Mapping,
    NoReturn,
    Optional,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object, TCallable

Theta: TypeAlias = Mapping['Variable', Optional[KIF_Object]]
VariableClass: TypeAlias = type['Variable']
TVariableClass: TypeAlias = Union[VariableClass, type[KIF_Object]]


class Variable(KIF_Object):
    """Base class for variables.

    Parameters:
       name: Name.
       variable_class: Variable class.
    """

    #: Object class associated with this variable class.
    object_class: type[KIF_Object]

    def __new__(
            cls,
            name: str,
            variable_class: Optional[TVariableClass] = None
    ):
        var_cls = cls._check_optional_arg_variable_class(
            variable_class, cls, cls, 'variable_class', 2)
        assert var_cls is not None
        return super().__new__(var_cls)

    @classmethod
    def _check_arg_variable_class(
            cls,
            arg: TVariableClass,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[VariableClass, NoReturn]:
        if isinstance(arg, type) and issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'variable_class'),
                f'no variable class for {arg.__qualname__}',
                function, name, position), 'variable_class')

    @classmethod
    def _check_optional_arg_variable_class(
            cls,
            arg: Optional[TVariableClass],
            default: Optional[VariableClass] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[VariableClass], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_variable_class(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_variable_class(
            cls,
            arg: TVariableClass,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[VariableClass, NoReturn]:
        return cls._check_arg_variable_class(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_variable_class(
            cls,
            arg: Optional[TVariableClass],
            i: int,
            default: Optional[VariableClass] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[VariableClass], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_variable_class(arg, i, function)

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
        from .value import PropertyVariable
        return self.coerce(PropertyVariable)(value1, value2)

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
           Name.
        """
        return self.args[0]

    def coerce(self, variable_class: TVariableClass) -> 'Variable':
        """Coerces variable to `variable_class`.

        Parameters:
           variable_class: Variable class.

        Returns:
           The resulting variable.
        """
        var_cls = Variable._check_arg_variable_class(
            variable_class, self.coerce, 'variable_class', 1)
        return self._coerce(var_cls, self.coerce, 'variable_class', 1)

    def _coerce(
            self,
            variable_class: VariableClass,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Variable':
        if issubclass(self.__class__, variable_class):
            return self         # nothing to do
        elif issubclass(variable_class, self.__class__):
            return variable_class(self.name)
        else:
            src = self.__class__.__qualname__
            dest = variable_class.__qualname__
            raise self._arg_error(
                f'cannot coerce {src} into {dest}',
                function, name, position, TypeError)

    def instantiate(
            self,
            theta: Theta,
            coerce: bool = True
    ) -> Optional[KIF_Object]:
        """Applies variable instantiation `theta` to variable.

        Parameters:
           theta: Variable instantiation.
           coerce: Whether to consider coercible variables equal.

        Returns:
           The resulting object.
        """
        self._check_arg_isinstance(
            theta, Mapping, self.instantiate, 'theta', 1)
        return self._instantiate(theta, coerce) if theta else self

    def _instantiate(
            self,
            theta: Theta,
            coerce: bool = True
    ) -> Optional[KIF_Object]:
        if self in theta:
            return self._instantiate_check_inst(theta[self])
        elif coerce:
            for other in filter(Variable.test, theta):
                if other.name == self.name:
                    try:
                        var = self.coerce(other.__class__)
                    except TypeError:
                        continue  # not coercible, skip
                    if var in theta:
                        return var._instantiate_check_inst(theta[var])
            return self
        else:
            return self

    def _instantiate_check_inst(
            self,
            inst: Optional[KIF_Object]
    ) -> Optional[KIF_Object]:
        if self.__class__ is Variable:
            obj_cls = KIF_Object
        else:
            obj_cls = self.object_class
        return cast(
            Optional[KIF_Object], obj_cls.check_optional(inst, None))


def Variables(
        name: str,
        *names: Union[str, TVariableClass],
) -> Iterator[Variable]:
    """Constructs one or more variables.

    Parameters:
       name: Name.
       names: Names or variable classes.

    Returns:
       The resulting variables.
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
    for xs, variable_class in it(chain((name,), names)):
        for x in xs:
            yield Variable(x, variable_class)
