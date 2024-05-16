# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from kif_lib import (
    ExternalIdDatatype,
    ItemDatatype,
    ItemDescriptor,
    LexemeDescriptor,
    PropertyDescriptor,
    Text,
    TextSet,
)
from kif_lib.vocabulary import wd

__all__ = (
    'ADAM',
    'ADAM_TTL',
    'ANDAR',
    'ANDAR_TTL',
    'BENZENE',
    'BENZENE_TTL',
    'BRAZIL',
    'BRAZIL_TTL',
    'INSTANCE',
    'INSTANCE_TTL',
    'PAINT',
    'PAINT_TTL',
)


class _TTL:

    test_data_dir: Path = Path('tests/data')
    path: Path

    @classmethod
    def __init_subclass__(cls, ttl=None):
        cls.path = cls.test_data_dir / ttl

    @classmethod
    def read(cls):
        return open(cls.path).read()


class ADAM_TTL(_TTL, ttl='adam.ttl'):

    Adam_en = ItemDescriptor(
        Text('Adam'),
        TextSet(),
        Text('first man according to the Abrahamic creation and '
             'religions such as Judaism, Christianity, and Islam'))

    Adam_es = ItemDescriptor(
        Text('Adán', 'es'),
        TextSet(
            Text('Adánico', 'es'),
            Text('Adam', 'es'),
            Text('Adan', 'es'),
            Text('Adanico', 'es')),
        Text('primer hombre, según la Biblia', 'es'))

    Adam_pt_br = ItemDescriptor(
        Text('Adão', 'pt-br'),
        TextSet(),
        Text('figura bíblica do livro de Gênesis', 'pt-br'))


class ANDAR_TTL(_TTL, ttl='andar.ttl'):

    andar_verb_pt = LexemeDescriptor(
        Text('andar', 'pt'),
        wd.verb,
        wd.Portuguese)


class BRAZIL_TTL(_TTL, ttl='brazil.ttl'):

    Brazil_en = ItemDescriptor(
        Text('Brazil'),
        TextSet(),
        Text('country in South America'))

    Brazil_pt_br = ItemDescriptor(
        Text('Brasil', 'pt-br'),
        TextSet(Text('🇧🇷', 'pt-br'), Text('pindorama', 'pt-br')),
        Text('país na América do Sul', 'pt-br'))

    Latin_America_en = ItemDescriptor(
        Text('Latin America', 'en'),
        TextSet(Text('LatAm', 'en')),
        Text('region of the Americas where Romance languages '
             'are primarily spoken', 'en'))

    Latin_America_pt_br = ItemDescriptor(
        None,
        TextSet(),
        None)


class BENZENE_TTL(_TTL, ttl='benzene.ttl'):

    benzene_en = ItemDescriptor(
        Text('benzene', 'en'),
        TextSet(Text('benzol', 'en')),
        None)

    InChIKey_en = PropertyDescriptor(
        Text('InChIKey', 'en'),
        TextSet(),
        Text('A hashed version of the full standard InChI - '
             'designed to create an identifier that encodes structural '
             'information and can also be practically '
             'used in web searching.', 'en'),
        ExternalIdDatatype())

    InChIKey_es = PropertyDescriptor(
        Text('InChIKey', 'es'),
        TextSet(),
        Text('código condensado para la identificación '
             'de un compuesto químico', 'es'),
        ExternalIdDatatype())


class INSTANCE_OF_TTL(_TTL, ttl='instance_of.ttl'):

    instance_of_en = PropertyDescriptor(
        Text('instance of'),
        TextSet(
            Text('is a'), Text('type'), Text('is of type'), Text('has type')),
        Text('that class of which this subject is a particular example '
             'and member; different from P279 (subclass of); for example: '
             'K2 is an instance of mountain; volcano is a subclass of '
             'mountain (and an instance of volcanic landform)'),
        ItemDatatype())

    instance_of_es = PropertyDescriptor(
        None,
        TextSet(),
        None,
        ItemDatatype())


class PAINT_TTL(_TTL, ttl='paint.ttl'):

    paint_verb_en = LexemeDescriptor(
        Text('paint', 'en'),
        wd.verb,
        wd.English)
