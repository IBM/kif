# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from .kif_object import KIF_Object
from .text_set import TextSet, TTextSet
from .value import Text, TText


class Descriptor(KIF_Object):
    """Entity descriptor (label, aliases, and description).

    Parameters:
       arg1: Label.
       arg2: Aliases.
       arg3: Description.
    """

    def __init__(
            self,
            arg1: Optional[TText] = None,
            arg2: Optional[TTextSet] = None,
            arg3: Optional[TText] = None
    ):
        super().__init__(arg1, arg2, arg3)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_optional_arg_text(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_text_set(arg, i, TextSet())
        elif i == 3:
            return self._preprocess_optional_arg_text(arg, i)
        else:
            return self._should_not_get_here()

    @property
    def label(self) -> Optional[Text]:
        """Descriptor label."""
        return self.get_label()

    def get_label(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets descriptor label.

        If descriptor label is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Descriptor label.
        """
        label = self.args[0]
        return label if label is not None else default

    @property
    def aliases(self) -> TextSet:
        """Descriptor aliases."""
        return self.get_aliases()

    def get_aliases(self) -> TextSet:
        """Gets descriptor aliases.

        Returns:
           Descriptor aliases.
        """
        return self.args[1]

    @property
    def description(self) -> Optional[Text]:
        """Descriptor description."""
        return self.get_description()

    def get_description(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets descriptor description.

        If descriptor description is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Descriptor description.
        """
        desc = self.args[2]
        return desc if desc is not None else default
