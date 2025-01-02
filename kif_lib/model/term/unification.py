# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import cast, Iterable, Set
from .template import Template
from .term import Term, Theta
from .variable import Variable


def unification(G: Set[tuple[Term | None, Term | None]]) -> Theta | None:
    """Computes an instantiation that unifies each pair of terms in `G`.

    The algorithm we implement here is an adaptation of Martelli &
    Montanari's 1982 algorithm described in Wikipedia
    <https://en.wikipedia.org/wiki/Unification_(computer_science)>.

    The main difference is the support for variable coercions and deletions
    (i.e., equations of the form `x=None`).

    Input-output behavior: "Given a finite set G:={s1=t1,...,sn=tn} of
    potential equations, the algorithm applies rules to transform it into an
    equivalent set of equations of the form {x1=u1,...,xm=um} where
    x1,...,xm are distinct variables and u1,...,um are terms containing none
    of the xi.  A set of this form can be read as a substitution [i.e.,
    variable instantiation theta]."

    Parameters:
       G: Set of pairs of terms (potential equations).

    Returns:
       A variable instantiation theta if successful; ``None`` otherwise.
    """
    return _unification(set(G))


class UnificationFailed(BaseException):
    """Unification failed."""


def _unification(G: set[tuple[Term | None, Term | None]]) -> Theta | None:
    done = False
    while not done:
        try:
            G, done = _unification_pass(G)
        except UnificationFailed:
            return None
    ###
    # TODO: Check whether the resulting `G` is a valid variable
    # instantiation.
    #
    # For instance,
    #
    #   x, y, z, w = Variables('x', 'y', 'z', 'w')
    #   A = QuantityTemplate(x, y, None, w)
    #   B = QuantityTemplate(y, z, x, w)
    #   theta = Term.unification((A, B))
    #
    # Produces the *invalid* instantiation `theta`:
    #
    #   {
    #       QuantityVariable('x'): None,
    #       ItemVariable('y'): ItemVariable('z'),
    #       QuantityVariable('y'): None,
    #   }
    #
    # Notice that variable ``y`` occurs twice with incompatible types.
    ###
    return cast(Theta, dict(G))


def _unification_pass(
        G: set[tuple[Term | None, Term | None]]
) -> tuple[set[tuple[Term | None, Term | None]], bool]:
    for pair in G:
        s, t = pair
        ###
        # DELETE:
        # G ∪ {s=t} and s == t ⇒ G
        ###
        if s == t:
            G.remove(pair)
            return G, False      # restart
        ###
        # DECOMPOSE:
        # G ∪ {f(s1,...,sn)=g(t1,...,tn)} ⇒ G ∪ {s1=t1,...,sn=tn}
        ###
        if not isinstance(s, Variable) and not isinstance(t, Variable):
            if s is None or t is None:
                raise UnificationFailed  # CONFLICT
            elif isinstance(s, Template) and isinstance(t, Template):
                if type(s) is not type(t):
                    raise UnificationFailed  # CONFLICT
            elif (not isinstance(s, Template)
                  and not isinstance(t, Template)):
                if s != t:
                    raise UnificationFailed  # CONFLICT
            elif isinstance(s, Template) and not isinstance(t, Template):
                if s.object_class is not type(t):
                    raise UnificationFailed  # CONFLICT
            elif not isinstance(s, Template) and isinstance(t, Template):
                if t.object_class is not type(s):
                    raise UnificationFailed  # CONFLICT
            else:
                raise Term._should_not_get_here()
            G.remove(pair)
            assert len(s.args) == len(t.args)
            for i, arg in enumerate(s.args):
                l, r = arg, t.args[i]
                if l is None or r is None:
                    if ((l is not None and not isinstance(l, Variable))
                            or (r is not None
                                and not isinstance(r, Variable))):
                        raise UnificationFailed  # CONFLICT
                if l is not None or r is not None:
                    from ..value import Value
                    if l is not None and not isinstance(l, Term):
                        l = Value.check(l)
                    if r is not None and not isinstance(r, Term):
                        r = Value.check(r)
                    G.add((l, r))
            return G, False     # restart
        ###
        # SWAP:
        # - G ∪ {f(s1..sn)=x} ⇒ G ∪ {x=f(s1..sn)}
        # - G ∪ {x=y} and x is (proper) coercible to y => G ∪ {y=x}
        ###
        if (isinstance(t, Variable)
            and (not isinstance(s, Variable)
                 or (type(s) is not type(t) and isinstance(s, type(t))))):
            G.remove(pair)
            G.add((t, s))
            return G, False     # restart
        ###
        # ELIMINATE:
        # G ∪ {x=t} ⇒ G[x:=t] ∪ {x=t}
        ###
        assert isinstance(s, Variable)
        try:
            # Attempt strict instantiation.
            s._instantiate_tail({s: t}, True, True)
        except Term.InstantiationError as err:
            raise UnificationFailed from err  # bad instantiation
        else:
            if (t is not None
                and not isinstance(t, Variable)
                    and _coercion_occurs_in(s, t.variables)):
                raise UnificationFailed  # CHECK
            H, theta, changed = {pair}, {s: t}, False
            for sx, tx in G:
                if sx == pair[0] and tx == pair[1]:
                    continue    # skip
                saved_sx, saved_tx = sx, tx
                try:
                    if sx is not None:
                        sx = cast(Term, sx.instantiate(theta, True, True))
                    if tx is not None:
                        tx = cast(Term, tx.instantiate(theta, True, True))
                except Term.InstantiationError as err:
                    raise UnificationFailed from err  # bad instantiation
                if sx != saved_sx or tx != saved_tx:
                    changed = True
                H.add((sx, tx))
            if changed:
                return H, False  # x ∈ G, restart
    ###
    # Done.
    ###
    return G, True


def _coercion_occurs_in(x: Variable, vars: Iterable[Variable]) -> bool:
    if x in vars:
        return True
    else:
        for var in vars:
            try:
                if var.check(x) == var:
                    return True
            except TypeError:
                pass
        return False
