# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re
from pathlib import Path

from kif_lib.model import kif_object

kif_object_py_path = Path(kif_object.__file__)
expected_kif_object_py_path = Path('./kif_lib/model/kif_object.py').absolute()
assert kif_object_py_path == expected_kif_object_py_path

kif_object_pyi_path = kif_object_py_path.with_suffix('.pyi')
fout = open(kif_object_pyi_path, 'w')


def p(*args, **kwargs):
    print(*args, file=kwargs.pop('file', fout), **kwargs)


def pp(*args, **kwargs):
    p(*args, end=kwargs.pop('end', '\n\n'), **kwargs)


pp('''\
#
# ** GENERATED FILE, DO NOT EDIT! **
#''')

with open(kif_object_py_path.with_suffix('.pyi.in')) as fin:
    for line in fin:
        p(line, end='')
p()

p('''\
#
# ** START OF GENERATED CODE **
#''')


def quoted_cls_name(cls):
    if cls is KIF_Object:
        return f"'{cls.__qualname__}'"
    else:
        return cls.__qualname__


def match(regexp, attr):
    m = regexp.match(attr)
    if not m:
        return None
    (cls_snake_case_name,) = m.groups()
    cls = KIF_Object._object_subclasses.get(cls_snake_case_name)
    if cls is None:
        return None
    cls_name = quoted_cls_name(cls)
    return cls, cls_name, cls_snake_case_name


def TC(cls_name, _TC={
        'Datatype': 'TDatatypeClass',
        'Template': 'TTemplateClass',
        'Variable': 'TVariableClass',
}):
    return _TC.get(cls_name, f'type[{cls_name}]')


def T(cls_name, _T={
        'AnnotationRecordSet': 'TAnnotationRecordSet',
        'EntityFingerprint': 'TEntityFingerprint',
        'ExternalId': 'TExternalId',
        'Fingerprint': 'TFingerprint',
        'IRI': 'T_IRI',
        'Item': 'TItem',
        'KIF_ObjectSet': 'T_KIF_ObjectSet',
        'Lexeme': 'TLexeme',
        'Property': 'TProperty',
        'PropertyFingerprint': 'TPropertyFingerprint',
        'Quantity': 'TQuantity',
        'ReferenceRecord': 'TReferenceRecord',
        'ReferenceRecordSet': 'TReferenceRecordSet',
        'SnakSet': 'TSnakSet',
        'String': 'TString',
        'Text': 'TText',
        'TextSet': 'TTextSet',
        'Time': 'TTime',
        'Value': 'TValue',
        'ValueSet': 'TValueSet',
}):
    return _T.get(cls_name, cls_name)


re__check_arg = re.compile(r'^_check_arg_([a-z_]+)$')
re__check_arg__class = re.compile(r'^_check_arg_([a-z_]+)_class$')
re__check_optional_arg = re.compile(r'^_check_optional_arg_([a-z_]+)$')
re__check_optional_arg__class = re.compile(
    r'^_check_optional_arg_([a-z_]+)_class$')

re__preprocess_arg = re.compile(r'^_preprocess_arg_([a-z_]+)$')
re__preprocess_optional_arg = re.compile(
    r'^_preprocess_optional_arg_([a-z_]+)$')

re_check = re.compile(r'^check_([a-z_]+)$')
re_is = re.compile(r'^is_([a-z_]+)$')
re_test = re.compile(r'^test_([a-z_]+)$')
re_unpack = re.compile(r'^unpack_([a-z_]+)$')

KIF_Object = kif_object.KIF_Object
for attr in sorted(dir(KIF_Object)):
    value = getattr(KIF_Object, attr)
    if (attr[0] == '_' and attr[1].isalpha() and attr[1].isupper()
            and issubclass(value, KIF_Object)):
        pp(f'    {attr}: type[{quoted_cls_name(value)}]')
        continue

    t = match(re__check_arg__class, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _check_arg_{cls_snake_case_name}_class(
            cls,
            arg: {TC(cls_name)},
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> type[{cls_name}]:
        ...''')
        continue

    t = match(re__check_arg, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _check_arg_{cls_snake_case_name}(
            cls,
            arg: {T(cls_name)},
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> {cls_name}:
        ...''')
        continue

    t = match(re__check_optional_arg__class, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _check_optional_arg_{cls_snake_case_name}_class(
            cls,
            arg: Optional[{TC(cls_name)}],
            default: Optional[type[{cls_name}]] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[type[{cls_name}]]:
        ...''')
        continue

    t = match(re__check_optional_arg, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _check_optional_arg_{cls_snake_case_name}(
            cls,
            arg: Optional[{T(cls_name)}],
            default: Optional[{cls_name}] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[{cls_name}]:
        ...''')
        continue

    t = match(re__preprocess_arg, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _preprocess_arg_{cls_snake_case_name}(
            cls,
            arg: {T(cls_name)},
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> {cls_name}:
        ...''')
        continue

    t = match(re__preprocess_optional_arg, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    @classmethod
    def _preprocess_optional_arg_{cls_snake_case_name}(
            cls,
            arg: Optional[{T(cls_name)}],
            i: int,
            default: Optional[{cls_name}] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[{cls_name}]:
        ...''')
        continue

    t = match(re_check, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    def check_{cls_snake_case_name}(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> {cls_name}:
        ...''')
        continue

    t = match(re_is, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    def is_{cls_snake_case_name}(self) -> bool: ...''')
        continue

    t = match(re_test, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    def test_{cls_snake_case_name}(self) -> bool: ...''')
        continue

    t = match(re_unpack, attr)
    if t:
        cls, cls_name, cls_snake_case_name = t
        pp(f'''\
    def unpack_{cls_snake_case_name}(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> TArgs:
        ...''')
        continue

p('''\
#
# ** END OF GENERATED CODE **
#''')

fout.close()
