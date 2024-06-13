# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..itertools import chain
from ..typing import (
    Any,
    ClassVar,
    Iterator,
    Mapping,
    Optional,
    Set,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object, KIF_ObjectClass, TLocation
from .variable import Theta, Variable

TemplateClass: TypeAlias = type['Template']
TTemplateClass: TypeAlias = Union[TemplateClass, KIF_ObjectClass]


class Template(KIF_Object):
    """Abstract base class for templates."""

    #: Object class associated with this template class.
    object_class: ClassVar[KIF_ObjectClass]

    @classmethod
    def _check_arg_template_class(
            cls,
            arg: TTemplateClass,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TemplateClass:
        if issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'template_class'),
                f'no template class for {arg.__qualname__}',
                function, name, position), 'template_class')

    def _preprocess_args(self, args: tuple[Any, ...]) -> tuple[Any, ...]:
        return self._normalize_args(super()._preprocess_args(args))

    def _normalize_args(self, args: tuple[Any, ...]) -> tuple[Any, ...]:
        ###
        # A template is *normal* iff for every two variables ``x``, ``y`` in
        # the template, ``x.name == y.name`` implies ``type(x) == type(y)``.
        #
        # We normalize a template by normalizing its arguments, i.e., by
        # replacing homonymous occurrences of a same variable by the
        # occurrence with the most specific type.  For example, if
        # ItemVariable('v') and EntityVariable('v') occur in the arguments
        # of the template, we replace all occurrences of the latter by
        # ItemVariable('v').
        #
        # Note that normalization is only possible if the homonymous
        # variables are inter-coercible.  This method will throw an error if
        # that is not the case.
        ###
        vars = frozenset(chain(*map(
            lambda x: (x,) if Variable.test(x) else x.variables,
            filter(self._isinstance_template_or_variable, args))))
        most_specific: dict[str, Variable] = {}
        for var in vars:
            if var.name not in most_specific:
                most_specific[var.name] = var
            else:
                cur = most_specific[var.name]
                assert var != cur  # as there are no repetitions in vars
                most_specific[var.name] = var._coerce(
                    cur.__class__, self.__class__)
        theta: dict[Variable, Variable] = {}
        for var in vars:
            if var.name in most_specific and most_specific[var.name] != var:
                theta[var] = most_specific[var.name]
        if not theta:
            return args
        else:
            return tuple(map(
                lambda x: x._instantiate(theta, False)
                if self._isinstance_template_or_variable(x) else x, args))

    @property
    def variables(self) -> Set[Variable]:
        """The set of variables occurring in template."""
        return self.get_variables()

    def get_variables(self) -> Set[Variable]:
        """Gets the set of variables occurring in template.

        Returns:
           Set of variables.
        """
        return frozenset(self._iterate_variables())

    def _iterate_variables(self) -> Iterator[Variable]:
        return self._traverse(
            Variable.test, self._isinstance_template_or_variable)

    def instantiate(self, theta: Theta, coerce: bool = True) -> KIF_Object:
        """Applies variable instantiation `theta` to template.

        Parameters:
           theta: A mapping of variables to objects or ``None``.
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
    ) -> KIF_Object:
        return self.__class__(*map(
            lambda arg: arg._instantiate(
                theta, coerce, function, name, position)
            if isinstance(arg, (Template, Variable)) else arg, self.args))
