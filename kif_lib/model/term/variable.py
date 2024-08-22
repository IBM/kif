# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from typing_extensions import overload

from ... import itertools
from ...typing import (
    Any,
    Callable,
    cast,
    Iterator,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from .term import ClosedTerm, OpenTerm, Term, Theta

if TYPE_CHECKING:               # pragma: no cover
    from ..snak import ValueSnakTemplate
    from ..statement import StatementTemplate
    from ..value import VTEntity, VTValue

TVariableClass: TypeAlias = Union[type['Variable'], type[Term]]


class Variable(OpenTerm):
    """Base class for variables.

    Parameters:
       name: Name.
       variable_class: Variable class.
    """

    def __new__(
            cls,
            name: str,
            variable_class: Optional[TVariableClass] = None
    ):
        if variable_class is None:
            variable_class = cls
        if (isinstance(variable_class, type)
                and issubclass(variable_class, ClosedTerm)
                and not issubclass(variable_class, cls)
                and hasattr(variable_class, 'variable_class')):
            variable_class = getattr(variable_class, 'variable_class')
        if (isinstance(variable_class, type)
                and issubclass(variable_class, cls)):
            return super().__new__(variable_class)  # pyright: ignore
        else:
            raise cls._check_error(variable_class, cls, 'variable_class', 2)

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, Variable):
            if issubclass(arg.__class__, cls):
                return cast(Self, arg)
            if issubclass(cls, arg.__class__):
                return cast(Self, cls(arg.name))
        raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            name: str,
            object_class: Optional[type[Term]] = None
    ):
        super().__init__(name)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            from ..value import String
            return String.check(arg, type(self), None, i).content
        else:
            raise self._should_not_get_here()

    @overload
    def __call__(self, v1: 'VTEntity', v2: 'VTValue') -> 'StatementTemplate':
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: 'VTValue') -> 'ValueSnakTemplate':
        ...                     # pragma: no cover

    def __call__(self, v1, v2=None):
        from ..value import PropertyVariable
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

    @override
    def _iterate_variables(self) -> Iterator['Variable']:
        return iter((self,))

    @override
    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Term]:
        if self in theta:
            return self._instantiate_tail(theta, function, name, position)
        elif coerce:
            for other in filter(lambda v: isinstance(v, Variable), theta):
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
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Term]:
        obj = theta[self]
        if obj is None:
            return obj
        else:
            from .template import Template
            if self.__class__ is Variable:
                obj_cls = Term
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
    for xs, variable_class in it(itertools.chain((name,), names)):
        for x in xs:
            yield Variable(x, variable_class)
