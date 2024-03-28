from .kif_object import KIF_Object, TCallable
from ..typing import NoReturn, Optional, TypeAlias, Union

TStringVariable: TypeAlias =\
    Union['Variable', 'TextVariable', 'StringVariable']


class Variable(KIF_Object):

    def __init__(self, name: str):
        super().__init__(name)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


class ValueVariable(Variable):
    pass


class EntityVariable(ValueVariable):
    pass


class ItemVariable(EntityVariable):
    pass


class PropertyVariable(EntityVariable):
    pass


class LexemeVariable(EntityVariable):
    pass


class DataValueVariable(ValueVariable):
    pass


class ShallowDataValueVariable(DataValueVariable):
    pass


class IRI_Variable(ShallowDataValueVariable):
    pass


class TextVariable(ShallowDataValueVariable):
    pass


class StringVariable(ShallowDataValueVariable):
    pass


class ExternalIdVariable(StringVariable):
    pass


class DeepDataValueVariable(DataValueVariable):
    pass


class QuantityVariable(DeepDataValueVariable):
    pass


class TimeValue(DeepDataValueVariable):
    pass
