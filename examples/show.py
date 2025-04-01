# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

def property_table(ps):
    from IPython.display import display_markdown
    def it():
        yield 'property', 'description'
        yield '-', '-'
        for p in ps:
            yield (f'[{p.label.content}]({p.iri.content})',
                   p.description.content)
    display_markdown('\n'.join(map(
        lambda t: f'|{t[0]}|{t[1]}|', it())), raw=True)


def graph(*stmts):
    from graphviz import Digraph
    from kif_lib import Entity, IRI, Quantity, Time, ValueSnak
    g = Digraph()
    g.attr(rankdir='LR')
    g.attr('node', fontname='arial', fontsize='10', shape='plain')
    g.attr('edge', fontname='arial', fontsize='9',
           arrowsize='.65', arrowhead='vee')
    for stmt in stmts:
        s = stmt.subject
        g.node(name=s.digest, label=s.display())
        if isinstance(stmt.snak, ValueSnak):
            v = stmt.snak.value
            if isinstance(v, Entity):
                g.node(name=v.digest, label=v.display())
            elif isinstance(v, Quantity):
                g.node(name=v.digest, label=str(v.amount))
            elif isinstance(v, Time):
                g.node(name=v.digest, label=str(v.time))
            elif isinstance(v, IRI):
                g.node(name=v.digest, label=v.content)
            else:
                g.node(name=v.digest, label=v.to_markdown())
        g.edge(s.digest, v.digest, label=stmt.snak.property.display())
    display(g)
