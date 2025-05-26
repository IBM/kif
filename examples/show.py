# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from IPython.display import display_markdown


def property_table(ps):
    def it():
        yield '#', 'property', 'description'
        yield '-', '-', '-'
        for i, p in enumerate(ps, 1):
            yield (str(i), f'[{p.display()}]({p.iri.content})',
                   p.description.content if p.description else '(no description)')
    display_markdown('\n'.join(map(
        lambda t: f'|{"|".join(t)}|', it())), raw=True)


def statement_table(stmts):
    import kif_lib

    def it():
        yield '#', 'subject', 'property', 'value'
        yield '-', '-', '-', '-'
        for i, stmt in enumerate(stmts, 1):
            subj, snak = stmt.subject, stmt.snak
            s = f'[{subj.display()}]({subj.iri.content})'
            p = f'[{snak.property.display()}]({snak.property.iri.content})'
            if isinstance(snak, kif_lib.ValueSnak):
                if isinstance(snak.value, (kif_lib.Item, kif_lib.Property)):
                    v = f'[{snak.value.label.content}]({snak.value.iri.content})'
                elif isinstance(snak.value, kif_lib.Quantity):
                    q = snak.value
                    v = str(q.amount)
                    if q.unit is not None:
                        v += ' ' + f'[{q.unit.display()}]({q.unit.iri.content})'
                else:
                    v = snak.value.to_markdown()
            elif isinstance(snak, kif_lib.SomeValueSnak):
                v = '(unknown)'
            elif isinstance(snak, kif_lib.NoValueSnak):
                v = '(no value)'
            else:
                raise RuntimeError('should not get here')
            yield (str(i), s, p, v)
    display_markdown('\n'.join(map(
        lambda t: f'|{"|".join(t)}|', it())), raw=True)