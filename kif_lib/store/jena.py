# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id$
#
# Jpype-based Python bindings for Jena RDF.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import json
import os
import pathlib

from typing_extensions import Any, ClassVar, Protocol


class Jena:
    """Jpype-based Python bindings for Jena RDF."""

    #: Whether JPype was initialized.
    _init: ClassVar[bool] = False

    #: Package and class aliases (java).
    _java: ClassVar[Any]
    _ByteArrayOutputStream: ClassVar[Any]
    _IOException: ClassVar[Any]

    #: Package and class aliases (jena).
    _jena: ClassVar[Any]
    _Lang: ClassVar[Any]
    _ModelFactory: ClassVar[Any]
    _Prologue: ClassVar[Any]
    _Query: ClassVar[Any]
    _QueryExecution: ClassVar[Any]
    _QueryExecutionFactory: ClassVar[Any]
    _QueryFactory: ClassVar[Any]
    _QueryParseException: ClassVar[Any]
    _RDFDataMgr: ClassVar[Any]
    _RDFLanguages: ClassVar[Any]
    _ResultSet: ClassVar[Any]
    _ResultSetFormatter: ClassVar[Any]
    _RiotException: ClassVar[Any]
    _Syntax: ClassVar[Any]

    @classmethod
    def init(
            cls,
            jena_home: pathlib.PurePath | str | None = None
    ) -> None:
        """Initializes Python-Java and loads Jena JARs.

        If `jena_home` is not given, reads it from the
        ``JENA_HOME`` environment variable.

        Parameters:
           jena_java_dir: Path to the directory containing Jena's JARs.
        """
        try:
            import jpype  # type: ignore
            import jpype.imports  # type: ignore
        except ImportError:
            raise ImportError(
                'Jena backend requires https://pypi.org/project/jpype1/')
        if jena_home is None:
            jena_home = os.getenv('JENA_HOME')
            if jena_home is None:
                raise RuntimeError('JENA_HOME is not set')
        assert jena_home is not None
        jena_home_lib = pathlib.Path(jena_home) / 'lib'
        if not jena_home_lib.exists():
            raise FileNotFoundError(str(jena_home_lib))
        if not jena_home_lib.is_dir():
            raise NotADirectoryError(str(jena_home_lib))
        jpype.startJVM(classpath=list(
            map(str, pathlib.Path(jena_home_lib).glob('*.jar'))))
        java = jpype.JPackage('java')
        cls._java = java
        cls._ByteArrayOutputStream = java.io.ByteArrayOutputStream
        cls._IOException = java.io.IOException
        jena = jpype.JPackage('org.apache.jena')
        cls._jena = jena
        cls._Lang = jena.riot.Lang
        cls._ModelFactory = jena.rdf.model.ModelFactory
        cls._Prologue = jena.sparql.core.Prologue
        cls._Query = jena.query.Query
        cls._QueryExecution = jena.query.QueryExecution
        cls._QueryExecutionFactory = jena.query.QueryExecutionFactory
        cls._QueryFactory = jena.query.QueryFactory
        cls._QueryParseException = jena.query.QueryParseException
        cls._RDFDataMgr = jena.riot.RDFDataMgr
        cls._RDFLanguages = jena.riot.RDFLanguages
        cls._ResultSet = jena.query.ResultSet
        cls._ResultSetFormatter = jena.query.ResultSetFormatter
        cls._RiotException = jena.riot.RiotException
        cls._Syntax = jena.query.Syntax
        cls._init = True

    #: Interface for jena.riot.Lang.
    class Lang(Protocol):
        pass

    #: Interface for jena.rdf.model.Model.
    class Model(Protocol):
        pass

    #: Interface for jena.query.Query.
    class Query(Protocol):

        def isAskType(self) -> bool:
            ...

        def isConstructType(self) -> bool:
            ...

        def isDescribeType(self) -> bool:
            ...

        def isSelectType(self) -> bool:
            ...

    #: Interface for jena.query.QueryExecution.
    class QueryExecution(Protocol):

        def close(self) -> None:
            ...

        def execAsk(self) -> bool:
            ...

        def execConstruct(self) -> Jena.Model:
            ...

        def execDescribe(self) -> Jena.Model:
            ...

        def execSelect(self) -> dict[str, Any]:
            ...

        def getQuery(self) -> Jena.Query:
            ...

    __slots__ = (
        'model',
    )

    #: Model.
    model: Model

    def __init__(
            self,
            jena_home: pathlib.PurePath | str | None = None
    ) -> None:
        if not self._init:
            self.init(jena_home)
        assert self._init
        self.model: Jena.Model = self._ModelFactory.createDefaultModel()

    def load(
            self,
            location: pathlib.PurePath | str,
            format: str | None = None
    ) -> None:
        """Loads RDF from location.

        Parameters:
           location: URI or path.
           format: Format.
        """
        try:
            self._RDFDataMgr.read(
                self.model,
                str(pathlib.Path(location)),
                self._format2lang(format) if format is not None
                else self._RDFLanguages.N3)  # type: ignore
        except self._RiotException as err:
            raise err

    def _format2lang(self, format: str) -> Jena.Lang:
        lang = self._RDFLanguages.nameToLang(format)  # type:ignore
        if lang is None:
            raise ValueError(f"bad format '{format}'")
        else:
            return lang

    def query(self, text: str) -> bool | Model | dict[str, Any]:
        """Evaluates SPARQL query.

        Parameters:
           text: Query text.

        Returns:
           The query results.
        """
        exec = self._query_prepare(text)
        query = exec.getQuery()
        try:
            if query.isAskType():
                return bool(exec.execAsk())
            elif query.isConstructType():
                return exec.execConstruct()
            elif query.isDescribeType():
                return exec.execDescribe()
            elif query.isSelectType():
                out = self._ByteArrayOutputStream()
                self._ResultSetFormatter.outputAsJSON(out, exec.execSelect())
                return json.loads(str(out.toString()))
            else:
                raise RuntimeError('should not get here')
        except self._IOException as err:
            raise err
        finally:
            exec.close()

    def _query_prepare(self, text: str) -> QueryExecution:
        try:
            query = self._query_parse(text)
        except self._QueryParseException as err:
            raise err
        else:
            return self._QueryExecutionFactory.create(query, self.model)

    def _query_parse(self, text: str) -> Query:
        prologue = self._Prologue(
            self.model.getGraph().getPrefixMapping())  # type: ignore
        return self._QueryFactory.parse(
            self._Query(prologue), text, None,
            self._Syntax.defaultQuerySyntax)
