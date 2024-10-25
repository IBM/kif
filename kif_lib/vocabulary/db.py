# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..model import Item, Property
from ..namespace.dbpedia import DBpedia


def oc(name: str) -> Item:
    return Item(DBpedia.ONTOLOGY[name])


def op(name: str) -> Property:
    return Property(DBpedia.ONTOLOGY[name])


def p(name: str) -> Property:
    return Property(DBpedia.PROPERTY[name])


def r(name: str) -> Item:
    return Item(DBpedia.RESOURCE[name])
