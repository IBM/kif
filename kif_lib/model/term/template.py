# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import itertools
from ...typing import Any, cast, ClassVar, Iterator, Location, override
from .term import ClosedTerm, OpenTerm, Term, Theta
from .variable import Variable


class Template(OpenTerm):
    """Abstract base class for templates."""

    #: Object class associated with this template class.
    object_class: ClassVar[type[ClosedTerm]]

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
        vars = frozenset(itertools.chain(*map(
            OpenTerm.get_variables, filter(self.is_open, args))))
        most_specific: dict[str, Variable] = {}
        for var in vars:
            if var.name not in most_specific:
                most_specific[var.name] = var
            else:
                cur = most_specific[var.name]
                assert var != cur  # as there are no repetitions in vars
                most_specific[var.name] = cur.check(var, type(self))
        theta: dict[Variable, Variable] = {}
        for var in vars:
            if var.name in most_specific and most_specific[var.name] != var:
                theta[var] = most_specific[var.name]
        if not theta:
            return args
        else:
            return tuple(map(
                lambda x: x._instantiate(theta, False, False)
                if self.is_open(x) else x, args))

    @override
    def _iterate_variables(self) -> Iterator[Variable]:
        return self._traverse(lambda x: isinstance(x, Variable), self.is_open)

    @override
    def instantiate(
            self,
            theta: Theta,
            coerce: bool = True,
            strict: bool = False
    ) -> Term:
        return cast(Term, super().instantiate(theta, coerce, strict))

    @override
    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term:
        try:
            return type(self)(*map(
                lambda arg: arg._instantiate(
                    theta, coerce, strict, function, name, position)
                if isinstance(arg, OpenTerm) else arg, self.args))
        except TypeError as err:
            raise self.InstantiationError from err
