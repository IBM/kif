# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import functools
from typing import TYPE_CHECKING

from ... import itertools
from ...typing import (
    Any,
    Callable,
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

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        has_tpl_or_var_arg = any(map(
            cls.is_open, itertools.chain(args, kwargs.values())))
        if (
                has_tpl_or_var_arg
                and hasattr(cls, 'template_class')
                and cls._is_proper_subclass_of_closed_term(cls)):
            return cast(Self, cls.template_class(  # type: ignore
                *args, **kwargs))
        elif (
                not has_tpl_or_var_arg
                and hasattr(cls, 'object_class')
                and cls._is_proper_subclass_of_template(cls)):
            return cast(Self, cls.object_class(  # type: ignore
                *args, **kwargs))
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

    def generalize(
            self,
            exclude: Iterable[Term | str] = (),
            rename: Callable[[str], Iterator[str]] | None = None,
            prefix: str | None = None
    ) -> Self:
        """Replaces ``None`` values occurring in term by fresh variables.

        Picks name variants not occurring in `exclude`.

        Uses `rename` (if given) to generate name variants.

        Uses `prefix` (if given) as prefix for name variants.

        Parameters:
           exclude: Name variant exclusion list.
           rename: Name variant generator.
           prefix: Name variant prefix.

        Returns:
           Term.
        """
        from .variable import Variable

        def it() -> Iterator[str | None]:
            if prefix is not None:
                yield prefix
            for i in itertools.count():
                if prefix is None:
                    yield None
                else:
                    yield prefix + str(i)
        names = it()
        exclude = list(exclude)

        def sigma(x: Any) -> Any:
            if x is None:
                nonlocal names  # noqa: F824
                var = Variable(next(names)).rename(exclude, rename)
                exclude.append(var)
                return var
            else:
                return x
        return self.substitute(sigma)

    def rename(
            self,
            exclude: Iterable[Term | str] = (),
            rename: Callable[[str], Iterator[str]] | None = None
    ) -> Self:
        """Renames all variables occurring in term.

        Picks name variants not occurring in `exclude`.

        Uses `rename` (if given) to generate name variants.

        Parameters:
           exclude: Name exclusion list.
           rename: Name variant generator.

        Returns:
           Term.
        """
        from .variable import Variable
        xnames, xterms = cast(
            tuple[Iterator[str], Iterator[Term]],
            itertools.partition(lambda x: isinstance(x, Term), exclude))
        exclude_set = set(itertools.chain(
            map(Variable.get_name, itertools.chain(
                *map(Term.get_variables, xterms))), xnames))
        return self._rename(exclude_set, rename)

    def _rename(
            self,
            exclude: Set[str],
            rename: Callable[[str], Iterator[str]] | None
    ) -> Self:
        theta = {x: x._rename(exclude, rename) for x in self.variables}
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
    def _rename(
            self,
            exclude: Set[str],
            rename: Callable[[str], Iterator[str]] | None
    ) -> Self:
        return self             # nothing to do


class OpenTerm(Term):
    """Abstract base class for open terms."""

    #: Closed-term class associated with this open-term class.
    object_class: ClassVar[type[ClosedTerm]]
