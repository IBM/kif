# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing_extensions import overload, TYPE_CHECKING

from ..itertools import chain
from ..typing import (
    Any,
    cast,
    ClassVar,
    Iterator,
    Mapping,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object, KIF_ObjectClass, TLocation

if TYPE_CHECKING:
    from .snak import ValueSnakTemplate
    from .statement import StatementTemplate
    from .value import VVEntity, VVTValue

Theta: TypeAlias = Mapping['Variable', Optional[KIF_Object]]
VariableClass: TypeAlias = type['Variable']
TVariableClass: TypeAlias = Union[VariableClass, KIF_ObjectClass]


class Variable(KIF_Object):
    """Base class for variables.

    Parameters:
       name: Name.
       variable_class: Variable class.
    """

    #: Object class associated with this variable class.
    object_class: ClassVar[KIF_ObjectClass]

    class InstantiationError(ValueError):
        """Bad instantiation attempt."""

    def __new__(
            cls,
            name: str,
            variable_class: Optional[TVariableClass] = None
    ):
        var_cls = cls._check_optional_arg_variable_class(
            variable_class, cls, cls, 'variable_class', 2)
        assert var_cls is not None
        return super().__new__(var_cls)  # pyright: ignore

    @classmethod
    @override
    def check(
            cls,
            arg: 'Variable',
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, Variable):
            if issubclass(arg.__class__, cls):
                return cast(Self, arg)
            if issubclass(cls, arg.__class__):
                return cast(Self, cls(arg.name))
        raise cls._check_error(arg, function, name, position)

    @classmethod
    def _check_arg_variable_class(
            cls,
            arg: TVariableClass,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> VariableClass:
        if isinstance(arg, type) and issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'variable_class'),
                f'no variable class for {arg.__qualname__}',
                function, name, position), 'variable_class')

    def __init__(
            self,
            name: str,
            object_class: Optional[KIF_ObjectClass] = None
    ):
        super().__init__(name)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()

    @overload
    def __call__(self, v1: 'VVEntity', v2: 'VVTValue') -> 'StatementTemplate':
        ...

    @overload
    def __call__(self, v1: 'VVTValue') -> 'ValueSnakTemplate':
        ...

    def __call__(self, v1, v2=None):
        from .value import PropertyVariable
        prop = PropertyVariable.check(self)
        if v2 is not None:
            return prop(v1, v2)
        else:
            return prop(v1)

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
        return self._instantiate(
            theta, coerce, self.instantiate) if theta else self

    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[KIF_Object]:
        if self in theta:
            return self._instantiate_tail(theta, function, name, position)
        elif coerce:
            for other in filter(Variable.test, theta):
                assert isinstance(other, Variable)
                if other.name == self.name:
                    try:
                        var = other.check(self)
                    except TypeError:
                        continue  # not coercible, skip
                    if var in theta:
                        return var._instantiate_tail(
                            theta, function, name, position)
            return self
        else:
            return self

    def _instantiate_tail(
            self,
            theta: Theta,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[KIF_Object]:
        obj = theta[self]
        if obj is None:
            return obj
        else:
            from .template import Template
            if self.__class__ is Variable:
                obj_cls = KIF_Object
            elif isinstance(obj, Template):
                assert hasattr(self.object_class, 'template_class')
                obj_cls = self.object_class.template_class
            elif isinstance(obj, Variable):
                obj_cls = self.__class__
            else:
                obj_cls = self.object_class
            if isinstance(obj, obj_cls):
                return obj
            else:
                src = self.__class__.__qualname__
                dest = obj.__class__.__qualname__
                raise self._arg_error(
                    f"cannot instantiate {src} '{self.name}' with {dest}",
                    function, name, position, self.InstantiationError)


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
