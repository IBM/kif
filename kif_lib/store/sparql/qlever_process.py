# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id$
#
# Python bindings for QLever.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import logging
import math
import os
import pathlib
import queue
import re
import subprocess
import sys
import threading

from typing_extensions import (
    Final,
    Iterator,
    Optional,
    TextIO,
    TypeAlias,
    Union,
)

TLocation: TypeAlias = Union[pathlib.PurePath, str]

if sys.version_info < (3, 13):
    setattr(queue, 'ShutDown', Exception)

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class QLever:
    """Python bindings for QLever.

    Parameters:
       index_builder_path: Path to the QLever index builder executable.
       server_path: Path to the QLever server executable.
    """

    class Error(Exception):
        """Base class for QLever errors."""

    @classmethod
    def _get_default_index_builder_path(cls) -> TLocation:
        return os.getenv('QLEVER_INDEX_BUILDER', 'IndexBuilderMain')

    @classmethod
    def _get_default_server_path(cls) -> TLocation:
        return os.getenv('QLEVER_SERVER', 'ServerMain')

    @classmethod
    def _get_free_port(cls) -> int:
        import socketserver
        with socketserver.TCPServer(
                ('localhost', 0), None) as server:  # type: ignore
            return server.server_address[1]

    @classmethod
    def _parse_log_line(
            cls,
            line: str,
            _level_map: dict[str, int] = {
                'ERROR': logging.ERROR,
                'INFO': logging.DEBUG,
                'WARN': logging.WARNING,
            },
            _re: re.Pattern[str] = re.compile(
                r'^.*[ ](ERROR|INFO|WARN):[ ]*(.*)$')
    ) -> tuple[int, str]:
        m = _re.match(line)
        if m:
            _level, message = m.groups()
            try:
                level = _level_map[_level]
                _logger.log(level, message)
                return level, message
            except KeyError:
                pass
        raise SyntaxError

    @classmethod
    def _which_exec(
            cls,
            path: TLocation | str,
            errmsg: str
    ) -> pathlib.Path:
        import shutil
        ret = shutil.which(path, os.R_OK | os.X_OK)
        if ret is None:
            raise cls.Error(f'{errmsg}: {path}')
        else:
            return pathlib.Path(ret)

    #: The path to the IndexBuilderMain executable.
    _index_builder_path: pathlib.Path

    #: The path to the ServerMain executable.
    _server_path: pathlib.Path

    #: The QLever server port.
    _server_port: int

    #: The underlying QLever server process.
    _server_process: subprocess.Popen | None

    #: The sever logger queue.
    _server_logger_queue: queue.Queue[str]

    #: the server logger thread.
    _server_logger_thread: threading.Thread

    __slots__ = (
        '_index_builder_path',
        '_server_logger_queue',
        '_server_logger_thread',
        '_server_path',
        '_server_port',
        '_server_process',
    )

    def __init__(
            self,
            index_builder_path: TLocation | None = None,
            server_path: TLocation | None = None
    ) -> None:
        self._server_port = 0
        self._server_process = None
        self._index_builder_path = self._which_exec(
            index_builder_path or self._get_default_index_builder_path(),
            'QLever index builder executable not found')
        self._server_path = self._which_exec(
            server_path or self._get_default_server_path(),
            'QLever server executable not found')

    def __del__(self):
        self.stop()

    @property
    def server_process(self) -> subprocess.Popen:
        """The underlying QLever server process."""
        assert self._server_process is not None
        return self._server_process

    @property
    def server_process_is_running(self) -> bool:
        """Whether QLever server process is running."""
        return not self.server_process.poll()

    @property
    def server_port(self) -> int:
        """The port on which QLever server is listening."""
        return self._server_port

    def build_index(
            self,
            basename: str,
            *args: TLocation,
            data: str | None = None,
            format: str | None = None,
            index_dir: TLocation | None = None,
            parse_parallel: bool | None = None
    ) -> str:
        """Builds QLever index.

        Parameters:
           basename: Index basename.
           args: Input files process.
           data: Input data to process.
           format: Input format.
           index_dir: Index directory (output dir).
           parse_parallel: Whether to enable parallel parsing.

        Returns:
           Index basename.
        """
        cwd: Optional[pathlib.Path]
        if index_dir is not None:
            cwd = pathlib.Path(index_dir)
            cwd.mkdir(parents=True, exist_ok=True)
        else:
            cwd = None

        def it() -> Iterator[str]:
            yield str(self._index_builder_path)
            yield '-i'
            yield basename
            for arg in args:
                yield '-f'
                yield str(pathlib.Path(arg).absolute())
            if data:
                yield '-f'
                yield '-'
            if format:
                yield '-F'
                yield format
            else:
                yield '-F'
                yield 'ttl'
            if parse_parallel is not False:
                yield '-p'
                yield '1'
        run_args = list(it())
        if _logger.isEnabledFor(logging.DEBUG):
            if cwd is not None:
                _logger.debug('cd-ing to %s', cwd)
            _logger.debug(' '.join(run_args))
        ret = subprocess.run(
            run_args, capture_output=True, check=False,
            cwd=cwd, input=data, text=True)
        errmsg = None
        for line in map(str.strip, ret.stdout.splitlines()):
            try:
                level, msg = self._parse_log_line(line)
                if level == logging.ERROR:
                    errmsg = msg
                    break
            except SyntaxError:
                pass            # ignore
        if ret.returncode != 0:
            raise self.Error(errmsg or 'unknown error')
        return basename

    def start(
            self,
            basename: str,
            port: int | None = None,
            index_dir: TLocation | None = None,
            memory_max_size: float | None = None,
            default_query_timeout: int | None = None,
            throw_on_onbound_variables: bool | None = None
    ) -> int:
        """Starts QLever server.

        Parameters:
           basename: Index basename.
           port: Server port.
           index_dir: Index directory (input dir).
           memory_max_size: Memory limit for query processing (in GBs).
           default_query_timeout: Timeout in seconds.
           throw_on_onbound_variables: Whether check for unbound variables.

        Returns:
           Server port.
        """
        port = port or self._get_free_port()
        cwd: Optional[pathlib.Path]
        if index_dir is not None:
            cwd = pathlib.Path(index_dir)
        else:
            cwd = None
        if memory_max_size is not None:
            mem: int = math.ceil(max(float(memory_max_size), 2.))
        else:
            mem = 16

        def it() -> Iterator[str]:
            yield str(self._server_path)
            yield '-i'
            yield basename
            yield '-p'
            yield str(port)
            yield '--memory-max-size'
            yield f'{mem}GB'
            if default_query_timeout is not None:
                yield '--default-query-timeout'
                yield f'{max(default_query_timeout, 0)}s'
            if throw_on_onbound_variables:
                yield '--throw-on-unbound-variables'
                yield '1'
        args = list(it())
        if _logger.isEnabledFor(logging.DEBUG):
            if cwd is not None:
                _logger.debug('cd-ing to %s', cwd)
            _logger.debug(' '.join(args))
        self._server_process = subprocess.Popen(
            args, cwd=cwd, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert self._server_process.stdout is not None
        self._server_logger_queue = queue.Queue()
        self._server_logger_thread = threading.Thread(
            target=self._server_logger_enqueue,
            args=(self._server_process.stdout, self._server_logger_queue),
            daemon=True)
        self._server_logger_thread.start()
        while True:
            level, message = self._server_logger_read_line()
            if level == logging.ERROR:
                raise self.Error(message)
            if message == (
                    'The server is ready, '
                    f'listening for requests on port {port} ...'):
                break
        self._server_port = port
        assert self._server_port
        return self._server_port

    @classmethod
    def _server_logger_enqueue(
            cls,
            output: TextIO,
            queue_: queue.Queue[str]
    ) -> None:
        try:
            while True:
                queue_.put(output.readline().strip())
        except queue.ShutDown:  # type: ignore
            pass
        finally:
            output.close()

    def _server_logger_read_line(self) -> tuple[int, str]:
        while self.server_process_is_running:
            try:
                return self._parse_log_line(
                    self._server_logger_queue.get(False, 0.01))
            except SyntaxError:
                continue
            except queue.Empty:
                continue
            except queue.ShutDown:  # type: ignore
                break
        return 0, ''

    def stop(self) -> None:
        """Stops QLever server."""
        if self._server_process is not None:
            _logger.debug(
                'stopping server listening on port %d',
                self._server_port)
            if sys.version_info >= (3, 13):
                self._server_logger_queue.shutdown(immediate=True)
            self._server_process.kill()
            self._server_process.wait()
            self._server_process = None
