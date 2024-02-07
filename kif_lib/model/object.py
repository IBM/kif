# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# $Id$
#
# Syntactical objects.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

import abc
import collections.abc
import copy
import functools
import itertools
import json
import re
from typing import (
    Any,
    Callable,
    cast,
    Generator,
    IO,
    NoReturn,
    Optional,
    TypeVar,
    Union,
)

import lark  # for S-expression parsing

__version__ = '0.1'

__all__ = [
    'Codec',
    'CodecError',
    'Decoder',
    'DecoderError',
    'Encoder',
    'EncoderError',
    'Error',
    'MustBeImplementedInSubclass',
    'Object',
    'ShouldNotGetHere',
]


class Error(Exception):
    """Base class for errors."""


class MustBeImplementedInSubclass(Error):
    """Must be implemented in subclass."""


class ShouldNotGetHere(Error):
    """Should not get here."""


class NilType:
    """Type for absence of value distinct from ``NoneType``."""

    Nil: Optional['NilType'] = None

    def __new__(cls):
        if cls.Nil is None:
            cls.Nil = super().__new__(cls)
        return cls.Nil


#: Absence of value distinct from ``None``.
Nil = NilType()

T = TypeVar('T')
TArgs = tuple[Any, ...]
TFun = Callable[..., Any]
TNil = NilType
TNum = Union[float, int]
TObj = type['Object']


# -- ObjectMeta ------------------------------------------------------------

class ObjectMeta(abc.ABCMeta):
    """Meta-class for syntactical objects."""

    _object_class: Optional[TObj] = None
    _object_subclasses: dict[str, TObj] = dict()

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        mcls._init(cls, name, bases, namespace, **kwargs)
        return cls

    @classmethod
    def _init(mcls, cls, name, bases, namespace, **kwargs):
        mcls._object_subclasses[name] = cls
        top = mcls._object_class or cls
        setattr(top, name, cls)
        cls._snake_case_name = top._camel2snake(name)
        mcls._init_test_(top, cls)
        mcls._init_check_(top, cls)
        mcls._init_unpack_(top, cls)
        mcls._init_preprocess_arg_(top, cls)
        return cls

    @classmethod
    def _init_test_(mcls, top: TObj, cls: TObj):
        def f_test(arg: Any) -> bool:
            return cls.test(arg)
        f_test.__doc__ = f"""\
        Tests whether object is :class:`{cls.__qualname__}`.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        setattr(top, 'is_' + cls._snake_case_name, f_test)
        setattr(top, 'test_' + cls._snake_case_name, f_test)

    @classmethod
    def _init_check_(mcls, top: TObj, cls: TObj):
        def mk_check_(s: str):
            def check_(
                    arg: 'Object',
                    function: Optional[Union[TFun, str]] = None,
                    name: Optional[str] = None,
                    position: Optional[int] = None
            ) -> Union['Object', NoReturn]:
                return cls.check(arg, function, name, position)
            return check_
        s = 'check_' + cls._snake_case_name
        f_check = mk_check_(s)
        f_check.__doc__ = f"""\
        Checks whether object is :class:`{cls.__qualname__}`.

        Parameters:
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           :class:`{cls.__qualname__}`.

        Raises:
           TypeError: Object is not :class:`{cls.__qualname__}`.
        """
        setattr(top, s, f_check)

    @classmethod
    def _init_unpack_(mcls, top: TObj, cls: TObj):
        def f_unpack(
                arg: 'Object',
                function: Optional[Union[TFun, str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Union[TArgs, NoReturn]:
            return cls.unpack(
                arg, function=function, name=name, position=position)
        f_unpack.__doc__ = f"""\
        Unpacks arguments of :class:`{cls.__qualname__}`.

        Returns:
           :class:`{cls.__qualname__}`'s arguments unpacked.

        Raises:
           TypeError: Object is not :class:`{cls.__qualname__}`.
        """
        s = 'unpack_' + cls._snake_case_name
        setattr(top, s, f_unpack)
        setattr(top, '_' + s, lambda x: cls._unpack(x))

    @classmethod
    def _init_preprocess_arg_(mcls, top: TObj, cls: TObj):
        ###
        # cls._check_arg_{cls}
        ###
        s_check_arg = '_check_arg_' + cls._snake_case_name
        if hasattr(cls, s_check_arg):
            f_check_arg = getattr(cls, s_check_arg)
        else:
            def mk_check_arg_(c):
                def check_arg_(
                        cls_,
                        arg: Any,
                        function: Optional[Union[TFun, str]] = None,
                        name: Optional[str] = None,
                        position: Optional[int] = None
                ) -> Union[c, NoReturn]:
                    return c.check(arg, function, name, position)
                return check_arg_
            f_check_arg = classmethod(mk_check_arg_(cls))
        setattr(top, s_check_arg, f_check_arg)
        ###
        # cls._check_optional_arg_{cls}
        ###
        s_check_optional_arg = '_check_optional_arg_' + cls._snake_case_name
        if hasattr(cls, s_check_optional_arg):
            f_check_optional_arg = getattr(cls, s_check_optional_arg)
        else:
            def mk_check_optional_arg_(c):
                def check_optional_arg_(
                        cls_,
                        arg: Any,
                        default: Optional[c] = None,
                        function: Optional[Union[TFun, str]] = None,
                        name: Optional[str] = None,
                        position: Optional[int] = None,
                        _f_check_arg: TFun = getattr(c, s_check_arg)
                ) -> Union[Optional[c], NoReturn]:
                    if arg is None:
                        return default
                    else:
                        return _f_check_arg(arg, function, name, position)
                return check_optional_arg_
            f_check_optional_arg = classmethod(mk_check_optional_arg_(cls))
        setattr(top, s_check_optional_arg, f_check_optional_arg)
        ###
        # cls._preprocess_arg_{cls}
        ###
        s_preprocess_arg = '_preprocess_arg_' + cls._snake_case_name
        if hasattr(cls, s_preprocess_arg):
            f_preprocess_arg = getattr(cls, s_preprocess_arg)
        else:
            def mk_preprocess_arg_(c):
                def preprocess_arg_(
                        cls_,
                        arg: Any,
                        i: int,
                        function: Optional[Union[TFun, str]] = None,
                        _f_check_arg: TFun = getattr(c, s_check_arg)
                ) -> Union[c, NoReturn]:
                    return _f_check_arg(arg, function or cls_, None, i)
                return preprocess_arg_
            f_preprocess_arg = classmethod(mk_preprocess_arg_(cls))
        setattr(top, s_preprocess_arg, f_preprocess_arg)
        ###
        # cls._preprocess_optional_arg_{cls}
        ###
        s_preprocess_optional_arg = (
            '_preprocess_optional_arg_' + cls._snake_case_name)
        if hasattr(cls, s_preprocess_optional_arg):
            f_preprocess_optional_arg = getattr(
                cls, s_preprocess_optional_arg)
        else:
            def mk_preprocess_optional_arg_(c):
                def preprocess_optional_arg_(
                        cls_,
                        arg: Any,
                        i: int,
                        default: Optional[c] = None,
                        function: Optional[Union[TFun, str]] = None,
                        _f_preprocess_arg: TFun = getattr(
                            c, s_preprocess_arg)
                ) -> Union[Optional[c], NoReturn]:
                    if arg is None:
                        return default
                    else:
                        return _f_preprocess_arg(arg, i, function)
                return preprocess_optional_arg_
            f_preprocess_optional_arg = classmethod(
                mk_preprocess_optional_arg_(cls))
        setattr(top, s_preprocess_optional_arg, f_preprocess_optional_arg)


# -- Object ----------------------------------------------------------------

@functools.total_ordering
class Object(collections.abc.Sequence, metaclass=ObjectMeta):
    """Abstract base class for syntactical objects."""

    #: Class name in snake case.
    _snake_case_name: str = 'object'

    #: Absence of value distinct from ``None``.
    Nil: NilType = Nil

    @classmethod
    def test(cls, obj: Any) -> bool:
        """Tests `obj` class.

        Parameters:
           obj: Value.

        Returns:
           ``True`` if `obj` is an instance of this class;
           ``False`` otherwise.
        """
        return isinstance(obj, cls)

    @classmethod
    def check(
            cls,
            obj: 'Object',
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Object', NoReturn]:
        """Checks `obj` class.

        Parameters:
           obj: Value.
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           `obj`.

        Raises:
           TypeError: `obj` is not an instance of this class.
        """
        return cls._check(obj, function or cls.check, name, position)

    @classmethod
    def check_optional(
            cls,
            obj: Optional['Object'],
            default: Optional['Object'] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional['Object'], NoReturn]:
        """Checks optional `obj` class.

        If `obj` is ``None``, returns `default`.

        Parameters:
           obj: Value.
           default: Default value.
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           `obj`.

        Raises:
           TypeError: `obj` is not an instance of this class.
        """
        return cls._check_optional(
            obj, default, function or cls.check_optional, name, position)

    _check_test = (lambda x, y: y.test(x))

    @classmethod
    def _check(
            cls,
            obj: 'Object',
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Object', NoReturn]:
        return cls._check_arg_isinstance(
            obj, cls, function, name, position, cls._check_test)

    @classmethod
    def _check_optional(
            cls,
            obj: Optional['Object'],
            default: Optional['Object'] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional['Object'], NoReturn]:
        return cls._check_optional_arg_isinstance(
            obj, cls, default, function, name, position, cls._check_test)

    @classmethod
    def unpack(
            cls,
            obj: 'Object',
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        """Unpacks `obj`'s arguments.

        Parameters:
           obj: Object.
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           `obj`'s arguments unpacked.

        Raises:
           TypeError: `obj` is not an instance of this class.
        """
        return cls._unpack(cls.check(
            obj, function or cls.unpack, name, position))

    @classmethod
    def _unpack(cls, obj: 'Object') -> TArgs:
        return obj.args

    __slots__ = (
        '_args',
        '_hash',
        '_digest',
    )

    _args: TArgs
    _hash: Optional[int]
    _digest: Optional[str]

    @abc.abstractmethod
    def __init__(self, *args):
        self._set_args(self._preprocess_args(args))
        self._hash = None
        self._digest = None

    def _set_args(self, args: TArgs):
        self._args = args

    def _preprocess_args(self, args: TArgs) -> TArgs:
        return tuple(map(
            self._preprocess_arg_callback, zip(args, itertools.count(1))))

    def _preprocess_arg_callback(self, t: tuple[Any, int]) -> Any:
        return self._preprocess_arg(*t)

    def _preprocess_arg(self, arg: T, i: int) -> Union[T, NoReturn]:
        return self._check_arg_not_none(arg, self.__class__, None, i)

    def __eq__(self, other):
        return type(self) is type(other) and self._args == other._args

    def __getitem__(self, i):
        return self.args[i]

    def __hash__(self):
        if self._hash is None:
            self._hash = hash((self.__class__, self._args))
        return self._hash

    def __len__(self):
        return len(self.args)

    def __lt__(self, other):
        other = Object.check(other, self.__class__.__lt__)
        if type(self) is not type(other):
            return (self.__class__.__qualname__
                    < other.__class__.__qualname__)
        else:
            return self.args < other.args

    def __str__(self):
        return self.dumps()

    @property
    def args(self) -> TArgs:
        """The arguments of object."""
        return self.get_args()

    def get_args(self) -> TArgs:
        """Gets the arguments of object.

        Returns:
           Arguments.
        """
        return self._args

    @property
    def digest(self) -> str:
        """The string digest of object."""
        return self.get_digest()

    def get_digest(self) -> str:
        """Gets the string digest of object.

        Returns:
           String digest.
        """
        if self._digest is None:
            self._digest = self._hexdigest(self.dumps())
        return self._digest

    def _hexdigest(self, s: str):
        import hashlib
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    # -- Copying -----------------------------------------------------------

    def copy(self) -> 'Object':
        """Makes a shallow copy of object.

        Returns:
           A shallow copy of object.
        """
        return copy.copy(self)

    def deepcopy(self, memo: Optional[dict[Any, Any]] = None) -> 'Object':
        """Makes a deep copy of object.

        Parameters:
           memo: Dictionary of objects already copied.

        Returns:
           A deep copy of object.
        """
        return copy.deepcopy(self, memo=memo)

    def replace(self, *args: Any) -> 'Object':
        """Shallow-copies object overwriting the given arguments.

        If a given argument is `None`, keeps the value of the corresponding
        argument in the resulting object.

        If a given argument is :attr:`Nil`, sets the corresponding argument
        to `None` in the resulting object.

        Parameters:
           args: Arguments.

        Returns:
           A shallow copy of object.
        """
        return self.__class__(*itertools.starmap(
            self._replace, itertools.zip_longest(self.args, args)))

    def _replace(self, x, y):
        if y is None:
            return x
        elif y is self.Nil:
            return None
        else:
            return y

    # -- Encoding ----------------------------------------------------------

    @classmethod
    def _install_encoder(cls, encoder: type['Encoder']):
        def mk_to_(fmt: str):
            def to_(obj: Object, **kwargs: Any) -> str:
                return obj.dumps(fmt, **kwargs)
            return to_
        f_to = mk_to_(encoder.format)
        f_to.__doc__ = f"""\
        Encodes object using {encoder.description}.

        Parameters:
           kwargs: Options to {encoder.description}.

        Returns:
           The resulting string.

        Raises:
           `EncoderError`: Encoder error
        """
        setattr(cls, 'to_' + encoder.format, f_to)

    def dump(self, fp: IO[Any], format: Optional[str] = None, **kwargs):
        """Encodes object and writes the result to stream.

        Parameters:
           fp: A ``.write()``-supporting file-like object.
           format: Encoding format.
           kwargs: Encoder options.

        Raises:
           `EncoderError`: Encoder error.
        """
        enc = Encoder.from_format(format, self.dump, 'format', 2)
        for chunk in enc(**kwargs).iterencode(self):
            fp.write(chunk)

    def dumps(self, format: Optional[str] = None, **kwargs) -> str:
        """Encodes object and returns the resulting string.

        Parameters:
           format: Encoding format.
           kwargs: Encoder options.

        Returns:
           The resulting string.

        Raises:
           `EncoderError`: Encoder error.
        """
        enc = Encoder.from_format(format, self.dumps, 'format', 1)
        return enc(**kwargs).encode(self)

    # -- Decoding ----------------------------------------------------------

    @classmethod
    def _install_decoder(cls, decoder: type['Decoder']):
        def mk_from_(fmt: str):
            def from_(
                    obj_cls: type[Object],
                    s: str,
                    **kwargs
            ) -> Union[Object, NoReturn]:
                return obj_cls.loads(s, fmt, **kwargs)
            return from_
        f_from = mk_from_(decoder.format)
        f_from.__doc__ = f"""\
        Decodes string using {decoder.description}.

        Parameters:
           kwargs: Options to {decoder.description}.

        Returns:
           The resulting object.

        Raises:
           `DecoderError`: Decoder error.
        """
        setattr(cls, 'from_' + decoder.format, classmethod(f_from))

    @classmethod
    def load(
            cls,
            fp: IO[Any],
            format: Optional[str] = None,
            **kwargs
    ) -> Union['Object', NoReturn]:
        """Decodes stream and returns the resulting object.

        Parameters:
           fp: A ``.read()``-supporting file-like object.
           format: Decoding format.
           kwargs: Decoder options.

        Returns:
           The resulting object.

        Raises:
           `DecoderError`: Decoder error.
        """
        return cls.loads(fp.read(), format, **kwargs)

    @classmethod
    def loads(
            cls,
            s: str,
            format: Optional[str] = None,
            **kwargs
    ) -> Union['Object', NoReturn]:
        """Decodes string and returns the resulting object.

        Parameters:
           s: String.
           format: Decoding format.
           kwargs: Options to decoder.

        Returns:
           The resulting object.

        Raises:
           `DecoderError`: Decoder error
        """
        dec = Decoder.from_format(format, cls.loads, 'format', 2)
        return cls.check(dec(**kwargs).decode(s), cls.load)

    # -- Argument checking -------------------------------------------------

    _arg_error_default_prefix = 'bad argument'
    _arg_error_default_exception = ValueError

    @classmethod
    def _arg_error(
            cls,
            details: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            exception: Optional[type[Exception]] = None,
            prefix: Optional[str] = None
    ) -> Exception:
        msg = prefix or Object._arg_error_default_prefix
        if position:
            assert position > 0
            msg += f' #{position}'
        if name:
            msg += f' ({name})'
        if function:
            if hasattr(function, '__qualname__'):
                function = function.__qualname__
            msg += f" to '{function}'"
        if details:
            msg += f' ({details})'
        return (exception or Object._arg_error_default_exception)(msg)

    @classmethod
    def _check_arg(
            cls,
            arg: T,
            test: Union[Callable[[T], bool], bool] = lambda x: True,
            details: Optional[Union[Callable[[T], str], str]] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            exception: Optional[type[Exception]] = None,
            prefix: Optional[str] = None
    ) -> Union[T, NoReturn]:
        if (test(arg) if callable(test) else test):
            return arg
        else:
            raise Object._arg_error(
                details(arg) if callable(details) else details,
                function, name, position, exception, prefix)

    @classmethod
    def _check_optional_arg(
            cls,
            arg: Optional[T],
            default: Optional[T] = None,
            test: Union[Callable[[T], bool], bool] = lambda x: True,
            details: Optional[Union[Callable[[T], str], str]] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            exception: Optional[type[Exception]] = None,
            prefix: Optional[str] = None
    ) -> Union[Optional[T], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg(
                arg, test, details, function, name, position,
                exception, prefix)

    @classmethod
    def _check_arg_not_none(
            cls,
            arg: T,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[T, NoReturn]:
        return Object._check_arg(
            arg, arg is not None, 'expected value, got None',
            function, name, position, TypeError)

    # -- callable --

    _check_arg_callable_details = (
        lambda x: f'expected callable, got {type(x).__qualname__}')

    @classmethod
    def _check_arg_callable(
            cls,
            arg: T,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
    ) -> Union[T, NoReturn]:
        return Object._check_arg(
            arg, callable, cls._check_arg_callable_details,
            function, name, position, TypeError)

    @classmethod
    def _check_optional_arg_callable(
            cls,
            arg: Optional[T],
            default: Optional[T] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[T], NoReturn]:
        return Object._check_optional_arg(
            arg, default, callable, cls._check_arg_callable_details,
            function, name, position, TypeError)

    # -- isinstance --

    @classmethod
    def _check_arg_isinstance(
            cls,
            arg: T,
            ty: Union[type, tuple[type, ...]],
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            test=isinstance
    ) -> Union[T, NoReturn]:
        if test(arg, ty):
            return arg
        else:
            if isinstance(ty, type):
                ty_name = ty.__qualname__
            else:
                ty_name = ' or '.join(sorted(map(
                    lambda x: x.__qualname__, ty)))
            raise Object._arg_error(
                f'expected {ty_name}, got {type(arg).__qualname__}',
                function, name, position, TypeError)

    @classmethod
    def _check_optional_arg_isinstance(
            cls,
            arg: Optional[T],
            ty: Union[type, tuple[type, ...]],
            default: Optional[T] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            test=isinstance
    ) -> Union[Optional[T], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_isinstance(
                arg, ty, function, name, position, test)

    # -- bool --

    @classmethod
    def _check_arg_bool(
            cls,
            arg: bool,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[bool, NoReturn]:
        return cls._check_arg_isinstance(
            arg, bool, function, name, position)

    @classmethod
    def _check_optional_arg_bool(
            cls,
            arg: Optional[bool],
            default: Optional[bool] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[bool], NoReturn]:
        return cls._check_optional_arg_isinstance(
            arg, bool, default, function, name, position)

    @classmethod
    def _preprocess_arg_bool(
            cls,
            arg: bool,
            i: int,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[bool, NoReturn]:
        return cls._check_arg_bool(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_bool(
            cls,
            arg: Optional[bool],
            i: int,
            default: Optional[bool] = None,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[Optional[bool], NoReturn]:
        return cls._check_optional_arg_bool(
            arg, default, function or cls, None, i)

    # -- int --

    @classmethod
    def _check_arg_int(
            cls,
            arg: int,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[int, NoReturn]:
        return cls._check_arg_isinstance(
            arg, int, function, name, position)

    @classmethod
    def _check_optional_arg_int(
            cls,
            arg: Optional[int],
            default: Optional[int] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[int], NoReturn]:
        return cls._check_optional_arg_isinstance(
            arg, int, default, function, name, position)

    @classmethod
    def _preprocess_arg_int(
            cls,
            arg: int,
            i: int,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[int, NoReturn]:
        return cls._check_arg_int(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_int(
            cls,
            arg: Optional[int],
            i: int,
            default: Optional[int] = None,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[Optional[int], NoReturn]:
        return cls._check_optional_arg_int(
            arg, default, function or cls, None, i)

    # -- float --

    @classmethod
    def _check_arg_float(
            cls,
            arg: float,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[float, NoReturn]:
        return cls._check_arg_isinstance(
            arg, float, function, name, position)

    @classmethod
    def _check_optional_arg_float(
            cls,
            arg: Optional[float],
            default: Optional[float] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[float], NoReturn]:
        return cls._check_optional_arg_isinstance(
            arg, float, default, function, name, position)

    @classmethod
    def _preprocess_arg_float(
            cls,
            arg: float,
            i: int,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[float, NoReturn]:
        return cls._check_arg_float(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_float(
            cls,
            arg: Optional[float],
            i: int,
            default: Optional[float] = None,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[Optional[float], NoReturn]:
        return cls._check_optional_arg_float(
            arg, default, function or cls, None, i)

    # -- number --

    @classmethod
    def _check_arg_number(
            cls,
            arg: TNum,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TNum, NoReturn]:
        return cls._check_arg_isinstance(
            arg, (float, int), function, name, position)

    @classmethod
    def _check_optional_arg_number(
            cls,
            arg: Optional[TNum],
            default: Optional[TNum] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[TNum], NoReturn]:
        return cls._check_optional_arg_isinstance(
            arg, (float, int), default, function, name, position)

    @classmethod
    def _preprocess_arg_number(
            cls,
            arg: TNum,
            i: int,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[TNum, NoReturn]:
        return cls._check_arg_number(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_number(
            cls,
            arg: Optional[TNum],
            i: int,
            default: Optional[TNum] = None,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[Optional[TNum], NoReturn]:
        return cls._check_optional_arg_number(
            arg, default, function or cls, None, i)

    # -- str --

    @classmethod
    def _check_arg_str(
            cls,
            arg: str,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[str, NoReturn]:
        return cls._check_arg_isinstance(
            arg, str, function, name, position)

    @classmethod
    def _check_optional_arg_str(
            cls,
            arg: Optional[str],
            default: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[str], NoReturn]:
        return cls._check_optional_arg_isinstance(
            arg, str, default, function, name, position)

    @classmethod
    def _preprocess_arg_str(
            cls,
            arg: str,
            i: int,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[str, NoReturn]:
        return cls._check_arg_str(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_str(
            cls,
            arg: Optional[str],
            i: int,
            default: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None
    ) -> Union[Optional[str], NoReturn]:
        return cls._check_optional_arg_str(
            arg, default, function or cls, None, i)

    # -- Utility -----------------------------------------------------------

    _camel2snake_re1 = re.compile(r'([^_])([A-Z][a-z]+)')
    _camel2snake_re2 = re.compile(r'([a-z0-9])([A-Z])')

    @classmethod
    def _camel2snake(cls, name: str) -> str:
        """Converts from camel-case name to snake-case.

        Parameters:
           name: Name (i.e., id-like :class:`str`).

        Returns:
           `name` converted to snake-case.
        """
        return cls._camel2snake_re2.sub(
            r'\1_\2', cls._camel2snake_re1.sub(r'\1_\2', name)).lower()

    @classmethod
    def _must_be_implemented_in_subclass(
            cls,
            details: Optional[str] = None
    ) -> MustBeImplementedInSubclass:
        """Makes a "must be implemented in subclass" error.

        Parameters:
           details: Details.

        Returns:
           A new :class:`MustBeImplementedInSubclass` error.
        """
        if details:
            return MustBeImplementedInSubclass(details)
        else:
            return MustBeImplementedInSubclass()

    @classmethod
    def _should_not_get_here(
            cls, details: Optional[str] = None) -> ShouldNotGetHere:
        """Makes a "should not get here" error.

        Parameters:
           details: Details.

        Returns:
           A new :class:`ShouldNotGetHere` error.
        """
        if details:
            return ShouldNotGetHere(details)
        else:
            return ShouldNotGetHere()


# -- Codec -----------------------------------------------------------------

class CodecError(Error):
    """Base class for codec errors."""


class Codec(abc.ABC):
    """Abstract base class for codecs."""

    registry: dict[str, type['Codec']] = dict()
    default: str

    format: str
    description: str

    @classmethod
    def _register(
            cls,
            codec: type['Codec'],
            format: str,
            description: str):
        codec.format = format
        codec.description = description
        cls.registry[format] = codec

    @classmethod
    def from_format(
            cls,
            format: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            details: Optional[Callable[[Any], str]] = None
    ) -> Union[type['Codec'], NoReturn]:
        fmt: str = format or cls.default
        Object._check_arg(
            fmt, fmt in cls.registry, details, function, name, position)
        assert fmt is not None
        return cls.registry[fmt]


class EncoderError(CodecError):
    """Base class for encoder errors."""


class Encoder(Codec):
    """Abstract base class for encoders."""

    registry = dict()
    default: str

    @classmethod
    def __init_subclass__(
            cls,
            format: str,
            description: str):
        Encoder._register(cls, format, description)
        Object._install_encoder(cls)

    @classmethod
    def from_format(
            cls,
            format: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            _details=lambda x: f"no such encoder '{x}'"
    ) -> type['Encoder']:
        return cast(type[Encoder], super().from_format(
            format, function, name, position, _details))

    def encode(self, obj: Object) -> Union[str, NoReturn]:
        """Encodes object.

        Parameters:
           obj: Object.

        Returns:
           The resulting string.

        Raises:
           `DecoderError`: Decoder error.
        """
        return ''.join(self.iterencode(obj))

    @abc.abstractmethod
    def iterencode(
            self,
            obj: Object
    ) -> Union[Generator[str, None, None], NoReturn]:
        """Encodes object iteratively.

        Yields each string as available.

        Parameters:
           obj: Object.

        Returns:
           An iterator of strings.

        Raises:
           `DecoderError`: Decoder error.
        """
        raise MustBeImplementedInSubclass


class SExpEncoder(
        Encoder, format='sexp', description='S-expression encoder'):
    """S-expression encoder."""

    def __init__(self, indent: int = 0):
        self.indent = indent

    def iterencode(self, obj: Object) -> Generator[str, None, None]:
        return self._iterencode(obj, 0, self.indent)

    def _iterencode(
            self,
            v: Any,
            n: int = 0,
            indent: int = 0) -> Generator[str, None, None]:
        dl = '\n' if indent > 0 else ''
        sp = '\n' if indent > 0 else ' '
        yield ' ' * indent * n
        if isinstance(v, (Object, list, tuple)):
            if Object.test(v):
                if v:
                    yield '('
                yield v.__class__.__qualname__
                if v and indent == 0:
                    yield ' '
            else:
                yield '['
            if v:
                yield dl
                for i in range(len(v) - 1):
                    yield from self._iterencode(v[i], n + 1, indent)
                    yield sp
                yield from self._iterencode(v[-1], n + 1, indent)
            if v:
                yield dl
                yield ' ' * indent * n
            if Object.test(v):
                if v:
                    yield ')'
            else:
                yield ']'
        else:
            try:
                yield json.dumps(v, ensure_ascii=False)
            except TypeError as err:
                raise EncoderError(str(err)) from None


class JSON_Encoder(Encoder, format='json', description='JSON encoder'):
    """JSON Encoder."""

    class Encoder(json.JSONEncoder):
        def default(self, v: Any) -> Any:
            if isinstance(v, Object):
                obj = cast(Object, v)
                return {
                    'class': obj.__class__.__qualname__,
                    'args': obj.args,
                }
            else:
                try:
                    return json.JSONEncoder.default(self, v)
                except TypeError as err:
                    raise EncoderError(str(err)) from None

    def __init__(self, **kwargs):
        self.enc = self.Encoder(**kwargs)

    def iterencode(self, obj: Object) -> Generator[str, None, None]:
        return self.enc.iterencode(obj)


class DecoderError(CodecError):
    """Base class for decoder errors."""


class Decoder(Codec):
    """Abstract base class for decoders."""

    registry = dict()
    default: str

    @classmethod
    def __init_subclass__(cls, format: str, description: str):
        Decoder._register(cls, format, description)
        Object._install_decoder(cls)

    @classmethod
    def from_format(
            cls,
            format: Optional[str] = None,
            function: Optional[Union[TFun, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            _details=lambda x: f"no such decoder '{x}'"
    ) -> type['Decoder']:
        return cast(type[Decoder], super().from_format(
            format, function, name, position, _details))

    @classmethod
    def check_object_class(
            cls,
            cls_name: str,
            exception: type[Exception] = DecoderError
    ) -> Union[type[Object], NoReturn]:
        if cls_name not in ObjectMeta._object_subclasses:
            raise exception(f"no such object class '{cls_name}'")
        return ObjectMeta._object_subclasses[cls_name]

    @abc.abstractmethod
    def decode(self, s: str) -> Union[Object, NoReturn]:
        """Decodes string.

        Parameters:
           s: String.

        Return:
           The resulting object.

        Raises:
           `DecoderError`: Decoder error.
        """
        raise MustBeImplementedInSubclass


class SExpDecoder(
        Decoder, format='sexp', description='S-expression decoder'):
    """S-expression decoder."""

    grammar = r"""
?sexp: cls                  -> sexp
     | "(" cls value* ")"   -> sexp

%import common.CNAME
cls: CNAME

?value: bool | int | float | str | list | sexp

bool: "true" -> true
    | "false" -> false

%import common.SIGNED_INT
int: SIGNED_INT -> int_

%import common.SIGNED_FLOAT
float: SIGNED_FLOAT -> float_

%import common.ESCAPED_STRING
str: ESCAPED_STRING -> str_

list: "[" value* "]" -> list_

%import common.SH_COMMENT
%ignore SH_COMMENT

%import common.WS
%ignore WS
"""

    class Visitor(lark.visitors.Transformer_InPlaceRecursive):

        def __init__(self):
            super().__init__()

        @lark.v_args(inline=True)
        def sexp(self, cls, *args):
            return cls(*args)

        @lark.v_args(inline=True)
        def cls(self, s):
            return Decoder.check_object_class(s)

        @lark.v_args(inline=True)
        def true(self):
            return True

        @lark.v_args(inline=True)
        def false(self):
            return False

        @lark.v_args(inline=True)
        def int_(self, s):
            return int(s)

        @lark.v_args(inline=True)
        def float_(self, s):
            return float(s)

        @lark.v_args(inline=True)
        def str_(self, s):
            return s[1:-1]

        @lark.v_args(inline=True)
        def list_(self, *args):
            return list(args)

    def __init__(self):
        self.parser = lark.Lark(
            self.grammar, start='sexp', parser='lalr',
            transformer=self.Visitor(), cache=True)

    def decode(self, s: str) -> Union[Object, NoReturn]:
        try:
            return self.parser.parse(s)
        except lark.exceptions.UnexpectedInput as err:
            line, col, ctx = err.line, err.column, err.get_context(s)
            raise DecoderError(
                f'syntax error at line {line}, column {col}\n\n{ctx}')\
                from None


class JSON_Decoder(Decoder, format='json', description='JSON decoder'):
    """JSON decoder."""

    class Decoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, object_hook=self.object_hook, **kwargs)

        def object_hook(self, o):
            assert isinstance(o, dict)
            if 'class' not in o:
                raise DecoderError("missing field 'class'")
            cls = Decoder.check_object_class(o['class'])
            return cls(*o.get('args', ()))

    def __init__(self, **kwargs):
        self.dec = self.Decoder(**kwargs)

    def decode(self, s: str) -> Union[Object, NoReturn]:
        return self.dec.decode(s)


# -- Defaults --------------------------------------------------------------

Decoder.default = SExpDecoder.format
Encoder.default = SExpEncoder.format
ObjectMeta._object_class = Object
