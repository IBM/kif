# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from kif_lib.compiler.sparql.pattern_compiler import (
    SPARQL_PatternCompiler,
    TPattern,
)

from ...tests import TestCase


class Test(TestCase):

    def assert_compile(self, pat: TPattern, template: str):
        compiler = SPARQL_PatternCompiler(pat).compile()
        self.assertEqual(compiler.pattern, pat)
        try:
            self.assert_compiled_query_string(str(compiler.query), template)
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

#     def test_compile_item_template(self) -> None:
#         self.assert_compile(ItemTemplate(IRI_Variable('x')), f'''
# SELECT * WHERE {{
#   ?x <{WIKIBASE.sitelinks}> _: .
# }}
# ''')
#         self.assert_compile(
#             ItemTemplate(IRI_Template(StringVariable('x'))), f'''
# SELECT * WHERE {{
#   ?x <{WIKIBASE.sitelinks}> _: .
#   BIND (STR(?x) AS ?_v0)
# }}
# ''')

###
# FIXME: NOT WORKING!
###
#     def test_compile_item_variable(self) -> None:
#         self.assert_compile(ItemVariable('x'), f'''
# SELECT * WHERE {{
#   ?x <{SCHEMA.version}> _: .
# }}
# ''')

#     def test_compile_item(self) -> None:
#         self.assert_compile(Item('x'), f'''
# SELECT * WHERE {{
#   <x> <{WIKIBASE.sitelinks}> _: .
# }}
# ''')

# -- Property --------------------------------------------------------------

#     def test_compile_property_template(self) -> None:
#         self.assert_compile(PropertyTemplate(IRI_Variable('x')), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{WIKIBASE.Property}> .
# }}
# ''')
#         self.assert_compile(
#             PropertyTemplate(IRI_Template(StringVariable('x'))), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{WIKIBASE.Property}> .
#   BIND (STR(?x) AS ?_v0)
# }}
# ''')

###
# FIXME: NOT WORKING!
###
#     def test_compile_property_variable(self) -> None:
#         self.assert_compile(PropertyVariable('x'), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{WIKIBASE.Property}> .
# }}
# ''')

#     def test_compile_property(self) -> None:
#         self.assert_compile(Property('x'), f'''
# SELECT * WHERE {{
#   <x> <{RDF.type}> <{WIKIBASE.Property}> .
# }}
# ''')

# -- Lexeme ----------------------------------------------------------------

#     def test_compile_lexeme_template(self) -> None:
#         self.assert_compile(LexemeTemplate(IRI_Variable('x')), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
# }}
# ''')
#         self.assert_compile(
#             LexemeTemplate(IRI_Template(StringVariable('x'))), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
#   BIND (STR(?x) AS ?_v0)
# }}
# ''')

###
# FIXME: NOT WORKING!
###
#     def test_compile_lexeme_variable(self) -> None:
#         self.assert_compile(LexemeVariable('x'), f'''
# SELECT * WHERE {{
#   ?x <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
# }}
# ''')

#     def test_compile_lexeme(self) -> None:
#         self.assert_compile(Lexeme('x'), f'''
# SELECT * WHERE {{
#   <x> <{RDF.type}> <{ONTOLEX.LexicalEntry}> .
# }}
# ''')

# -- IRI -------------------------------------------------------------------

###
# FIXME: NOT WORKING!
###
#     def test_compile_iri_template(self) -> None:
#         self.assert_compile(IRI_Template(StringVariable('x')), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 ?x .
#         BIND (STR(?x) AS ?_v3)
#       }}
#     }}
#   }}
# }}
# ''')

###
# FIXME: NOT WORKING!
###
#     def test_compile_iri_variable(self) -> None:
#         self.assert_compile(IRI_Variable('x'), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 ?_v3 .
#       }}
#     }}
#   }}
# }}
# ''')

###
# FIXME: NOT WORKING!
###
#     def test_compile_iri(self) -> None:
#         self.assert_compile(IRI('x'), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Url}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 <x> .
#       }}
#     }}
#   }}
# }}
# ''')

# -- Text ------------------------------------------------------------------


###
# FIXME: NOT WORKING!
###
#     def test_compile_text_template(self) -> None:
#         self.assert_compile(
#             TextTemplate(StringVariable('x'), StringVariable('y')), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 ?x .
#         BIND (LANG(?x) AS ?_v3)
#       }}
#     }}
#   }}
# }}
# ''')
#         self.assert_compile(
#             TextTemplate('x', StringVariable('y')), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 ?_v3 .
#         BIND (LANG(?_v3) AS ?_v4)
#         FILTER ((STR(?_v3) = "x"))
#       }}
#     }}
#   }}
# }}
# ''')
#         self.assert_compile(
#             TextTemplate(StringVariable('x'), 'y'), f'''
# SELECT * WHERE {{
#   {{
#     ?_v0 <{RDF.type}> <{WIKIBASE.Property}> .
#     {{
#       {{
#         ?_v0 <{WIKIBASE.propertyType}> <{WIKIBASE.Monolingualtext}> .
#         ?_v0 <{WIKIBASE.statementProperty}> ?_v1 .
#         ?_v2 ?_v1 ?x .
#         FILTER ((LANG(?x) = "y"))
#       }}
#     }}
#   }}
# }}
# ''')


if __name__ == '__main__':
    Test.main()
