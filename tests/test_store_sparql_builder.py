# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import IRI, String
from kif.store.sparql_builder import SPARQL_Builder

from .tests import kif_TestCase, main


class TestSPARQL_Builder(kif_TestCase):

    def test__init__(self):
        q = SPARQL_Builder()
        self.assertIsInstance(q, SPARQL_Builder)

    def test_BNode(self):
        q = SPARQL_Builder()
        self.assertEqual(q._bcnt, 0)
        self.assertFalse(bool(q._bnodes))
        self.assertFalse(bool(q._bnodes))
        a, b = q.bnodes(2)
        a1 = q.bnode()
        self.assertEqual(a.id, 0)
        self.assertEqual(b.id, 1)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, a1)

    def test_Variable(self):
        q = SPARQL_Builder()
        self.assertFalse(bool(q._vars))
        self.assertFalse(bool(q._vals))
        a, b = q.vars('a', 'b')
        a1 = q.var('a')
        self.assertEqual(a.id, 'a')
        self.assertEqual(b.id, 'b')
        self.assertNotEqual(a, b)
        self.assertEqual(a, a1)
        self.assertEqual(a.n3(), '?a')

    # -- Builtin calls -----------------------------------------------------

    def test_concat_(self):
        q = SPARQL_Builder()
        self.assertEqual(
            q.concat(IRI('x'), q.var('y'), String('z')),
            'concat(<x>, ?y, "z")')

    def test_str_(self):
        q = SPARQL_Builder()
        self.assertEqual(q.str_(IRI('x')), 'str(<x>)')

    def test_substr(self):
        q = SPARQL_Builder()
        self.assertEqual(q.substr(IRI('x'), 8), 'substr(<x>, 8)')
        self.assertEqual(q.substr(IRI('x'), 8, 2), 'substr(<x>, 8, 2)')
        self.assertEqual(
            q.str_(q.substr(IRI('x'), 8, 2)), 'str(substr(<x>, 8, 2))')

    def test_uri_(self):
        q = SPARQL_Builder()
        self.assertEqual(q.uri(String('x')), 'uri("x")')

    # -- Patterns ----------------------------------------------------------

    def test_bind(self):
        q = SPARQL_Builder()
        self.assertIs(q.bind(IRI('x'), q.var('x')), q)
        self.assertEqual(q[-1], 'bind(<x> as ?x)')
        self.assertIs(q.bind(q.var('x'), q.var('x')), q)
        self.assertEqual(q[-1], 'bind(?x as ?x)')
        self.assertTrue(q.has_variable(q.var('x')))
        self.assertTrue(q.has_value(IRI('x')))
        b0 = q.bnode()
        self.assertIs(q.bind(b0, q.var('x')), q)
        self.assertEqual(q[-1], 'bind(_:b0 as ?x)')
        self.assertTrue(q.has_bnode(b0))
        self.assertFalse(q.has_bnode(q.bnode()))

    def test_triple(self):
        q = SPARQL_Builder()
        x, y = q.vars('x', 'y')
        u = IRI('u')
        s = String('s')
        self.assertIs(q.triple(x, u, y), q)
        self.assertEqual(q[-1], '?x <u> ?y .')
        self.assertIs(q.triple(u, x, s), q)
        self.assertEqual(q[-1], '<u> ?x "s" .')
        self.assertTrue(q.has_variable(q.var('x')))
        self.assertTrue(q.has_variable(q.var('y')))
        self.assertTrue(q.has_value(IRI('u')))
        self.assertTrue(q.has_value(String('s')))

    def test_group(self):
        q = SPARQL_Builder()
        with q.group(cond=False):
            pass
        self.assertEqual(len(q), 0)
        with q.group():
            self.assertEqual(q[-1], '{')
            with q.group():
                self.assertEqual(q[-1], '{')
                with q.group():
                    self.assertEqual(q[-1], '{')
                self.assertEqual(q[-1], '}')
            self.assertEqual(q[-1], '}')
        self.assertEqual(q[-1], '}')
        self.assertEqual(q.typeset(), '''\
{
  {
    {
    }
  }
}''')

    def test_optional(self):
        q = SPARQL_Builder()
        with q.optional(cond=False):
            pass
        self.assertEqual(len(q), 0)
        with q.optional():
            self.assertEqual(q[-1], 'optional {')
            x = q.var('x')
            q.triple(x, x, x)
        self.assertEqual(q[-1], '}')
        self.assertEqual(q.typeset(), '''\
optional {
  ?x ?x ?x .
}''')

    # -- Modifiers ---------------------------------------------------------

    def test_limit(self):
        q = SPARQL_Builder()
        q.limit(500)
        self.assertEqual(q[-1], 'limit 500')

    def test_offset(self):
        q = SPARQL_Builder()
        q.offset(33)
        self.assertEqual(q[-1], 'offset 33')

    # -- Typesetting -------------------------------------------------------

    def test_select(self):
        q = SPARQL_Builder()
        s, p, o, c = q.vars('s', 'p', 'o', 'c')
        with q.where():
            q.triple(s, p, o)
        self.assertRaises(ValueError, q.select, c)
        self.assertEqual(q.select(), '''\
select * where {
  ?s ?p ?o .
}''')
        self.assertEqual(q.select('*'), '''\
select * where {
  ?s ?p ?o .
}''')
        self.assertEqual(q.select(o, p), '''\
select ?o ?p where {
  ?s ?p ?o .
}''')
        self.assertEqual(q.select((o, c)), '''\
select (?o as ?c) where {
  ?s ?p ?o .
}''')
        self.assertEqual(q.select('(count (*) as ?c)'), '''\
select (count (*) as ?c) where {
  ?s ?p ?o .
}''')


if __name__ == '__main__':
    main()
