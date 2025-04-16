# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..model import (
    Entity,
    Graph,
    IRI,
    KIF_Object,
    NoValueSnak,
    Quantity,
    SomeValueSnak,
    Statement,
    Time,
    ValueSnak,
)
from ..model.kif_object import Encoder, Object
from ..typing import Any, Iterator, override


class DotEncoder(
        Encoder,
        format='dot',
        description='Dot encoder'
):
    """Dot encoder."""

    @classmethod
    def _to_graphviz(cls, input: Object) -> Any:
        try:
            from graphviz import Digraph  # type: ignore
        except ImportError as err:
            raise ImportError(
                f'{cls.__qualname__} requires '
                'https://pypi.org/project/graphviz/') from err
        if isinstance(input, Statement):
            input = Graph(input)
        if not isinstance(input, Graph):
            raise cls._error(f'cannot encode to Dot: {input}')
        assert isinstance(input, Graph)
        g = Digraph()
        g.attr(rankdir='LR')
        g.attr('node', fontname='arial', fontsize='10', shape='plain')
        g.attr(
            'edge', fontname='arial', fontsize='9',
            arrowsize='.65', arrowhead='vee')
        for stmt in input:
            s = stmt.subject
            p = stmt.snak.property
            g.node(name=s.digest, label=s.display())
            if isinstance(stmt.snak, ValueSnak):
                v = stmt.snak.value
                label: str
                if isinstance(v, Entity):
                    label = v.display()
                elif isinstance(v, IRI):
                    label = f'<{v.content}>'
                elif isinstance(v, Quantity):
                    label = str(v.amount)
                    if v.unit:
                        label += ' ' + v.unit.display()
                elif isinstance(v, Time):
                    label = str(v.time)
                else:
                    label = v.to_markdown()
                g.node(name=v.digest, label=label)
                g.edge(s.digest, v.digest, label=p.display())
            elif isinstance(stmt.snak, SomeValueSnak):
                g.edge(s.digest, s.digest,
                       label=p.display() + ' (some value)')
            elif isinstance(stmt.snak, NoValueSnak):
                g.edge(s.digest, s.digest,
                       label=p.display() + ' (no value)')
            else:
                raise KIF_Object._should_not_get_here()
        return g

    @override
    def iterencode(self, input: Object) -> Iterator[str]:
        yield self._to_graphviz(input).source
