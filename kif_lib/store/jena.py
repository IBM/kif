# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id$
#
# Jpype-based Python bindings for Jena RDF.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import functools
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
    _ByteArrayInputStream: ClassVar[Any]
    _ByteArrayOutputStream: ClassVar[Any]
    _FileOutputStream: ClassVar[Any]
    _IOException: ClassVar[Any]
    _PrintStream: ClassVar[Any]

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
    _ResourceUtils: ClassVar[Any]
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
        jena_home = cls._find_jena_home(jena_home)
        assert jena_home is not None
        jena_home_lib = pathlib.Path(jena_home) / 'lib'
        if not jena_home_lib.exists():
            raise FileNotFoundError(
                f'bad JENA_HOME (no such file "{jena_home_lib}")')
        if not jena_home_lib.is_dir():
            raise NotADirectoryError(
                f'bad JENA_HOME (no not a directory "{jena_home_lib}")')
        try:
            jpype.startJVM(classpath=list(
                map(str, pathlib.Path(jena_home_lib).glob('*.jar'))))
        except BaseException as err:
            raise RuntimeError('failed to start JPype') from err
        java = jpype.JPackage('java')
        cls._java = java
        cls._ByteArrayInputStream = java.io.ByteArrayInputStream
        cls._ByteArrayOutputStream = java.io.ByteArrayOutputStream
        cls._FileOutputStream = java.io.FileOutputStream
        cls._IOException = java.io.IOException
        cls._PrintStream = java.io.PrintStream
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
        cls._ResourceUtils = jena.util.ResourceUtils
        cls._ResultSet = jena.query.ResultSet
        cls._ResultSetFormatter = jena.query.ResultSetFormatter
        cls._RiotException = jena.riot.RiotException
        cls._Syntax = jena.query.Syntax
        cls._init = True

    @classmethod
    def _find_jena_home(
            cls,
            jena_home: pathlib.PurePath | str | None
    ) -> pathlib.Path:
        if jena_home is not None:
            return pathlib.Path(jena_home)
        else:
            jena_home = os.getenv('JENA_HOME')
            if jena_home:
                return cls._find_jena_home(jena_home)
            else:
                return cls._find_jena_home(cls._find_jena_home_fallback())

    @classmethod
    @functools.cache
    def _find_jena_home_fallback(cls) -> str:
        import subprocess
        try:
            out = subprocess.run(
                ['jena'], stdout=subprocess.PIPE, check=True).stdout
            return out.decode('utf-8').split('\n')[-2].split(':')[-1].strip()
        except Exception:
            raise RuntimeError('cannot find JENA_HOME')

    class Lang(Protocol):
        """Interface for jena.riot.Lang."""

    class Model(Protocol):
        """Interface for jena.rdf.model.Model."""

        def listSubjects(self) -> Jena.ResIterator:
            ...

    class Query(Protocol):
        """Interface for jena.query.Query."""

        def isAskType(self) -> bool:
            ...

        def isConstructType(self) -> bool:
            ...

        def isDescribeType(self) -> bool:
            ...

        def isSelectType(self) -> bool:
            ...

    class QueryExecution(Protocol):
        """Interface for jena.query.QueryExecution."""

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

    class ResIterator(Protocol):
        """Interface for jena.rdf.model.ResIterator."""

        def hasNext(self) -> bool:
            ...

        def nextResource(self) -> Jena.Resource:
            ...

    class Resource(Protocol):
        """Interface for jena.rdf.model.Resource."""

        def isAnon(self) -> bool:
            ...

        def getId(self) -> str:
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

    def dump(
            self,
            location: pathlib.PurePath | str,
            format: str | None = None
    ) -> None:
        """Dumps model to location.

        Parameters:
           location: URI or path.
           format: Format.
        """
        try:
            location = str(pathlib.Path(location))
            self._RDFDataMgr.write(
                self._PrintStream(self._FileOutputStream(location)),
                self.model,
                self._format2lang(format))
        except self._IOException as err:
            raise err

    def dumps(self, format: str | None = None) -> str:
        """Dumps model to string.

        Parameters:
           format: Format.

        Returns:
           The resulting string.
        """
        try:
            out = self._ByteArrayOutputStream()
            self._RDFDataMgr.write(
                self._PrintStream(out, True, 'utf-8'),
                self.model,
                self._format2lang(format))
            return out.toString('utf-8')
        except self._IOException as err:
            raise err

    def load(
            self,
            location: pathlib.PurePath | str,
            format: str | None = None
    ) -> None:
        """Loads RDF data from location into model.

        Parameters:
           location: URI or path.
           format: Format.
        """
        try:
            self._RDFDataMgr.read(
                self.model,
                str(pathlib.Path(location)),
                self._format2lang(format))  # type: ignore
        except self._RiotException as err:
            raise err

    def loads(
            self,
            data: str,
            format: str | None = None
    ) -> None:
        """Loads RDF data from string into model.

        Parameters:
           data: Data.
           format: Format.
        """
        try:
            self._RDFDataMgr.read(
                self.model,
                self._ByteArrayInputStream(bytes(data, 'utf-8')),
                self._format2lang(format))  # type: ignore
        except self._RiotException as err:
            raise err

    def _formats(self) -> tuple[str, ...]:
        return tuple(sorted(map(
            str, (getattr(self._RDFLanguages, lang)
                  for lang in dir(self._RDFLanguages)
                  if lang.startswith('strLang')))))

    def _format2lang(self, format: str | None) -> Jena.Lang:
        if format is None:
            return self._RDFLanguages.N3
        else:
            lang = self._RDFLanguages.nameToLang(format)  # type:ignore
            if lang is None:
                supported = ", ".join(self._formats())
                raise ValueError(
                    f"bad format '{format}' (supported: {supported})")
            else:
                return lang

    def query(self, text: str) -> bool | Model | dict[str, Any]:
        """Evaluates SPARQL query over model.

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

    def skolemize(self) -> None:
        """Skolemizes model."""
        it = self.model.listSubjects()
        while it.hasNext():
            res = it.nextResource()
            if res is not None and res.isAnon():
                self._ResourceUtils.renameResource(
                    res, f'urn:skolem:{res.getId()}')
