# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id: e2aeae285a946e14ad80b86947d342f1b0be53b4 $
#
# Python bindings for RDFox using OS pipes.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import io
import logging
import os
import pathlib
import queue
import re
import shutil
import subprocess
import threading

from typing_extensions import Final

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class RDFox:
    """Pipe-based Python bindings for RDFox.

    Parameters:
       path: Path to the RDFox executable.
    """

    class Error(Exception):
        """Base class for RDFox errors."""

    #: The underlying RDFox process.
    _process: subprocess.Popen | None

    #: Message queue.
    _queue: queue.Queue

    __slots__ = (
        '_path',
        '_process',
        '_queue',
    )

    @classmethod
    def _read_thread(
            cls,
            output: io.TextIOWrapper,
            queue: queue.Queue
    ) -> None:
        try:
            while True:
                queue.put(output.readline())
        except Exception:
            pass
        finally:
            output.close()

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
        self._queue = queue.Queue()
        ###
        # TODO: Replace daemon thread by non-blocking reads with explicit
        # join in __del__().
        ###
        threading.Thread(
            target=RDFox._read_thread,
            args=(self.process.stdout, self._queue),
            daemon=True).start()
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
            sentinel: str = '__EOF__'
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
        self._write(f'echo {sentinel}')
        output = ''
        while True:
            line = self._read()
            if line == f'{sentinel}\n':
                break
            output += line
        return output.rstrip()

    def _read(self) -> str:
        while True:
            buf = None
            try:
                buf = self._queue.get_nowait()
            except queue.Empty:
                continue
            return buf

    def _write(self, line: str) -> None:
        assert self.process.stdin is not None
        print(line, file=self.process.stdin)
        self.process.stdin.flush()

    def dstore_create(self, name: str) -> None:
        """Creates a new data store.

        Parameters:
           name: Data store name.
        """
        status = self.push(f'dstore create {name}')
        if status != f"A new data store '{name}' was created and initialized.":
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
        m = _re.match(status)
        if not m:
            raise self.Error(status)
        return m.group(1)

    def import_file(self, path: pathlib.PurePath | str) -> None:
        """Import RDF data from file.

        Parameters:
           path: File or IRI.
        """
        status = self.push(f'import {str(path)}')
        _logger.debug('%s()\n%s', self.import_file.__qualname__, status)
        if not status.startswith(f"Adding data in file '{str(path)}'."):
            raise self.Error(status)

    def import_data(self, data: str) -> None:
        """Import RDF data from string.

        Parameters:
           data: String.
        """
        status = self.push(f'import ! {data}')
        _logger.debug('%s()\n%s', self.import_data.__qualname__, status)
        if not status.startswith('Adding data.'):
            raise self.Error(status)

    def endpoint_start(self) -> None:
        """Starts the RDFox endpoint."""
        status = self.push('endpoint start')
        if not status.startswith('The REST endpoint was successfully started'):
            raise self.Error(status)

    def endpoint_stop(self) -> None:
        """Stops the RDFox endpoint."""
        status = self.push('endpoint stop')
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
        m = re.match(f'^{variable} = "([^"]+)"', status)
        if not m:
            raise self.Error(status)
        return m.group(1)
