
from collections import OrderedDict

from .parameter import Parameter

import sasoptpy

class ParameterGroup:

    @sasoptpy.class_containable
    def __init__(self, *index_key, name, init=None, value=None, ptype=None):
        self._key = list(index_key)
        self._name = name
        self._init = init
        self._value = value
        if ptype is None:
            ptype = sasoptpy.NUM
        self._ptype = ptype
        self._objorder = sasoptpy.util.get_creation_id()
        self._shadows = OrderedDict()

    def get_name(self):
        return self._name

    def get_element_name(self, key):
        keyname = sasoptpy.util.package_utils._to_sas_string(key)
        return '{}[{}]'.format(self.get_name(), keyname)

    def __getitem__(self, key):
        if key in self._shadows:
            return self._shadows[key]
        else:
            pv = Parameter(name=None)
            pv.set_parent(self, key=key)
            self._shadows[key] = pv
            return pv

    def __setitem__(self, key, value):
        k = self[key]
        k.set_value(value)
        sasoptpy.abstract.Assignment(self._shadows[key], value)

    def _defn(self):
        s = '{} {}'.format(self._ptype, self.get_name())
        s += ' {{{}}}'.format(', '.join(sasoptpy.to_expression(k) for k in self._key))
        if self._init is not None:
            s += ' init {}'.format(self._init)
        elif self._value is not None:
            s += ' = {}'.format(self._value)
        s += ';'
        return s

    def _expr(self):
        return self.get_name()
