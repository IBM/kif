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
