# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from kif_lib.compiler.sparql.compiler import SPARQL_Compiler
from kif_lib.model import (
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    Pattern,
    Property,
    PropertyTemplate,
    PropertyVariable,
    StringVariable,
    TextTemplate,
)
from kif_lib.namespace import ONTOLEX, RDF, SCHEMA, WIKIBASE

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def assert_compile(self, pat: Pattern, template: str):
        res = SPARQL_Compiler(pat).compile()
        self.assertEqual(res.pattern, pat)
        try:
            self.assert_compiled_query_string(str(res.query), template)
        except AssertionError as err:
            print('-- expected --')
            print(template.strip())
            print('-- got --')
            m = re.match(r'.* not found in ["\'](.*)["\']$', err.args[0])
            assert m is not None
            print(re.sub(r'\\n', '\n', m.group(1)))
            raise err

    def assert_compiled_query_string(
            self,
            query: str,
            template: str,
            _pat=re.compile('_:')
    ):
        regex = _pat.sub(r'_:\\w+', re.escape(template.strip()))
        self.assertRegex(query, regex)

# -- Item ------------------------------------------------------------------

    def test_compile_item_template(self):
        self.assert_compile(ItemTemplate(IRI_Variable('x')), f'''
SELECT * WHERE {{
  ?x <{SCHEMA.version}> _: .
}}
''')
        self.assert_compile(
            ItemTemplate(IRI_Template(StringVariable('x'))), f'''
SELECT * WHERE {{
  ?x <{SCHEMA.version}> _: .
  BIND (STR(?x) AS ?_v0)
}}
''')

    def test_compile_item_variable(self):
        self.assert_compile(ItemVariable('x'), f'''
SELECT * WHERE {{
  ?x <{SCHEMA.version}> _: .
}}
''')

    def test_compile_item(self):
        self.assert_compile(Item('x'), f'''
SELECT * WHERE {{
  <x> <{SCHEMA.version}> _: .
}}
''')

# -- Property --------------------------------------------------------------

    def test_compile_property_template(self):
        self.assert_compile(PropertyTemplate(IRI_Variable('x')), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{WIKIBASE.Property}> .
}}
''')
        self.assert_compile(
            PropertyTemplate(IRI_Template(StringVariable('x'))), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{WIKIBASE.Property}> .
  BIND (STR(?x) AS ?_v0)
}}
''')

    def test_compile_property_variable(self):
        self.assert_compile(PropertyVariable('x'), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{WIKIBASE.Property}> .
}}
''')

    def test_compile_property(self):
        self.assert_compile(Property('x'), f'''
SELECT * WHERE {{
  <x> <{RDF.type}> <{WIKIBASE.Property}> .
}}
''')

# -- Lexeme ----------------------------------------------------------------

    def test_compile_lexeme_template(self):
        self.assert_compile(LexemeTemplate(IRI_Variable('x')), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
}}
''')
        self.assert_compile(
            LexemeTemplate(IRI_Template(StringVariable('x'))), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
  BIND (STR(?x) AS ?_v0)
}}
''')

    def test_compile_lexeme_variable(self):
        self.assert_compile(LexemeVariable('x'), f'''
SELECT * WHERE {{
  ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
}}
''')

    def test_compile_lexeme(self):
        self.assert_compile(Lexeme('x'), f'''
SELECT * WHERE {{
  <x> <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
}}
''')

# -- IRI -------------------------------------------------------------------

    def test_compile_iri_template(self):
        self.assert_compile(IRI_Template(StringVariable('x')), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 ?x .
        BIND (STR(?x) AS ?_v3)
      }}
    }}
  }}
}}
''')

    def test_compile_iri_variable(self):
        self.assert_compile(IRI_Variable('x'), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 ?_v3 .
      }}
    }}
  }}
}}
''')

    def test_compile_iri(self):
        self.assert_compile(IRI('x'), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 <x> .
      }}
    }}
  }}
}}
''')

# -- Text ------------------------------------------------------------------

    def test_compile_text_template(self):
        self.assert_compile(
            TextTemplate(StringVariable('x'), StringVariable('y')), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 ?x .
        BIND (LANG(?x) AS ?_v3)
      }}
    }}
  }}
}}
''')
        self.assert_compile(
            TextTemplate('x', StringVariable('y')), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 ?_v3 .
        BIND (LANG(?_v3) AS ?_v4)
        FILTER ((STR(?_v3) = "x"))
      }}
    }}
  }}
}}
''')
        self.assert_compile(
            TextTemplate(StringVariable('x'), 'y'), f'''
SELECT * WHERE {{
  {{
    ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
    {{
      {{
        ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
        ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
        ?_v2 ?_v1 ?x .
        FILTER ((LANG(?x) = "y"))
      }}
    }}
  }}
}}
''')


if __name__ == '__main__':
    Test.main()
