# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id: e2aeae285a946e14ad80b86947d342f1b0be53b4 $
#
# Python bindings for RDFox using OS pipes.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import fcntl
import io
import logging
import os
import pathlib
import re
import shutil
import subprocess

from typing_extensions import Final

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class RDFox:
    """Pipe-based Python bindings for RDFox.

    Parameters:
       path: Path to the RDFox executable.
    """

    class Error(Exception):
        """Base class for RDFox errors."""

    #: The path to the RDFox executable.
    _path: pathlib.PurePath

    #: The underlying RDFox process.
    _process: subprocess.Popen | None

    __slots__ = (
        '_path',
        '_process',
    )

    def __init__(
            self,
            path: pathlib.PurePath | str | None = None,
    ) -> None:
        self._process = None
        if path is None:
            path = shutil.which(os.getenv('RDFOX', 'RDFox'))
            if path is None:
                raise RuntimeError('RDFox executable not found')
        self._path = pathlib.PurePath(path)
        self._process = subprocess.Popen(
            [self._path, 'sandbox'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        ###
        # TODO: There must be a better way to do this.
        ###
        assert self._process.stdout is not None
        flags = fcntl.fcntl(
            self._process.stdout,  # type: ignore
            fcntl.F_GETFL)
        fcntl.fcntl(
            self._process.stdout,  # type: ignore
            fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self.push()             # discard startup message

    @property
    def process(self) -> subprocess.Popen:
        """The underlying RDFox process."""
        assert self._process is not None
        return self._process

    def __del__(self):
        if self._process is not None:
            self._process.kill()
            self._process.wait()
            self._process = None

    def push(
            self,
            input: str | None = None,
            sentinel: str = '__EOF__\n'
    ) -> str:
        """Pushes input to RDFox process.

        Parameters:
           input: Input.
           sentinel: Sentinel (used to signal end of output).

        Returns:
           The RDFox process response.
        """
        if input is not None:
            self._write(input)
        self._write(f'echo {sentinel}', end='')
        output = ''
        while True:
            output += self._read()
            if output.endswith(sentinel):
                break
        return output[:-len(sentinel)].rstrip()

    def _read(self) -> str:
        assert self.process.stdout is not None
        while True:
            buf = self.process.stdout.read(io.DEFAULT_BUFFER_SIZE)
            if buf:
                return buf

    def _write(self, line: str, end: str | None = None) -> None:
        assert self.process.stdin is not None
        print(line, file=self.process.stdin, end=end)
        self.process.stdin.flush()

    def dstore_create(self, name: str) -> None:
        """Creates a new data store.

        Parameters:
           name: Data store name.
        """
        status = self.push(f'dstore create {name}')
        _logger.debug('%s()\n%s', self.dstore_create.__qualname__, status)
        if status != f"A new data store '{name}' was created and initialized.":
            raise self.Error(status)

    def dstore_delete(self, name: str) -> None:
        """Deletes data store.

        Parameters:
           name: Data store name.
        """
        status = self.push(f'dstore delete {name} force')
        _logger.debug('%s()\n%s', self.dstore_delete.__qualname__, status)
        if status != f"The data store '{name}' was deleted.":
            raise self.Error(status)

    def active(
            self,
            name: str | None,
            _re: re.Pattern = re.compile(
                r"^Data store connection '([^']\w+)' is active.$")
    ) -> str:
        """Gets or sets the active data store connection name.

        If `name` is given, sets it as the active data store connection.

        Parameters:
           name: Data store name.

        Returns:
           The active data store connection name.
        """
        if name is not None:
            status = self.push(f'active {name}')
        else:
            status = self.push('active')
        _logger.debug('%s()\n%s', self.active.__qualname__, status)
        m = _re.match(status)
        if not m:
            raise self.Error(status)
        return m.group(1)

    def clear(self, target: str | None = None) -> None:
        """Clears target.

        If `target` is not given, clears everything.

        Parameters:
           target: Target.
        """
        status = self.push(f'clear {target or ""} force')
        _logger.debug('%s()\n%s', self.clear.__qualname__, status)
        if not status.endswith('has been cleared as specified.'):
            raise self.Error(status)

    def import_file(self, path: pathlib.PurePath | str) -> None:
        """Imports RDF data from file.

        Parameters:
           path: File path or IRI.
        """
        status = self.push(f'import "{str(path)}"')
        _logger.debug('%s()\n%s', self.import_file.__qualname__, status)
        if not status.startswith(f"Adding data in file '{str(path)}'."):
            raise self.Error(status)

    def import_data(self, data: str) -> None:
        """Imports RDF data from string.

        Parameters:
           data: String.
        """
        import tempfile
        with tempfile.NamedTemporaryFile(
                prefix='rdfox_pipe_', mode='w', delete=True) as temp:
            temp.write(data)
            temp.flush()
            self.import_file(temp.name)

    def export(self, path: pathlib.Path | str, *args: str) -> None:
        """Exports RDF data to file.

        If `format` is not given, assumes "text/turtle".

        Parameters:
           path: File path.
           args: Other arguments.
        """
        cmd = f'export "{str(path)}"'
        if args is not None:
            cmd += ' ' + ' '.join(args)
        status = self.push(cmd)
        _logger.debug('%s()\n%s', self.export.__qualname__, status)
        if not status.startswith('Exporting data into file'):
            raise self.Error(status)

    def endpoint_start(self) -> None:
        """Starts the RDFox endpoint."""
        status = self.push('endpoint start')
        _logger.debug('%s()\n%s', self.endpoint_start.__qualname__, status)
        if not status.startswith('The REST endpoint was successfully started'):
            raise self.Error(status)

    def endpoint_stop(self) -> None:
        """Stops the RDFox endpoint."""
        status = self.push('endpoint stop')
        _logger.debug('%s()\n%s', self.endpoint_stop.__qualname__, status)
        if status != 'The REST endpoint was successfully stopped.':
            raise self.Error(status)

    def set(self, variable: str, value: str | None = None) -> str:
        """Gets or sets variable.

        If `value` is given, sets `variable` to `value`.

        Parameters:
           variable: Variable.
           value: Value.

        Returns:
           The value of `variable`.
        """
        if value is not None:
            status = self.push(f'set {variable} {value}')
        else:
            status = self.push(f'set {variable}')
        _logger.debug('%s()\n%s', self.set.__qualname__, status)
        m = re.match(f'^{variable} = "([^"]+)"', status)
        if not m:
            raise self.Error(status)
        return m.group(1)
