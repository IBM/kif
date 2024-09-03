# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import Any, Iterable, Set
from .template import Template
from .term import Term, Theta
from .variable import Variable


def unification(G: Set[tuple[Term, Term]]) -> Theta | None:
    """Computes an instantiation that unifies each pair of terms in `G`.

    Implements the Martelli & Montanari (1982) algorithm described in
    Wikipedia <https://en.wikipedia.org/wiki/Unification_(computer_science)>:

    "Given a finite set G:={s1=t1,...,sn=tn} of potential equations, the
    algorithm applies rules to transform it to an equivalent set of
    equations of the form {x1=u1,...,xm=um} where x1,...,xm are distinct
    variables and u1,...,um are terms containing none of the xi.  A set of
    this form can be read as a substitution."

    Parameters:
       G: Set of pairs of terms (potential equations).

    Returns:
       A variable instantiation theta if successful; ``None`` otherwise.
    """
    return _unification(set(G))


def _unification(G: set[tuple[Any, Any]]) -> Theta | None:
    while True:
        done = True
        for pair in G:
            s, t = pair
            ###
            # DELETE:
            # G ∪ {s=t} and s == t ⇒ G
            ###
            if s == t:
                G.remove(pair)
                done = False
                break
            ###
            # DECOMPOSE:
            # G ∪ {f(s1,...,sn)=g(t1,...,tn)} ⇒ G ∪ {s1=t1,...,sn=tn}
            ###
            if not isinstance(s, Variable) and not isinstance(t, Variable):
                if isinstance(s, Template) and isinstance(t, Template):
                    if type(s) != type(t):
                        return None  # fail
                elif (not isinstance(s, Template)
                      and not isinstance(t, Template)):
                    if s != t:
                        return None  # fail
                elif isinstance(s, Template) and not isinstance(t, Template):
                    if s.object_class is not type(t):
                        return None  # fail
                elif not isinstance(s, Template) and isinstance(t, Template):
                    if t.object_class is not type(s):
                        return None  # fail
                else:
                    raise Term._should_not_get_here()
                G.remove(pair)
                assert len(s.args) == len(t.args)
                for i, arg in enumerate(s.args):
                    G.add((arg, t.args[i]))
                done = False
                break
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
                done = False
                break
            ###
            # INSTANTIATION CHECK:
            # G ∪ {x=t} and x cannot be instantiate with t ⇒ ⊥
            ###
            if isinstance(s, Variable):
                try:
                    s._instantiate_tail({s: t})
                except Variable.InstantiationError:
                    return None  # fail
            ###
            # ELIMINATE:
            # G ∪ {x=t} ⇒ G[x:=t] ∪ {x=t}
            ###
            if isinstance(s, Variable) and isinstance(t, Template):
                if _coercion_occurs_in(s, t.variables):
                    return None  # fail: x ∈ t
                G.remove(pair)
                H, theta, changed = set(), {s: t}, False
                for sx, tx in G:
                    saved_sx, saved_tx = sx, tx
                    sx = sx.instantiate(theta)
                    tx = tx.instantiate(theta)
                    if sx != saved_sx or tx != saved_tx:
                        changed = True
                    H.add((sx, tx))
                G = H
                G.add(pair)
                done = not changed
                break
        if done:
            return dict(G)


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
