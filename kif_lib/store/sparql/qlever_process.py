# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id: 3706d9f5c61235308277a8a76e9edc0c7bbfcd0f $
#
# Python bindings for QLever.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

import io
import logging
import os
import pathlib
import re
import subprocess

from typing_extensions import Final, Iterator, Optional, TypeAlias

TPath: TypeAlias = pathlib.PurePath | str

_logger: Final[logging.Logger] = logging.getLogger(__name__)


class QLever:
    """Python bindings QLever.

    Parameters:
       index_builder_path: Path to the QLever index builder executable.
       server_path: Path to the QLever server executable.
    """

    class Error(Exception):
        """Base class for QLever errors."""

    @classmethod
    def _get_default_index_builder_path(cls) -> str:
        return os.getenv('QLEVER_INDEX_BUILDER', 'IndexBuilderMain')

    @classmethod
    def _get_default_server_path(cls) -> str:
        return os.getenv('QLEVER_SERVER', 'ServerMain')

    @classmethod
    def _get_free_port(cls) -> int:
        import socketserver
        with socketserver.TCPServer(
                ('localhost', 0), None) as server:  # type: ignore
            return server.server_address[1]

    @classmethod
    def _parse_log(
            cls,
            buf: str,
            _level_map: dict[str, int] = {
                'ERROR': logging.ERROR,
                'INFO': logging.DEBUG,
                'WARN': logging.WARNING,
            },
            _re: re.Pattern[str] = re.compile(
                r'^.*[ ](ERROR|INFO|WARN):[ ]*(.*)$')
    ) -> str | None:
        for line in buf.splitlines():
            m = _re.match(line)
            if m:
                level, msg = m.groups()
                _logger.log(_level_map[level], msg)
                if level == 'ERROR':
                    return msg
        return None

    #: The path to the IndexBuilderMain executable.
    _index_builder_path: pathlib.Path

    #: The path to the ServerMain executable.
    _server_path: pathlib.Path

    #: The QLever server port.
    _server_port: int

    #: The underlying QLever server process.
    _server_process: subprocess.Popen | None

    __slots__ = (
        '_index_builder_path',
        '_server_path',
        '_server_port',
        '_server_process',
    )

    def __init__(
            self,
            index_builder_path: TPath | None = None,
            server_path: TPath | None = None
    ) -> None:
        self._index_builder_path = self._which_exec(
            index_builder_path or self._get_default_index_builder_path(),
            'QLever index builder executable not found')
        self._server_path = self._which_exec(
            server_path or self._get_default_server_path(),
            'QLever server executable not found')
        self._server_port = 0
        self._server_process = None

    def _which_exec(self, path: TPath, errmsg: str) -> pathlib.Path:
        import shutil
        ret = shutil.which(path, os.R_OK | os.X_OK)
        if ret is None:
            raise self.Error(f'{errmsg}: {path}')
        else:
            return pathlib.Path(ret)

    @property
    def server_process(self) -> subprocess.Popen:
        """The underlying QLever server process."""
        assert self._server_process is not None
        return self._server_process

    def build_index(
            self,
            basename: str,
            *args: TPath,
            data: str | None = None,
            format: str | None = None,
            index_dir: TPath | None = None,
            parse_parallel: bool | None = None
    ) -> str:
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
                path = pathlib.Path(arg)
                if not path.exists():
                    raise FileNotFoundError(path)
                yield '-f'
                yield str(path.absolute())
            if data:
                yield '-f'
                yield '-'
            if format:
                yield '-F'
                yield format
            else:
                yield '-F'
                yield 'ttl'
            if parse_parallel:
                yield '-p'
                yield '1'
        ret = subprocess.run(
            list(it()), capture_output=True, check=False,
            cwd=cwd, input=data, text=True)
        errmsg = self._parse_log(ret.stdout)
        if ret.returncode != 0:
            assert errmsg is not None
            raise self.Error(errmsg)
        return basename

    def start(
            self,
            basename: str,
            port: int | None = None,
            index_dir: TPath | None = None
    ) -> int:
        import fcntl
        port = port or self._get_free_port()
        cwd: Optional[pathlib.Path]
        if index_dir is not None:
            cwd = pathlib.Path(index_dir)
        else:
            cwd = None
        self._server_process = subprocess.Popen(
            [self._server_path, '-i', basename, '-p', str(port)],
            cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert self._server_process.stdout is not None
        flags = fcntl.fcntl(
            self._server_process.stdout,  # type: ignore
            fcntl.F_GETFL)
        fcntl.fcntl(
            self._server_process.stdout,  # type: ignore
            fcntl.F_SETFL, flags | os.O_NONBLOCK)
        buf, success = '', False
        while not self.server_process.poll():
            buf += self._read()
            if self.server_process.poll():
                break
            if buf.endswith(f'listening for requests on port {port} ...\n'):
                success = True
                break
        errmsg = self._parse_log(buf)
        if not success:
            raise self.Error(
                f"Failed to start QLever server: {errmsg or 'unknown error'}")
        self._server_port = port
        assert self._server_port
        return self._server_port

    def _read(self) -> str:
        assert self.server_process.stdout is not None
        while not self.server_process.poll():
            buf = self.server_process.stdout.read(io.DEFAULT_BUFFER_SIZE)
            if buf:
                return buf
        return ''
