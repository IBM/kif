# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import Any, Callable, cast, Optional, override, Self, Union
from ..set import TSnakSet
from ..snak import TSnak
from ..value import Entity, TEntity, Value
from .fingerprint import Fingerprint

TEntityFingerprint = Union['EntityFingerprint', TEntity, TSnak, TSnakSet]


class EntityFingerprint(Fingerprint):
    """Entity fingerprint.

    Parameters:
       entity_spec: Entity or snak set.
    """

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        else:
            fp = Fingerprint.check(arg, function or cls.check, name, position)
            if isinstance(fp[0], Value):
                return cls(Entity.check(
                    fp[0], function or cls.check, name, position))
            else:
                return cls(fp[0])

    def __init__(self, entity_spec: TEntityFingerprint):
        super().__init__(entity_spec)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            arg = Fingerprint._static_preprocess_arg(self, arg, i)
            if isinstance(arg, Value):
                return Entity.check(arg, type(self), None, i)
            else:
                return arg
        else:
            raise self._should_not_get_here()

    @property
    def entity(self) -> Optional[Entity]:
        """The entity of fingerprint."""
        return self.get_entity()

    def get_entity(
            self,
            default: Optional[Entity] = None
    ) -> Optional[Entity]:
        """Gets the entity of fingerprint.

        If the entity is ``None``, returns `default`.

        Parameters:
           default: Default entity.

        Returns:
           Entity.
        """
        return cast(Optional[Entity], self.get_value(default))
