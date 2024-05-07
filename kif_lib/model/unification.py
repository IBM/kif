# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, Iterable, Optional, Set
from .kif_object import KIF_Object
from .template import Template
from .variable import Theta, Variable

# See: <https://en.wikipedia.org/wiki/
#       Unification_(computer_science)#Unification_algorithms>


def unify(G: Set[tuple[KIF_Object, KIF_Object]]) -> Optional[Theta]:
    return _unify(set(G))


def _unify(G: set[tuple[Any, Any]]) -> Optional[Theta]:
    while True:
        done = True
        for p in G:
            s, t = p
            ###
            # DELETE:
            # G ∪ {s=t} and s == t ⇒ G
            ###
            if s == t:
                G.remove(p)
                done = False
                break
            ###
            # DECOMPOSE:
            # G ∪ {f(s1..sn)=g(t1..tn)} ⇒ G ∪ {s1=t1..sn=tn}
            ###
            if not isinstance(s, Variable) and not isinstance(t, Variable):
                if isinstance(s, Template) and isinstance(t, Template):
                    if s.__class__ != t.__class__:
                        return None  # fail: f != g
                elif (not isinstance(s, Template)
                      and not isinstance(t, Template)):
                    if s != t:
                        return None  # fail: f != g
                elif isinstance(s, Template) and not isinstance(t, Template):
                    if s.object_class != t.__class__:
                        return None  # fail: f != g
                elif not isinstance(s, Template) and isinstance(t, Template):
                    if t.object_class != s.__class__:
                        return None  # fail: f != g
                else:
                    raise KIF_Object._should_not_get_here()
                G.remove(p)
                assert len(s.args) == len(t.args)
                for i in range(len(s.args)):
                    G.add((s.args[i], t.args[i]))
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
            # SWAP:
            # G ∪ {f(s1..sn)=x} ⇒ G ∪ {x=f(s1..sn)}
            ###
            if not isinstance(s, Variable) and isinstance(t, Variable):
                G.remove(p)
                G.add((t, s))
                done = False
                break
            ###
            # ELIMINATE:
            # G ∪ {x=t} ⇒ G[x:=t] ∪ {x=t}
            ###
            if isinstance(s, Variable) and isinstance(t, Template):
                if _coercion_occurs_in(s, t.variables):
                    return None  # fail: x ∈ t
                G.remove(p)
                H, theta, changed = set(), {s: t}, False
                for sx, tx in G:
                    saved_sx, saved_tx = sx, tx
                    sx = sx.instantiate(theta)
                    tx = tx.instantiate(theta)
                    if sx != saved_sx or tx != saved_tx:
                        changed = True
                    H.add((sx, tx))
                G = H
                G.add(p)
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
                if x._coerce(var.__class__) == var:
                    return True
            except Variable.CoercionError:
                pass
        return False
