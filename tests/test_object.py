# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import json
import pathlib
import tempfile
from unittest import main, TestCase

import kif_lib
from kif_lib.model.object import (
    Decoder,
    DecoderError,
    Encoder,
    EncoderError,
    JSON_Decoder,
    JSON_Encoder,
    MustBeImplementedInSubclass,
    Object,
    SExpDecoder,
    SExpEncoder,
    ShouldNotGetHere,
)


def setUpModule():
    global A, B, C

    class A(Object):
        def __init__(self, *args):
            super().__init__(*args)

    class B(Object):
        def __init__(self, *args):
            super().__init__(*args)

        def _preprocess_arg(self, arg, i):
            arg = super()._preprocess_arg(arg, i)
            if i == 1:              # A
                return self._preprocess_arg_a(arg, i)
            elif i == 2:            # bool
                return self._preprocess_arg_bool(arg, i)
            else:
                return arg

    class C(Object):
        def __init__(self, *args):
            super().__init__(*args)

        def _preprocess_arg(self, arg, i):
            return arg


def tearDownModule():
    from importlib import reload
    reload(kif_lib)


class TestObject(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reset_codecs()

    def assert_object(self, obj, args, kwargs={}):
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(args, (tuple, list))
        self.assertIs(obj.args, obj.get_args())
        self.assertEqual(len(obj), len(args))
        for i, arg in enumerate(args):
            self.assertEqual(obj[i], arg)
        self.assertLessEqual(obj, obj)

    def test__eq__(self):
        self.assertEqual(A(), A())
        self.assertNotEqual(A(), A(1))
        self.assertNotEqual(A(), B())

    def test_test(self):
        self.assertFalse(Object.test(-1))
        self.assertTrue(Object.test(A()))
        self.assertTrue(Object.test(B(A())))
        self.assertTrue(A.test(A()))
        self.assertFalse(A.test(B(A())))
        self.assertTrue(A().test_object())
        self.assertTrue(A().test_a())
        self.assertFalse(A().test_b())
        self.assertFalse(B().test_a())

    def test_is(self):
        self.assertTrue(A().is_object())
        self.assertTrue(A().is_a())
        self.assertFalse(A().is_b())
        self.assertFalse(B().is_a())

    def test_check(self):
        self.assertEqual(Object.check(A()), A())
        self.assertEqual(Object.check(B()), B())
        self.assertEqual(A.check(A()), A())
        self.assertRaises(TypeError, A.check, B())
        self.assertEqual(A().check_object(), A())
        self.assertEqual(A().check_a(), A())
        self.assertEqual(B().check_b(), B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(expected A, got B\)$",
            A.check, B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check' \(expected A, got B\)$",
            B().check_a)
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'f' \(expected A, got B\)$",
            B().check_a, 'f')

    def test_check_optional(self):
        self.assertEqual(Object.check_optional(A()), A())
        self.assertEqual(Object.check_optional(None, A()), A())
        self.assertEqual(Object.check_optional(B()), B())
        self.assertEqual(Object.check_optional(None, B()), B())
        self.assertEqual(A.check_optional(A()), A())
        self.assertRaises(TypeError, A.check_optional, B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.check_optional' \(expected A, got B\)$",
            A.check_optional, B())

    def test_unpack(self):
        self.assertEqual(Object.unpack(A()), ())
        self.assertEqual(Object.unpack(A(1, 2, 3)), (1, 2, 3))
        self.assertEqual(A.unpack(A(1, B(), 3)), (1, B(), 3))
        self.assertRaises(TypeError, A.unpack, B())
        # unpack_*
        self.assertEqual(A().unpack_a(), ())
        self.assertEqual(A(2).unpack_object(), (2,))
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.unpack' \(expected A, got B\)$",
            A.unpack, B())
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.unpack' \(expected A, got B\)$",
            B().unpack_a)
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'f' \(expected A, got B\)$",
            B().unpack_a, 'f')

    def test__init__(self):
        self.assertRaises(TypeError, A, None)
        self.assert_object(A(), ())
        self.assert_object(A(1, 2, 3), (1, 2, 3))
        self.assert_object(A(A(), B(A(1), True)), (A(), B(A(1), True)))
        self.assert_object(B(A(1)), (A(1),))
        self.assertRaises(TypeError, B, 1)
        self.assertRaises(TypeError, B, A(), 1)

    def test__hash__(self):
        self.assertNotEqual(hash(A()), hash(B()))  # unlikely

    def test__lt__(self):
        self.assertRaisesRegex(
            TypeError, r"^bad argument to 'Object.__lt__'", A().__lt__, 0)
        self.assertLess(A(), A(1))
        self.assertGreater(B(), A())

    def test_digest(self):
        self.assertEqual(A([1, 2, 3]).digest, A((1, 2, 3)).digest)
        self.assertNotEqual(A(1).digest, A(2).digest)
        self.assertNotEqual(A().digest, B().digest)

    # -- Copying -----------------------------------------------------------

    def test_copy(self):
        a = A(1, A(2, 3), A(4))
        self.assertEqual(a.copy(), a)
        self.assertIsNot(a.copy(), a)
        self.assertIs(a.copy()[1], a[1])

    def test_deepcopy(self):
        a = A(1, A(2, 3), A(4))
        self.assertEqual(a.deepcopy(), a)
        self.assertIsNot(a.deepcopy(), a)
        self.assertIsNot(a.deepcopy()[1], a[1])

    def test_replace(self):
        c = C(1, C(2, 3), C(4))
        self.assertEqual(c.replace(), c)
        self.assertEqual(c.replace(2), C(2, *c[1:]))
        self.assertEqual(c.replace(None), c)
        self.assertEqual(c.replace(None, c.Nil), C(1, None, C(4)))

    # -- Encoding ----------------------------------------------------------

    @classmethod
    def reset_codecs(cls):
        for enc in [JSON_Encoder, SExpEncoder]:
            Encoder._register(enc, enc.format, enc.description)
        for dec in [JSON_Decoder, SExpDecoder]:
            Decoder._register(dec, dec.format, dec.description)

    def assert_dump(self, obj, s, format=None, **kwargs):
        self.assertEqual(obj.dumps(format, **kwargs), s)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / f'{__name__}.assert_dump'
            with open(path, 'w') as fp:
                obj.dump(fp, format=format, **kwargs)
            with open(path, 'r') as fp:
                self.assertEqual(fp.read(), s)

    def test_dump(self):
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.dump' \(no such encoder 'x'\)$",
            A().dump, None, 'x')

    def test_dumps(self):
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #1 \(format\) to "
            r"'Object\.dumps' \(no such encoder 'x'\)$",
            A().dumps, 'x')

    def test_dump_sexp(self):
        self.assertRaises(EncoderError, A(set()).dumps)
        self.assert_dump(A(), 'A')
        self.assert_dump(A(1), '(A 1)', 'sexp')
        self.assert_dump(A(1, 2, 3), '(A 1 2 3)')
        self.assert_dump(A(1, '2', 3), '(A 1 "2" 3)', 'sexp')
        self.assert_dump(A(1, ['2', 3]), '(A 1 ["2" 3])')
        self.assert_dump(A(1, ['2', (3,)]), '(A 1 ["2" [3]])')
        self.assert_dump(B(A(), True), '(B A true)')
        self.assert_dump(B(A(1.0), False), '(B (A 1.0) false)')
        self.assert_dump(B(A(B(A()))), '(B (A (B A)))')
        # indent
        self.assert_dump(A(1), '(A\n  1\n)', indent=2)
        self.assert_dump(B(A(B(A()))), '''\
(B
    (A
        (B
            A
        )
    )
)''', indent=4)

    def test_to_sexp(self):
        self.assertEqual(A().to_sexp(), 'A')
        self.assertEqual(A().to_sexp(indent=2), 'A')
        self.assertEqual(A(B()).to_sexp(indent=2), '(A\n  B\n)')

    def test_dump_json(self):
        def js(A, *args):
            args = ", ".join(args)
            return f'{{"class": "{A}", "args": [{args}]}}'
        self.assertRaises(EncoderError, A(set()).dumps, format='json')
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

    def test_to_json(self):
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

    # -- Decoding ----------------------------------------------------------

    def assert_load(self, obj, s, format=None, **kwargs):
        self.assertEqual(obj.loads(s, format, **kwargs), obj)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / f'{__name__}.assert_load'
            with open(path, 'w') as fp:
                obj.dump(fp, format=format, **kwargs)
            with open(path, 'r') as fp:
                self.assertEqual(obj.load(fp, format), obj)

    def test_load(self):
        class FP():
            def read(self):
                return ''
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.loads' \(no such decoder 'x'\)$",
            A.load, FP(), 'x')

    def test_loads(self):
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #2 \(format\) to "
            r"'Object\.loads' \(no such decoder 'x'\)$",
            A.loads, '', 'x')

    def test_loads_sexp(self):
        self.assertRaisesRegex(
            DecoderError, 'syntax error', A.loads, '{}')
        self.assertRaisesRegex(
            DecoderError, r"^no such object class 'Z'$", A.loads, 'Z')
        self.assert_load(A(), 'A')
        self.assert_load(A(), '(A)')
        self.assertRaisesRegex(
            DecoderError, 'syntax error', A.loads, '((A))')
        self.assert_load(A(1), '(A 1)', 'sexp')
        self.assert_load(A(1, 2, 3), '(A 1 2 3)')
        self.assert_load(A(1, '2', 3), '(A 1 "2" 3)', 'sexp')
        self.assert_load(A(1, ['2', 3]), '(A 1 ["2" 3])')
        self.assert_load(A(1, ['2', [3]]), '(A 1 ["2" [3]])')
        self.assert_load(B(A(), True), '(B A true)')
        self.assert_load(B(A(1.0), False), '(B (A 1.0) false)')
        self.assert_load(B(A(B(A()))), '(B (A (B A)))')
        # indent
        self.assert_load(A(1), '(A\n  1\n)')
        self.assert_load(B(A(B(A()))), '''\
(B
    (A # this is a comment
        (B
            A
        )
    )
)''')

    def test_from_sexp(self):
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.load' \(expected B, got A\)$",
            B.from_sexp, '(A\n  B\n)')
        self.assertEqual(A(), A.from_sexp('A'))
        self.assertEqual(A(), A.from_sexp('  A  #'))
        self.assertEqual(A(B()), A.from_sexp('(A\n  B\n)'))

    def test_load_json(self):
        def js(A, *args):
            args = ", ".join(args)
            return f'{{"class": "{A}", "args": [{args}]}}'
        self.assertRaisesRegex(
            DecoderError, r"^missing field 'class'$", A.loads, '{}',
            format='json')
        self.assertRaisesRegex(
            DecoderError, r"^no such object class 'Z'$", A.loads,
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

    def test_from_json(self):
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument to 'Object.load' \(expected B, got A\)$",
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

    # -- _check_arg --------------------------------------------------------

    def test__check_arg(self):
        self.assertRaisesRegex(
            ValueError, r'^bad argument$',
            Object._check_arg, 'x', False)
        self.assertRaisesRegex(
            ValueError, r'^bad argument$',
            Object._check_arg, 'x', lambda x: False)
        self.assertRaisesRegex(
            ValueError, r'^bad argument \(details\)$',
            Object._check_arg, 'x', False, 'details')
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f'$",
            Object._check_arg, 'x', False, None, 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\)$",
            Object._check_arg, 'x', False, None, None, 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument #8$",
            Object._check_arg, 'x', False, None, None, None, 8)
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f' \(details\)$",
            Object._check_arg, 'x', False, 'details', 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f'$",
            Object._check_arg, 'x', False, None, 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) to 'f' \(details\)$",
            Object._check_arg, 'x', False, 'details', 'f', 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) to 'f'$",
            Object._check_arg, 'x', False, None, 'f', 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) \(details\)$",
            Object._check_arg, 'x', False, 'details', None, 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument #8 \(v\) to 'f' \(details\)$",
            Object._check_arg, 'x', False, 'details', 'f', 'v', 8)
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #8 \(v\) to 'Object.get_args' \(details\)$",
            Object._check_arg, 'x', False, 'details',
            Object.get_args, 'v', 8)
        self.assertRaises(
            AssertionError, Object._check_arg,
            'x', False, 'details', 'f', 'v', -8)
        # A, B, C
        self.assertEqual(A._check_arg_a(A()), A())
        self.assertRaises(TypeError, A()._check_arg_a, B())

    def test__check_optional_arg(self):
        self.assertRaisesRegex(
            ValueError, r'^bad argument \(details\)$',
            Object._check_optional_arg, 'x', None, False, 'details')
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f'$",
            Object._check_optional_arg, 'x', None, False, None, 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\)$",
            Object._check_optional_arg, 'x', None, False, None, None, 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument #8$",
            Object._check_optional_arg, 'x', None, False, None, None, None, 8)
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f' \(details\)$",
            Object._check_optional_arg, 'x', None, False, 'details', 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument to 'f'$",
            Object._check_optional_arg, 'x', None, False, None, 'f')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) to 'f' \(details\)$",
            Object._check_optional_arg, 'x', None, False, 'details', 'f', 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) to 'f'$",
            Object._check_optional_arg, 'x', None, False, None, 'f', 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument \(v\) \(details\)$",
            Object._check_optional_arg,
            'x', None, False, 'details', None, 'v')
        self.assertRaisesRegex(
            ValueError, r"^bad argument #8 \(v\) to 'f' \(details\)$",
            Object._check_optional_arg,
            'x', None, False, 'details', 'f', 'v', 8)
        self.assertRaisesRegex(
            ValueError,
            r"^bad argument #8 \(v\) to 'Object.get_args' \(details\)$",
            Object._check_optional_arg, 'x', None, False, 'details',
            Object.get_args, 'v', 8)
        self.assertRaises(
            AssertionError, Object._check_optional_arg,
            'x', None, False, 'details', 'f', 'v', -8)
        self.assertEqual(Object._check_optional_arg(1, None, True), 1)
        self.assertEqual(Object._check_optional_arg(None, 1, True), 1)
        self.assertEqual(Object._check_optional_arg(None, 1, False), 1)
        self.assertEqual(A._check_optional_arg_a(A(), None), A())
        self.assertIsNone(A._check_optional_arg_a(None), None)
        self.assertEqual(A._check_optional_arg_a(None, A()), A())
        self.assertRaises(TypeError, A()._check_optional_arg_a, B())

    def test__check_arg_not_none(self):
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected value, got None\)$',
            Object._check_arg_not_none, None)
        self.assertEqual(Object._check_arg_not_none(0), 0)

    # -- callable --

    def test__check_arg_callable(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError, r'^bad argument \(expected callable, got int\)$',
            Object._check_arg_callable, 0)
        # good argument
        self.assertEqual(
            Object._check_arg_callable(Object.get_args),
            Object.get_args)

    def test__check_optional_arg_callable(self):
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

    # -- isinstance --

    def test__check_arg_isinstance(self):
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

    def test__check_optional_arg_isinstance(self):
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

    # -- _preprocess_arg ---------------------------------------------------

    def test__preprocess_arg(self):
        self.assertEqual(A._preprocess_arg, Object._preprocess_arg)
        self.assertNotEqual(A._preprocess_arg, B._preprocess_arg)
        self.assertEqual(A._preprocess_arg_a(A(), 1), A())
        self.assertRaises(TypeError, A()._preprocess_arg_a, 'abc', 1)

        class C(Object):
            def __init__(self):
                return super().__init__()

            @classmethod
            def _preprocess_arg_c(cls, arg, i, function=None):
                return 0
        self.assertTrue(hasattr(A, '_preprocess_arg_c'))
        self.assertEqual(A._preprocess_arg_c(1, 1), 0)

        # bool
        class C1(Object):
            def __init__(self, *args):
                return super().__init__(*args)

            def _preprocess_arg(self, arg, i):
                return self._preprocess_arg_bool(arg, i)
        self.assert_object(C1(True), (True,))
        self.assertRaises(TypeError, C1, 1)

        # int
        class C2(Object):
            def __init__(self, *args):
                return super().__init__(*args)

            def _preprocess_arg(self, arg, i):
                return self._preprocess_arg_int(arg, i)
        self.assert_object(C2(0), (0,))
        self.assertRaises(TypeError, C2, 'abc')

        # float
        class C3(Object):
            def __init__(self, *args):
                return super().__init__(*args)

            def _preprocess_arg(self, arg, i):
                return self._preprocess_arg_float(arg, i)
        self.assert_object(C3(0.), (0.,))
        self.assertRaises(TypeError, C3, 'abc')

        # number
        class C4(Object):
            def __init__(self, *args):
                return super().__init__(*args)

            def _preprocess_arg(self, arg, i):
                return self._preprocess_arg_number(arg, i)
        self.assert_object(C4(0.), (0.,))
        self.assert_object(C4(0), (0,))
        self.assertRaises(TypeError, C4, 'abc')

        # str
        class C5(Object):
            def __init__(self, *args):
                return super().__init__(*args)

            def _preprocess_arg(self, arg, i):
                return self._preprocess_arg_str(arg, i)
        self.assert_object(C5(''), ('',))
        self.assertRaises(TypeError, C5, 0)

    def test__preprocess_optional_arg(self):
        self.assertEqual(A._preprocess_optional_arg_a(None, 1, A()), A())
        self.assertRaises(
            TypeError, A()._preprocess_optional_arg_a, 'abc', 1)
        self.assertEqual(A._preprocess_optional_arg_a(None, 1, A(1)), A(1))

        class C(Object):
            def __init__(self):
                return super().__init__()

            @classmethod
            def _preprocess_arg_c(cls, arg, i, function=None):
                return 0
        self.assertEqual(A._preprocess_arg_c(1, 1), 0)
        self.assertEqual(A._preprocess_optional_arg_c(None, 1, 8), 8)

    # -- bool --

    def test__preprocess_arg_bool(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected bool, got int\)$",
            Object._preprocess_arg_bool, 0, 8)
        # good argument
        self.assertEqual(Object._preprocess_arg_bool(True, 8), True)

    def test__preprocess_optional_arg_bool(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected bool, got int\)$",
            Object._preprocess_optional_arg_bool, 0, 8)
        # no argument
        self.assertEqual(
            Object._preprocess_optional_arg_bool(None, 8, False), False)
        # good argument
        self.assertEqual(
            Object._preprocess_optional_arg_bool(True, 8), True)
        self.assertEqual(
            Object._preprocess_optional_arg_bool(True, 8, False), True)

    # -- int --

    def test__preprocess_arg_int(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected int, got str\)$",
            Object._preprocess_arg_int, 'abc', 8)
        # good argument
        self.assertEqual(Object._preprocess_arg_int(-1, 8), -1)

    def test__preprocess_optional_arg_int(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected int, got str\)$",
            Object._preprocess_optional_arg_int, 'abc', 8)
        # no argument
        self.assertEqual(
            Object._preprocess_optional_arg_int(None, 8, -1), -1)
        # good argument
        self.assertEqual(Object._preprocess_optional_arg_int(-1, 8), -1)
        self.assertEqual(Object._preprocess_optional_arg_int(-1, 8, 1), -1)

    # -- float --

    def test__preprocess_arg_float(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected float, got int\)$",
            Object._preprocess_arg_float, 1, 8)
        # good argument
        self.assertEqual(Object._preprocess_arg_float(-1., 8), -1.)

    def test__preprocess_optional_arg_float(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected float, got int\)$",
            Object._preprocess_optional_arg_float, 1, 8)
        # no argument
        self.assertEqual(
            Object._preprocess_optional_arg_float(None, 8, -1.), -1.)
        # good argument
        self.assertEqual(
            Object._preprocess_optional_arg_float(-1., 8), -1.)
        self.assertEqual(
            Object._preprocess_optional_arg_float(-1., 8, 1.), -1.)

    # -- number --

    def test__preprocess_arg_number(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' "
            r"\(expected float or int, got str\)$",
            Object._preprocess_arg_number, 'abc', 8)
        # good argument
        self.assertEqual(Object._preprocess_arg_number(-1., 8), -1.)
        self.assertEqual(Object._preprocess_arg_number(-1, 8), -1)

    def test__preprocess_optional_arg_number(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' "
            r"\(expected float or int, got str\)$",
            Object._preprocess_optional_arg_number, 'abc', 8)
        # no argument
        self.assertEqual(
            Object._preprocess_optional_arg_number(None, 8, -1.), -1.)
        self.assertEqual(
            Object._preprocess_optional_arg_number(None, 8, -1), -1)
        # good argument
        self.assertEqual(
            Object._preprocess_optional_arg_number(-1., 8), -1.)
        self.assertEqual(
            Object._preprocess_optional_arg_number(-1, 8, 1.), -1)

    # -- str --

    def test__preprocess_arg_str(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected str, got int\)$",
            Object._preprocess_arg_str, 99, 8)
        # good argument
        self.assertEqual(Object._preprocess_arg_str('abc', 8), 'abc')

    def test__preprocess_optional_arg_str(self):
        # bad argument
        self.assertRaisesRegex(
            TypeError,
            r"^bad argument #8 to 'Object' \(expected str, got float\)$",
            Object._preprocess_optional_arg_str, .99, 8)
        # no argument
        self.assertEqual(
            Object._preprocess_optional_arg_str(None, 8, 'abc'), 'abc')
        # good argument
        self.assertEqual(
            Object._preprocess_optional_arg_str('abc', 8), 'abc')
        self.assertEqual(
            Object._preprocess_optional_arg_str('abc', 8, 'x'), 'abc')

    # -- Utility -----------------------------------------------------------

    def test_camel2snake(self):
        self.assertEqual(
            Object._camel2snake('a'), 'a')
        self.assertEqual(
            Object._camel2snake('aB'), 'a_b')
        self.assertEqual(
            Object._camel2snake('a_B'), 'a_b')
        self.assertEqual(
            Object._camel2snake('AaB'), 'aa_b')
        self.assertEqual(
            Object._camel2snake('Aa_B'), 'aa_b')
        self.assertEqual(
            Object._camel2snake('AAB'), 'aab')
        self.assertEqual(
            Object._camel2snake('AA_B'), 'aa_b')
        self.assertEqual(
            Object._camel2snake('CamelToSnake'), 'camel_to_snake')

    def test_must_be_implemented_in_subclass(self):
        def f(msg=None):
            raise Object._must_be_implemented_in_subclass(msg)
        self.assertRaisesRegex(MustBeImplementedInSubclass, r'^$', f)
        self.assertRaisesRegex(
            MustBeImplementedInSubclass, r'^details$', f, 'details')

    def test_should_not_get_here(self):
        def f(msg=None):
            raise Object._should_not_get_here(msg)
        self.assertRaisesRegex(ShouldNotGetHere, r'^$', f)
        self.assertRaisesRegex(
            ShouldNotGetHere, r'^details$', f, 'details')


if __name__ == '__main__':
    main()
