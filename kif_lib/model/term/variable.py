# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from typing_extensions import overload

from ... import itertools
from ...typing import (
    Any,
    Callable,
    cast,
    Final,
    Iterator,
    Location,
    override,
    Self,
    Set,
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
       name: Name or ``None`` (fresh name).
       variable_class: Variable class.
    """

    def __new__(
            cls,
            name: str | None = None,
            variable_class: TVariableClass | None = None
    ):
        variable_class = cls._check_variable_class(
            variable_class, cls, 'variable_class', 2)
        assert isinstance(variable_class, type)
        assert issubclass(variable_class, cls)
        return super().__new__(variable_class)  # pyright: ignore

    @classmethod
    def _check_variable_class(
            cls,
            variable_class: TVariableClass | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> type[Variable]:
        if variable_class is None:
            variable_class = cls
        if (isinstance(variable_class, type)
            and issubclass(variable_class, ClosedTerm)  # pyright: ignore
            and not issubclass(variable_class, cls)
                and hasattr(variable_class, 'variable_class')):
            variable_class = getattr(variable_class, 'variable_class')
        if (isinstance(variable_class, type)
                and issubclass(variable_class, cls)):
            return variable_class
        else:
            raise cls._check_error(variable_class, function, name, position)

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, Variable):
            if issubclass(type(arg), cls):
                return cast(Self, arg)
            if issubclass(cls, type(arg)):
                return cast(Self, cls(arg.name))
        raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            name: str | None = None,
            object_class: type[Term] | None = None
    ) -> None:
        super().__init__(name)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            from ..value import String
            if arg is None:     # name
                return self._fresh_id()
            else:
                return String.check(arg, type(self), None, i).content
        else:
            raise self._should_not_get_here()

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> StatementTemplate:
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> ValueSnakTemplate:
        ...                     # pragma: no cover

    def __call__(
            self,
            v1: VTEntity | VTValue,
            v2: VTValue | None = None
    ) -> StatementTemplate | ValueSnakTemplate:
        from ..value import PropertyVariable
        prop = PropertyVariable.check(self)
        if v2 is not None:
            return prop(v1, v2)  # type: ignore
        else:
            return prop(v1)

    def __matmul__(self, variable_class: TVariableClass) -> Self:
        return self.coerce(variable_class)

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

    def coerce(
            self,
            variable_class: TVariableClass | None = None,
    ) -> Self:
        """Coerces variable into `variable_class`.

        If variable cannot be coerced, raises an error.

        Parameters:
           variable_class: Variable class.

        Returns:
           Variable.
        """
        variable_class = Variable._check_variable_class(
            variable_class, self.coerce, 'variable_class', 1)
        assert isinstance(variable_class, type)
        if issubclass(type(self), variable_class):
            return self
        else:
            return cast(Self, variable_class.check(
                self, self.coerce, 'variable_class', 1))

    @override
    def _iterate_variables(self) -> Iterator[Variable]:
        return iter((self,))

    @override
    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term | None:
        if self in theta:
            return self._instantiate_tail(
                theta, coerce, strict, function, name, position)
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
                            theta, coerce, strict, function, name, position)
            return self
        else:
            return self

    def _instantiate_tail(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term | None:
        obj = theta[self]
        if obj is None:
            return obj
        else:
            from .template import Template
            if type(self) is Variable:
                obj_cls = Term
            elif isinstance(obj, Template):
                if hasattr(self.object_class, 'template_class'):
                    obj_cls = self.object_class.template_class
                else:
                    obj_cls = type(self)
            elif isinstance(obj, Variable):
                obj_cls = type(self)
            else:
                obj_cls = self.object_class
            if isinstance(obj, obj_cls):
                return obj
            else:
                src = type(self).__qualname__
                dest = type(obj).__qualname__
                raise self._arg_error(
                    f"cannot instantiate {src} '{self.name}' with {dest}",
                    function, name, position, self.InstantiationError)

    @override
    def _rename(
            self,
            exclude: Set[str],
            rename: Callable[[str], Iterator[str]] | None
    ) -> Self:
        rename = rename or self._rename_default_rename
        for name in rename(self.name):
            if name not in exclude:
                return self.replace(name, self.KEEP)
        raise self._should_not_get_here()

    _rename_default_rename_re: Final[re.Pattern] =\
        re.compile(r'(.*?)(\d*)$')

    def _rename_default_rename(self, name: str) -> Iterator[str]:
        m = self._rename_default_rename_re.match(name)
        assert m is not None
        prefix, suffix = m.groups()
        return map(lambda n: prefix + str(n),
                   itertools.count(int(suffix or -1) + 1))


def Variables(
        name: str | None,
        *names: str | TVariableClass | None
) -> Iterator[Variable]:
    """Constructs one or more variables.

    Parameters:
       name: Name or ``None`` (fresh name).
       names: Names or ``None`` values (fresh names) or variable classes.

    Returns:
       The resulting variables.
    """
    def it(
            args: Iterator[str | TVariableClass | None]
    ) -> Iterator[tuple[list[str | None], TVariableClass | None]]:
        vars: list[str | None] = []
        for x in args:
            if x is None or isinstance(x, str):
                vars.append(x)
            elif vars:
                yield (vars, x)
                vars = []
        if vars:
            yield (vars, None)
    for xs, variable_class in it(itertools.chain((name,), names)):
        for x in xs:
            yield Variable(x, variable_class)
