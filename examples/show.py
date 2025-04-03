# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

def property_table(ps):
    from IPython.display import display_markdown

    def it():
        yield '#', 'property', 'description'
        yield '-', '-', '-'
        for i, p in enumerate(ps, 1):
            yield (str(i), f'[{p.label.content}]({p.iri.content})',
                   p.description.content)
    display_markdown('\n'.join(map(
        lambda t: f'|{"|".join(t)}|', it())), raw=True)
