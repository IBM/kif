# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .typing import Any, Hashable, TypeVar

T = TypeVar('T')


class Cache:
    """Object cache.

    Parameters:
       enabled: Whether cache is enabled.
    """

    __slots__ = (
        '_cache',
        '_enabled',
    )

    _cache: dict[Hashable, dict[str, Any]]
    _enabled: bool

    def __init__(self, enabled: bool = True) -> None:
        self._cache = {}
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        """Whether cache is enabled."""
        return self.is_enabled()

    def is_enabled(self) -> bool:
        """Tests whether cache is enabled.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._enabled is True

    def enable(self) -> None:
        """Enables cache."""
        self._enabled = True

    @property
    def disabled(self) -> bool:
        """Whether cache is disabled."""
        return self.is_disabled()

    def is_disabled(self) -> bool:
        """Tests whether cache is disabled.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._enabled is False

    def disable(self) -> None:
        """Disables cache."""
        self._enabled = False

    @property
    def size(self) -> int:
        """The number of objects in cache."""
        return self.get_size()

    def get_size(self) -> int:
        """Gets the number of objects in cache.

        Returns:
           The number of objects in cache.
        """
        return len(self._cache)

    def clear(self) -> None:
        """Clears cache."""
        self._cache = {}

    def get(self, obj: Hashable, key: str) -> Any:
        """Gets the value attached to `key` of `obj` in cache.

        Parameters:
           obj: Object.
           key: Key.

        Returns:
           Value or ``None``.
        """
        if not self._enabled:
            return None
        if obj not in self._cache:
            return None
        return self._cache[obj].get(key, None)

    def set(self, obj, key: str, value: T) -> T:
        """Attaches `value` to `key` of `obj` in cache.

        Parameters:
           obj: Object.
           key: Key.

        Returns:
           `value`.
        """
        if not self._enabled:
            return value
        if obj not in self._cache:
            self._cache[obj] = {}
        self._cache[obj][key] = value
        return value

    def unset(self, obj: Hashable, key: str | None = None) -> Any:
        """Detaches value from `key` of `obj` in cache.

        If `key` is ``None``, detaches all values from `obj` and removes it
        from cache.

        Parameters:
           obj: Object.
           key: Key or ``None``.

        Returns:
           The detached value or ``None``.
        """
        if not self._enabled:
            return None
        if obj not in self._cache:
            return None
        if key is None:
            value = self._cache[obj]
            del self._cache[obj]
            return value
        if key not in self._cache[obj]:
            return None
        value = self._cache[obj][key]
        del self._cache[obj][key]
        if len(self._cache[obj]) == 0:
            del self._cache[obj]
        return value
