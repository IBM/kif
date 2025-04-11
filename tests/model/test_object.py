# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# type: ignore

from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any
from unittest import main, TestCase


class Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import kif_lib.model.object as obj

        global Decoder
        global Encoder
        global JSON_Decoder
        global JSON_Encoder
        global Object
        global ObjectMeta
        global SExpDecoder
        global SExpEncoder
        global ShouldNotGetHere
        global A, A1, A11, B, C

        Decoder = obj.Decoder
        Encoder = obj.Encoder
        JSON_Decoder = obj.JSON_Decoder
        JSON_Encoder = obj.JSON_Encoder
        Object = obj.Object
        ObjectMeta = obj.ObjectMeta
        SExpDecoder = obj.SExpDecoder
        SExpEncoder = obj.SExpEncoder
        ShouldNotGetHere = obj.Object.ShouldNotGetHere

        class A(Object):
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)

        class A1(A):
            def _preprocess_arg(self, arg: Any, i: int) -> Any:
                return arg

        class A11(A1):
            pass

        class B(Object):
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)

            def _preprocess_arg(self, arg: Any, i: int) -> None:
                arg = super()._preprocess_arg(arg, i)
                if i == 1:              # A
                    return A.check(arg, type(self), None, i)
                elif i == 2:            # bool
                    return self._check_arg_bool(arg, type(self), None, i)
                else:
                    return arg

        class C(Object):
            def __init__(self, *args: Any) -> None:
                super().__init__(*args)

            def _preprocess_arg(self, arg: Any, i: int) -> None:
                return arg

        # reset codecs
        for enc in [JSON_Encoder, SExpEncoder]:
            Encoder._register(enc, enc.format, enc.description)
        for dec in [JSON_Decoder, SExpDecoder]:
            Decoder._register(dec, dec.format, dec.description)

    def assert_object(self, obj, args, kwargs={}) -> None:
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(args, (tuple, list))
        self.assertIs(obj.args, obj.get_args())
        self.assertEqual(len(obj), len(args))
        for i, arg in enumerate(args):
            self.assertEqual(obj[i], arg)
        self.assertLessEqual(obj, obj)

    def test__fresh_id(self) -> None:
        x, y, z = A._fresh_id(), A11._fresh_id(), B._fresh_id()
        self.assertIsInstance(x, str)
        self.assertIsInstance(y, str)
        self.assertIsInstance(z, str)
        self.assertNotEqual(x, y)
        self.assertNotEqual(y, z)
        self.assertNotEqual(x, z)

    def test__get_subclasses(self) -> None:
        self.assertEqual(set(A._get_subclasses()), {A, A1, A11})
        self.assertEqual(set(A1._get_subclasses()), {A1, A11})
        self.assertEqual(set(A11._get_subclasses()), {A11})
        self.assertEqual(set(B._get_subclasses()), {B})
        self.assertEqual(set(C._get_subclasses()), {C})

    def test__get_proper_subclasses(self) -> None:
        self.assertEqual(set(A._get_proper_subclasses()), {A1, A11})
        self.assertEqual(set(A1._get_proper_subclasses()), {A11})
        self.assertEqual(set(A11._get_proper_subclasses()), set())
        self.assertEqual(set(B._get_proper_subclasses()), set())
        self.assertEqual(set(C._get_proper_subclasses()), set())

    def test_check(self) -> None:
        self.assertEqual(Object.check(A()), A())
        self.assertEqual(Object.check(B()), B())
        self.assertEqual(A.check(A()), A())
        self.assertRaises(TypeError, A.check, B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(cannot coerce B into A\)$",
            A.check, B())

    def test_check_optional(self) -> None:
        self.assertIsNone(Object.check_optional(None))
        self.assertEqual(Object.check_optional(A()), A())
        self.assertEqual(Object.check_optional(None, A()), A())
        self.assertEqual(Object.check_optional(B()), B())
        self.assertEqual(Object.check_optional(None, B()), B())
        self.assertEqual(A.check_optional(A()), A())
        self.assertRaises(TypeError, A.check_optional, B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' "
            r'\(cannot coerce B into A\)$',
            A.check_optional, B())

    def test__check_error(self) -> None:
        self.assertIsInstance(Object._check_error(int), TypeError)

    def test__init__(self) -> None:
        self.assertRaises(TypeError, A, None)
        self.assert_object(A(), ())
        self.assert_object(A(1, 2, 3), (1, 2, 3))
        self.assert_object(A(A(), B(A(1), True)), (A(), B(A(1), True)))
        self.assert_object(B(A(1)), (A(1),))
        self.assertRaises(TypeError, B, 1)
        self.assertRaises(TypeError, B, A(), 1)

    def test__eq__(self) -> None:
        self.assertEqual(A(), A())
        self.assertNotEqual(A(), A(1))
        self.assertNotEqual(A(), B())

    def test__hash__(self) -> None:
        self.assertNotEqual(hash(A()), hash(B()))  # unlikely

    def test__le__(self) -> None:
        self.assertRaises(TypeError, lambda x, y: x <= y, A(), 0)
        self.assertLessEqual(A(), A())
        self.assertLessEqual(A(), A(1))
        self.assertLessEqual(A(), B())
        self.assertGreaterEqual(B(), A())

    def test__lt__(self) -> None:
        self.assertRaises(TypeError, lambda x, y: x < y, A(), 0)
        self.assertLess(A(), A(1))
        self.assertLess(A(), B())
        self.assertGreater(B(), A())

    def test__ge__(self) -> None:
        self.assertRaises(TypeError, lambda x, y: x >= y, A(), 0)
        self.assertGreaterEqual(A(), A())
        self.assertGreaterEqual(A(1), A())
        self.assertGreaterEqual(B(), A())
        self.assertLessEqual(A(), B())

    def test__gt__(self) -> None:
        self.assertRaises(TypeError, lambda x, y: x > y, A(), 0)
        self.assertGreater(A(1), A(0))
        self.assertGreater(B(), A())
        self.assertLess(A(), B())

    def test_get(self) -> None:
        self.assertRaises(IndexError, A().get, 0)
        a = A1(0, None, 2)
        self.assertEqual(a.get(0), 0)
        self.assertIsNone(a.get(1))
        self.assertEqual(a.get(1, 1), 1)
        self.assertEqual(a.get(2), 2)
        self.assertEqual(a.get(-1), 2)

    def test_digest(self) -> None:
        self.assertEqual(A([1, 2, 3]).digest, A([1, 2, 3]).digest)
        self.assertNotEqual(A([1, 2, 3]).digest, A((1, 2, 3)).digest)
        self.assertNotEqual(A(1).digest, A(2).digest)
        self.assertNotEqual(A().digest, B().digest)

# -- Copying ---------------------------------------------------------------

    def test_copy(self) -> None:
        a = A(1, A(2, 3), A(4))
        self.assertEqual(a.copy(), a)
        self.assertIsNot(a.copy(), a)
        self.assertIs(a.copy()[1], a[1])

    def test_deepcopy(self) -> None:
        a = A(1, A(2, 3), A(4))
        self.assertEqual(a.deepcopy(), a)
        self.assertIsNot(a.deepcopy(), a)
        self.assertIsNot(a.deepcopy()[1], a[1])

    def test_replace(self) -> None:
        c = C(1, C(2, 3), C(4))
        self.assertEqual(c.KEEP(), c.KEEP)
        self.assertEqual(c.replace(), c)
        self.assertEqual(c.replace(2), C(2, *c[1:]))
        self.assertEqual(c.replace(c.KEEP), c)
        self.assertEqual(c.replace(c.KEEP, None), C(1, None, C(4)))
        self.assertEqual(C(1).replace(0, C.KEEP, C.KEEP), C(0))

# -- Conversion ------------------------------------------------------------

    def test_to_ast(self) -> None:
        self.assertEqual(A().to_ast(), {'class': 'A', 'args': ()})
        self.assertEqual(
            A(1, A(2, 3), C(4)).to_ast(),
            {'class': 'A', 'args': (
                1,
                {'class': 'A', 'args': (2, 3)},
                {'class': 'C', 'args': (4,)})})

    def test_from_ast(self) -> None:
        self.assertRaises(TypeError, C.from_ast, {'class': 'A', 'args': ()})
        self.assertEqual(A.from_ast({'class': 'A', 'args': ()}), A())
        self.assertEqual(C.from_ast({'class': 'C', 'args': (4,)}), C(4))
        self.assertEqual(Object.from_ast(
            {'class': 'A', 'args': (
                1,
                {'class': 'A', 'args': (2, 3)},
                {'class': 'C', 'args': (4,)})}), A(1, A(2, 3), C(4)))

# -- Encoding --------------------------------------------------------------

    def assert_dump(self, obj, s, format=None, **kwargs) -> None:
        self.assertEqual(obj.dumps(format, **kwargs), s)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / f'{__name__}.assert_dump'
            with open(path, 'w') as fp:
                obj.dump(fp, format=format, **kwargs)
            with open(path) as fp:
                self.assertEqual(fp.read(), s)

    def assert_dump_repr(self, obj, s, **kwargs) -> None:
        self.assert_dump(obj, s, format='repr', **kwargs)

    def assert_dump_sexp(self, obj, s, **kwargs) -> None:
        self.assert_dump(obj, s, format='sexp', **kwargs)

    def test_dump(self) -> None:
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.dump' \(no such encoder 'x'\)$",
            A().dump, None, 'x')

    def test_dumps(self) -> None:
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #1 \(format\) to "
            r"'Object\.dumps' \(no such encoder 'x'\)$",
            A().dumps, 'x')

    def test_dump_repr(self) -> None:
        self.assert_dump_repr(A(), 'A()')
        self.assert_dump_repr(A(1), 'A(1)')
        self.assert_dump_repr(A([1]), 'A([1])')
        self.assert_dump_repr(A((1,)), 'A((1,))')
        self.assert_dump_repr(A('"x"'), "A('\"x\"')")
        self.assert_dump_repr(A(1, 2, 3), 'A(1, 2, 3)')
        self.assert_dump_repr(A(1, '2', 3), "A(1, '2', 3)")
        self.assert_dump_repr(A(1, ['2', 3]), "A(1, ['2', 3])")
        self.assert_dump_repr(A(1, ['2', [3]]), "A(1, ['2', [3]])")
        self.assert_dump_repr(B(A(), True), 'B(A(), True)')
        self.assert_dump_repr(B(A(1.0), False), 'B(A(1.0), False)')
        self.assert_dump_repr(B(A(B(A()))), 'B(A(B(A())))')
        # indent
        self.assert_dump_repr(A(1), 'A(\n  1\n)', indent=2)
        self.assert_dump_repr(B(A(B(A(), False))), '''\
B(
    A(
        B(
            A(),
            False
        )
    )
)''', indent=4)

    def test_to_repr(self) -> None:
        self.assertEqual(A().to_repr(), 'A()')
        self.assertEqual(A().to_repr(indent=2), 'A()')
        self.assertEqual(A(B()).to_repr(indent=2), 'A(\n  B()\n)')

    def test_dump_sexp(self) -> None:
        self.assertRaises(Encoder.Error, A(set()).dumps, format='sexp')
        self.assert_dump_sexp(A(), 'A')
        self.assert_dump_sexp(A(1), '(A 1)')
        self.assert_dump_sexp(A(1, 2, 3), '(A 1 2 3)')
        self.assert_dump_sexp(A(1, '2', 3), '(A 1 "2" 3)')
        self.assert_dump_sexp(A(1, ['2', 3]), '(A 1 ["2" 3])')
        self.assert_dump_sexp(A(1, ['2', [3]]), '(A 1 ["2" [3]])')
        self.assert_dump_sexp(B(A(), True), '(B A true)')
        self.assert_dump_sexp(B(A(1.0), False), '(B (A 1.0) false)')
        self.assert_dump_sexp(B(A(B(A()))), '(B (A (B A)))')
        # indent
        self.assert_dump_sexp(A(1), '(A\n  1\n)', indent=2)
        self.assert_dump_sexp(B(A(B(A()))), '''\
(B
    (A
        (B
            A
        )
    )
)''', indent=4)

    def test_to_sexp(self) -> None:
        self.assertEqual(A().to_sexp(), 'A')
        self.assertEqual(A().to_sexp(indent=2), 'A')
        self.assertEqual(A(B()).to_sexp(indent=2), '(A\n  B\n)')

    def test_dump_json(self) -> None:
        def js(A, *args):
            args = ", ".join(args)
            return f'{{"class": "{A}", "args": [{args}]}}'
        self.assertRaises(Encoder.Error, A(set()).dumps, format='json')
        self.assert_dump(A(), js('A'), 'json')
        self.assert_dump(A(1), js('A', '1'), 'json')
        self.assert_dump(A(1, 2, 3), js('A', '1', '2', '3'), 'json')
        self.assert_dump(A(1, '2', 3), js('A', '1', '"2"', '3'), 'json')
        self.assert_dump(A(1, ['2', 3]), js('A', '1', '["2", 3]'), 'json')
        self.assert_dump(B(A(), True), js('B', js('A'), 'true'), 'json')
        self.assert_dump(
            B(A(1.0), False), js('B', js('A', '1.0'), 'false'), 'json')
        self.assert_dump(
            B(A(B(A()))), js('B', js('A', js('B', js('A')))), 'json')
        # indent
        self.assert_dump(
            B(A(B(A()))), json.dumps(json.loads(
                js('B', js('A', js('B', js('A'))))), indent=4),
            format='json', indent=4)

    def test_to_json(self) -> None:
        self.assertEqual(A().to_json(), '{"class": "A", "args": []}')
        self.assertEqual(A(B()).to_json(indent=2), '''\
{
  "class": "A",
  "args": [
    {
      "class": "B",
      "args": []
    }
  ]
}''')

# -- Decoding --------------------------------------------------------------

    def assert_load(self, obj, s, format=None, **kwargs) -> None:
        self.assertEqual(obj.loads(s, format, **kwargs), obj)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / f'{__name__}.assert_load'
            with open(path, 'w') as fp:
                obj.dump(fp, format=format, **kwargs)
            with open(path) as fp:
                self.assertEqual(obj.load(fp, format), obj)

    def assert_load_sexp(self, obj, s, **kwargs) -> None:
        self.assert_load(obj, s, format='sexp', **kwargs)

    def test_load(self) -> None:
        class FP():
            def read(self):
                return ''
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.loads' \(no such decoder 'x'\)$",
            A.load, FP(), 'x')

    def test_loads(self) -> None:
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.loads' \(no such decoder 'x'\)$",
            A.loads, '', 'x')

    def test_loads_sexp(self) -> None:
        self.assertRaisesRegex(
            Decoder.Error, 'syntax error', A.from_sexp, '{}')
        self.assertRaisesRegex(
            Decoder.Error, r"^no such object class 'Z'$", A.from_sexp, 'Z')
        self.assert_load_sexp(A(), 'A')
        self.assert_load_sexp(A(), '(A)')
        self.assertRaisesRegex(
            Decoder.Error, 'syntax error', A.from_sexp, '((A))')
        self.assert_load_sexp(A(1), '(A 1)')
        self.assert_load_sexp(A(1, 2, 3), '(A 1 2 3)')
        self.assert_load_sexp(A(1, '2', 3), '(A 1 "2" 3)')
        self.assert_load_sexp(A(1, ['2', 3]), '(A 1 ["2" 3])')
        self.assert_load_sexp(A(1, ['2', [3]]), '(A 1 ["2" [3]])')
        self.assert_load_sexp(B(A(), True), '(B A true)')
        self.assert_load_sexp(B(A(1.0), False), '(B (A 1.0) false)')
        self.assert_load_sexp(B(A(B(A()))), '(B (A (B A)))')
        # indent
        self.assert_load_sexp(A(1), '(A\n  1\n)')
        self.assert_load_sexp(B(A(B(A()))), '''\
(B
    (A # this is a comment
        (B
            A
        )
    )
)''')

    def test_from_repr(self) -> None:
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(cannot coerce A into B\)$",
            B.from_repr, ('A(B())'))
        self.assertEqual(A(), A.from_repr('A()'))
        self.assertEqual(A(), A.from_repr('  A()  #'))
        self.assertEqual(A(B()), A.from_repr('A(\n  B(\n)\n)'))
        self.assertEqual(A(B(), C(1, A(2))), A.from_repr('A(B(),C(1,A(2)))'))

    def test_from_sexp(self) -> None:
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(cannot coerce A into B\)$",
            B.from_sexp, '(A\n  B\n)')
        self.assertEqual(A(), A.from_sexp('A'))
        self.assertEqual(A(), A.from_sexp('  A  #'))
        self.assertEqual(A(B()), A.from_sexp('(A\n  B\n)'))
        self.assertEqual(A(B(), C(1, A(2))), A.from_sexp('(A(B)(C 1 (A 2)))'))

    def test_load_json(self) -> None:
        def js(A, *args):
            args = ", ".join(args)
            return f'{{"class": "{A}", "args": [{args}]}}'
        self.assertRaisesRegex(
            Decoder.Error, r"^missing attribute 'class'$", A.loads, '{}',
            format='json')
        self.assertRaisesRegex(
            Decoder.Error, r"^no such object class 'Z'$", A.loads,
            js('Z'), format='json')
        self.assert_load(A(), js('A'), 'json')
        self.assert_load(A(1), js('A', '1'), 'json')
        self.assert_load(A(1), js('A', '1'), 'json')
        self.assert_load(A(1, 2, 3), js('A', '1', '2', '3'), 'json')
        self.assert_load(A(1, '2', 3), js('A', '1', '"2"', '3'), 'json')
        self.assert_load(A(1, ['2', 3]), js('A', '1', '["2", 3]'), 'json')
        self.assert_load(B(A(), True), js('B', js('A'), 'true'), 'json')
        self.assert_load(
            B(A(1.0), False), js('B', js('A', '1.0'), 'false'), 'json')
        self.assert_load(
            B(A(B(A()))), js('B', js('A', js('B', js('A')))), 'json')
        self.assert_load(
            B(A(B(A()))), js('B', js('A', js('B', js('A')))),
            format='json')

    def test_from_json(self) -> None:
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(cannot coerce A into B\)$",
            B.from_json, '{"class": "A", "args": []}')
        self.assertEqual(A(), A.from_json('{"class": "A", "args": []}'))
        self.assertEqual(A(B()), A.from_json('''\
{
  "class": "A",
  "args": [
    {
      "class": "B",
      "args": []
    }
  ]
}'''))

# -- Argument checking -----------------------------------------------------

    def test__check_arg_not_none(self) -> None:
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected value, got None\)$',
            Object._check_arg_not_none, None)
        self.assertEqual(Object._check_arg_not_none(0), 0)

    def test__check_arg_callable(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected callable, got int\)$',
            Object._check_arg_callable, 0)
        # good argument
        self.assertEqual(
            Object._check_arg_callable(Object.get_args),
            Object.get_args)

    def test__check_optional_arg_callable(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected callable, got int\)$',
            Object._check_optional_arg_callable, 0)
        # no argument
        self.assertIsNone(Object._check_optional_arg_callable(None))
        self.assertEqual(
            Object._check_optional_arg_callable(None, Object.get_args),
            Object.get_args)
        # good argument
        self.assertEqual(
            Object._check_optional_arg_callable(Object.get_args),
            Object.get_args)

    def test__check_arg_isinstance(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected str, got int\)$',
            Object._check_arg_isinstance, 0, str)
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected int or str, got float\)$',
            Object._check_arg_isinstance, 0.5, (str, int))
        # good argument
        self.assertEqual(Object._check_arg_isinstance(0, int), 0)
        self.assertEqual(Object._check_arg_isinstance('0', (int, str)), '0')

    def test__check_optional_arg_isinstance(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected str, got int\)$',
            Object._check_optional_arg_isinstance, 0, str)
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected int or str, got float\)$',
            Object._check_optional_arg_isinstance, 0.5, (str, int))
        # no argument
        self.assertIsNone(Object._check_optional_arg_isinstance(None, int))
        self.assertEqual(
            Object._check_optional_arg_isinstance(None, (int, str), 'abc'),
            'abc')
        # good argument
        self.assertEqual(
            Object._check_optional_arg_isinstance('abc', (int, str)),
            'abc')

    def test__check_arg_issubclass(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected type, got int\)$',
            Object._check_arg_issubclass, 0, int)
        self.assertRaisesRegex(
            ValueError,
            r'^bad argument \(expected subclass of str, got int\)$',
            Object._check_arg_issubclass, int, str)
        self.assertRaisesRegex(
            ValueError, r'^bad argument '
            r'\(expected subclass of int or str, got float\)$',
            Object._check_arg_issubclass, float, (str, int))
        # good argument
        self.assertEqual(Object._check_arg_issubclass(int, object), int)
        self.assertEqual(Object._check_arg_issubclass(int, (object, str)), int)

    def test__check_optional_arg_issubclass(self) -> None:
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected type, got int\)$',
            Object._check_optional_arg_issubclass, 0, int)
        self.assertRaisesRegex(
            ValueError,
            r'^bad argument \(expected subclass of str, got int\)$',
            Object._check_optional_arg_issubclass, int, str)
        self.assertRaisesRegex(
            ValueError, r'^bad argument '
            r'\(expected subclass of int or str, got float\)$',
            Object._check_optional_arg_issubclass, float, (str, int))
        # no argument
        self.assertIsNone(Object._check_optional_arg_issubclass(None, int))
        self.assertEqual(
            Object._check_optional_arg_issubclass(None, (int, str), 'abc'),
            'abc')
        # good argument
        self.assertEqual(
            Object._check_optional_arg_issubclass(int, (object, str), 'abc'),
            int)

# -- Utility ---------------------------------------------------------------

    def test_should_not_get_here(self) -> None:
        def f(msg=None):
            raise Object._should_not_get_here(msg)
        self.assertRaisesRegex(ShouldNotGetHere, r'^$', f)
        self.assertRaisesRegex(
            ShouldNotGetHere, r'^details$', f, 'details')


if __name__ == '__main__':
    main()
