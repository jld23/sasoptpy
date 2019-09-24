#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""
SAS Viya Optimization Modeling for Python (sasoptpy)
****************************************************

This file includes static methods and imports.

"""

from sasoptpy._libs import *
import sasoptpy.util

from sasoptpy.util import (
    quick_sum, expr_sum, reset, reset, reset_globals,
    flatten_frame, get_value_table,
    get_solution_table, dict_to_frame, exp_range,
    to_expression, to_definition, to_optmodel, is_linear)

from sasoptpy.structure import (inside_container, containable,
                                class_containable)

from sasoptpy.core.expression import Expression
from sasoptpy.core import (Variable, VariableGroup, Constraint, ConstraintGroup,
                           Model, Objective, Auxiliary, Symbol)
from sasoptpy.core.util import read_data

from sasoptpy.abstract import (Set, Parameter, ImplicitVar,
                               OldStatement, ParameterGroup, SetIterator,
                               SetIteratorGroup)

sasoptpy.util.load_package_globals()

import sasoptpy.config
from sasoptpy.config import Config
sasoptpy.config._load_default_config()

sasoptpy.statement_dictionary = dict()
sasoptpy.util.load_function_containers()
sasoptpy.util.load_condition_container()
from sasoptpy.actions import register_actions
register_actions()
#sasoptpy.core.util._load_function_containers()


import sasoptpy.interface
sasoptpy.mediators = dict()
sasoptpy.util.load_default_mediators()


from sasoptpy.session import Workspace

name = "sasoptpy"
__version__ = '1.0.0.dev1'
