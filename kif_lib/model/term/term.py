# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import functools
from typing import TYPE_CHECKING

from ... import itertools
from ...typing import (
    Any,
    cast,
    ClassVar,
    Iterable,
    Iterator,
    Location,
    Mapping,
    Optional,
    override,
    Self,
    Set,
    TypeAlias,
)
from ..kif_object import KIF_Object

if TYPE_CHECKING:               # pragma: no cover
    from .template import Template
    from .variable import Variable

#: The type of variable instantiations.
Theta: TypeAlias = Mapping['Variable', Optional['Term']]


class Term(KIF_Object):
    """Abstract base class for terms."""

    class InstantiationError(ValueError):
        """Bad instantiation attempt."""

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

    @classmethod
    def unify(
            cls,
            *eqs: tuple[Term, Term]
    ) -> Theta | None:
        """Computes an instantiation that unifies term equations.

        Parameters:
           eqs: Pairs of terms (potential equations).

        Returns:
           A variable instantiation theta if successful; ``None`` otherwise.
        """
        from .unification import unification
        return unification(set(eqs))

    @property
    def variables(self) -> Set[Variable]:
        """The set of variables occurring in term."""
        return self.get_variables()

    def get_variables(self) -> Set[Variable]:
        """Gets the set of variables occurring in term.

        Returns:
           Set of variables.
        """
        return self._get_variables_cached(self)

    @classmethod
    @functools.cache
    def _get_variables_cached(cls, term: Term) -> Set[Variable]:
        return frozenset(term._iterate_variables())

    @abc.abstractmethod
    def _iterate_variables(self) -> Iterator[Variable]:
        raise NotImplementedError

    def instantiate(
            self,
            theta: Theta,
            coerce: bool = True,
            strict: bool = False
    ) -> Term | None:
        """Applies variable instantiation `theta` to term.

        Parameters:
           theta: Variable instantiation.
           coerce: Whether to consider coercible variables equal.
           strict: Whether to adopt stricter coercion rules.

        Returns:
           Term or ``None``.
        """
        self._check_arg_isinstance(
            theta, Mapping, self.instantiate, 'theta', 1)
        return self._instantiate(
            theta, coerce, strict, self.instantiate) if theta else self

    @abc.abstractmethod
    def _instantiate(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term | None:
        raise NotImplementedError

    def match(self, other: Term) -> Theta | None:
        """Tests whether term matches `other`.

        If term matches `other`, returns a variable instantiation theta that
        can be used to unify both term and `other`.  Otherwise, return
        ``None``.

        Parameters:
           other: Term.

        Returns:
           A variable instantiation theta if successful; ``None`` otherwise.
        """
        return self.unify((self, Term.check(other, self.match, 'other', 1)))

    def rename(self, exclude: Iterable[Term | str] = ()) -> Self:
        """Rename all variables occurring in term.

        Pick new names that do conflict with those [of variables] in `exclude`.

        Parameters:
           exclude: Exclusion list.

        Returns:
           Term.
        """
        from .variable import Variable
        xnames, xterms = cast(
            tuple[Iterator[str], Iterator[Term]],
            itertools.partition(lambda x: isinstance(x, Term), exclude))
        excluded = set(itertools.chain(
            map(Variable.get_name, itertools.chain(
                *map(Term.get_variables, xterms))), xnames))
        return self._rename(excluded)

    def _rename(self, excluded: Set[str]) -> Self:
        theta = {x: x._rename(excluded) for x in self.variables}
        return cast(Self, self.instantiate(theta))


class ClosedTerm(Term):
    """Abstract base class for closed (ground) terms."""

    #: Template class associated with this closed-term class.
    template_class: ClassVar[type[Template]]

    #: Variable class associated with this closed-term class.
    variable_class: ClassVar[type[Variable]]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
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

    @override
    def _iterate_variables(self) -> Iterator[Variable]:
        return iter(())

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
    ) -> Term | None:
        return self

    @override
    def rename(self, exclude: Iterable[Term | str] = ()) -> Self:
        return self             # nothing to do


class OpenTerm(Term):
    """Abstract base class for open terms."""

    #: Closed-term class associated with this open-term class.
    object_class: ClassVar[type[ClosedTerm]]
