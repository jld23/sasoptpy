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
Model includes :class:`Model` class, the main structure of an opt. model

"""


from collections import OrderedDict
import inspect
from math import inf
from types import GeneratorType
import warnings

import numpy as np
import pandas as pd

import sasoptpy
import sasoptpy.util
from sasoptpy.core import (Expression, Objective, Variable, VariableGroup,
                           Constraint, ConstraintGroup)


class Model:
    """
    Creates an optimization model

    Parameters
    ----------
    name : string
        Name of the model
    session : :class:`swat.cas.connection.CAS` or \
:class:`saspy.SASsession`, optional
        CAS or SAS Session object

    Examples
    --------

    >>> from swat import CAS
    >>> import sasoptpy as so
    >>> s = CAS('cas.server.address', port=12345)
    >>> m = so.Model(name='my_model', session=s)
    NOTE: Initialized model my_model

    >>> mip = so.Model(name='mip')
    NOTE: Initialized model mip
    """

    @sasoptpy.class_containable
    def __init__(self, name=None, session=None):
        self._name = name
        self._objorder = sasoptpy.util.get_creation_id()
        self._session = session
        self._variables = []
        self._constraints = []
        self._vargroups = []
        self._congroups = []
        self._objective = Objective(0, name=name+'_obj', internal=True)
        self._multiobjs = []
        self._variableDict = {}
        self._constraintDict = {}
        self._soltime = 0
        self._objval = None
        self._status = ''
        self._castablename = None
        self._mpsmode = 0
        self._problemSummary = None
        self._solutionSummary = None
        self._primalSolution = None #pd.DataFrame()
        self._dualSolution = None #pd.DataFrame()
        self._milp_opts = {}
        self._lp_opts = {}
        self._sets = []
        self._parameters = []
        self._impvars = []
        self._statements = []
        self._postsolve_statements = []
        self.response = None

        print('NOTE: Initialized model {}.'.format(name))

    def __eq__(self, other):
        if not isinstance(other, sasoptpy.Model):
            warnings.warn('Cannot compare Model object with {}'.
                          format(type(other)), RuntimeWarning, stacklevel=2)
            return False
        return super().__eq__(other)

    def get_name(self):
        return self._name

    def add(self, object):
        self.include(object)

    def add_variable(self, name, vartype=None,
                     lb=None, ub=None, init=None):
        """
        Adds a new variable to the model

        New variables can be created via this method or existing variables
        can be added to the model.

        Parameters
        ----------
        name : string, optional
            Name of the variable to be created
        vartype : string, optional
            Type of the variable, either 'BIN', 'INT' or 'CONT'
        lb : float, optional
            Lower bound of the variable
        ub : float, optional
            Upper bound of the variable
        init : float, optional
            Initial value of the variable

        Returns
        -------
        var : Variable
            Variable that is added to the model

        Examples
        --------
        Adding a variable on the fly

        >>> m = so.Model(name='demo')
        >>> x = m.add_variable(name='x', vartype=so.INT, ub=10, init=2)
        >>> print(repr(x))
        NOTE: Initialized model demo
        sasoptpy.Variable(name='x', lb=0, ub=10, init=2, vartype='INT')

        Adding an existing variable to a model

        >>> y = so.Variable(name='y', vartype=so.BIN)
        >>> m = so.Model(name='demo')
        >>> m.include(y)

        Notes
        -----
        * If argument *var* is not None, then all other arguments are ignored.
        * A generic variable name is generated if name argument is None.

        See also
        --------
        :class:`Variable`, :func:`Model.include`
        """

        var = Variable(name, vartype, lb, ub, init)
        self.include(var)
        return var

    def add_variables(self, *argv, name=None,
                      vartype=None,
                      lb=None, ub=None, init=None):
        """
        Adds a group of variables to the model

        Parameters
        ----------
        argv : list, dict, :class:`pandas.Index`
            Loop index for variable group
        name : string, optional
            Name of the variables
        vartype : string, optional
            Type of variables, `BIN`, `INT`, or `CONT`
        lb : list, dict, :class:`pandas.Series`
            Lower bounds of variables
        ub : list, dict, :class:`pandas.Series`
            Upper bounds of variables
        init : list, dict, :class:`pandas.Series`
            Initial values of variables

        See also
        --------
        :class:`VariableGroup`, :meth:`Model.include`

        Notes
        -----
        If `vg` argument is passed, all other arguments are ignored.

        Examples
        --------

        >>> production = m.add_variables(PERIODS, vartype=so.INT,
                                        name='production', lb=min_production)
        >>> print(production)
        >>> print(repr(production))
        Variable Group (production) [
          [Period1: production['Period1',]]
          [Period2: production['Period2',]]
          [Period3: production['Period3',]]
        ]
        sasoptpy.VariableGroup(['Period1', 'Period2', 'Period3'],
        name='production')

        """

        vg = VariableGroup(*argv, name=name, vartype=vartype, lb=lb, ub=ub,
                           init=init)
        self.include(vg)
        return vg

    @sasoptpy.containable
    def add_constraint(self, c, name):
        """
        Adds a single constraint to the model

        Parameters
        ----------
        c : Constraint
            Constraint to be added to the model
        name : string, optional
            Name of the constraint

        Returns
        -------
        c : Constraint
            Reference to the constraint

        Examples
        --------

        >>> x = m.add_variable(name='x', vartype=so.INT, lb=0, ub=5)
        >>> y = m.add_variables(3, name='y', vartype=so.CONT, lb=0, ub=10)
        >>> c1 = m.add_constraint(x + y[0] >= 3, name='c1')
        >>> print(c1)
         x  +  y[0]  >=  3

        >>> c2 = m.add_constraint(x - y[2] == [4, 10], name='c2')
        >>> print(c2)
         -  y[2]  +  x  =  [4, 10]

        See also
        --------
        :class:`Constraint`, :meth:`Model.include`

        """

        if ((c._direction == 'L' and c._linCoef['CONST']['val'] == -inf) or
           (c._direction == 'G' and c._linCoef['CONST']['val'] == inf)):
            raise ValueError("Invalid constant value for the constraint type")

        if c._name is None:
            c.set_name(name)
            c.set_permanent()

        self.include(c)
        return c

    def add_constraints(self, argv, name=None):
        """
        Adds a set of constraints to the model

        Parameters
        ----------
        argv : Generator-type object
            List of constraints as a Generator-type object
        name : string, optional
            Name for the constraint group and individual constraint prefix

        Returns
        -------
        cg : ConstraintGroup
            Reference to the ConstraintGroup

        Examples
        --------

        >>> x = m.add_variable(name='x', vartype=so.INT, lb=0, ub=5)
        >>> y = m.add_variables(3, name='y', vartype=so.CONT, lb=0, ub=10)
        >>> c = m.add_constraints((x + 2 * y[i] >= 2 for i in [0, 1, 2]),
                                  name='c')
        >>> print(c)
        Constraint Group (c) [
          [0:  2.0 * y[0]  +  x  >=  2]
          [1:  2.0 * y[1]  +  x  >=  2]
          [2:  2.0 * y[2]  +  x  >=  2]
        ]

        >>> t = m.add_variables(3, 4, name='t')
        >>> ct = m.add_constraints((t[i, j] <= x for i in range(3)
                                   for j in range(4)), name='ct')
        >>> print(ct)
        Constraint Group (ct) [
          [(0, 0):  -  x  +  t[0, 0]  <=  0]
          [(0, 1):  t[0, 1]  -  x  <=  0]
          [(0, 2):  -  x  +  t[0, 2]  <=  0]
          [(0, 3):  t[0, 3]  -  x  <=  0]
          [(1, 0):  t[1, 0]  -  x  <=  0]
          [(1, 1):  t[1, 1]  -  x  <=  0]
          [(1, 2):  -  x  +  t[1, 2]  <=  0]
          [(1, 3):  -  x  +  t[1, 3]  <=  0]
          [(2, 0):  -  x  +  t[2, 0]  <=  0]
          [(2, 1):  t[2, 1]  -  x  <=  0]
          [(2, 2):  t[2, 2]  -  x  <=  0]
          [(2, 3):  t[2, 3]  -  x  <=  0]
        ]

        See also
        --------
        :class:`ConstraintGroup`, :meth:`Model.include`

        """

        if type(argv) == list or type(argv) == GeneratorType:
            cg = ConstraintGroup(argv, name=name)
            self.include(cg)
            return cg
        elif sasoptpy.core.util.is_constraint(argv):
            warnings.warn(
                'Use add_constraint method for adding single constraints',
                UserWarning)
            c = self.add_constraint(argv, name=name)
            return c

    def add_set(self, name, init=None, value=None, settype=None):
        """
        Adds a set to the model

        Parameters
        ----------
        name : string, optional
            Name of the set
        init : :class:`Set`, optional
            Initial value of the set
        value : list, float, optional
            Exact value of the set
        settype : list, optional
            Types of the set, a list consists of 'num' and 'str' values

        Examples
        --------

        >>> I = m.add_set(name='I')
        >>> print(I._defn())
        set I;

        >>> J = m.add_set(name='J', settype=['str'])
        >>> print(J._defn())
        set <str> J;

        >>> N = m.add_parameter(name='N', init=4)
        >>> K = m.add_set(name='K', init=so.exp_range(1, N))
        >>> print(K._defn())
        set K = 1..N;

        """
        new_set = sasoptpy.abstract.Set(name, init=init, value=value,
                                        settype=settype)
        self.include(new_set)
        return new_set

    def add_parameter(self, *argv, name=None, init=None, value=None, p_type=None):
        """
        Adds a parameter to the model

        Parameters
        ----------
        argv : :class:`Set`, optional
            Key set of the parameter
        name : string, optional
            Name of the parameter
        init : float or expression, optional
            Initial value of the parameter
        p_type : string, optional
            Type of the parameter, 'num' for floats or 'str' for strings

        Examples
        --------

        >>> I = m.add_set(name='I')
        >>> a = m.add_parameter(I, name='a', init=5)
        >>> print(a._defn())
        num a {I} init 5 ;

        """
        if len(argv) == 0:
            p = sasoptpy.abstract.Parameter(
                name, init=init, value=value, ptype=p_type)
            self.include(p)
            return p
        else:
            keylist = list(argv)
            p = sasoptpy.abstract.ParameterGroup(keylist, name=name, init=init,
                                                 value=value, ptype=p_type)
            self.include(p)
            return p

    def add_implicit_variable(self, argv=None, name=None):
        """
        Adds an implicit variable to the model

        Parameters
        ----------
        argv : Generator-type object
            Generator object where each item is an entry
        name : string, optional
            Name of the implicit variable

        Examples
        --------

        >>> x = m.add_variables(range(5), name='x')
        >>> y = m.add_implicit_variable((
        >>>     x[i] + 2 * x[i+1] for i in range(4)), name='y')
        >>> print(y[2])
        x[2] + 2 * x[3]

        >>> I = m.add_set(name='I')
        >>> z = m.add_implicit_variable((x[i] * 2 + 2 for i in I), name='z')
        >>> print(z._defn())
        impvar z {i_1 in I} = 2 * x[i_1] + 2;


        Notes
        -----

        - Based on whether generated by a regular expression or an abstract
          one, implicit variables may appear in generated OPTMODEL codes.

        """
        iv = sasoptpy.abstract.ImplicitVar(argv=argv, name=name)
        self.include(iv)
        return iv

    def add_statement(self, statement, after_solve=None):
        """
        Adds a PROC OPTMODEL statement to the model

        Parameters
        ----------
        statement : Expression or string
            Statement object

        Examples
        --------

        >>> I = m.add_set(name='I')
        >>> x = m.add_variables(I, name='x', vartype=so.INT)
        >>> a = m.add_parameter(I, name='a')
        >>> c = m.add_constraints((x[i] <= 2 * a[i] for i in I), name='c')
        >>> m.add_statement('print x;', after_solve=True)
        >>> print(m.to_optmodel())
        proc optmodel;
        min m_obj = 0;
        set I;
        var x {I} integer >= 0;
        num a {I};
        con c {i_1 in I} : x[i_1] - 2.0 * a[i_1] <= 0;
        solve;
        print _var_.name _var_.lb _var_.ub _var_ _var_.rc;
        print _con_.name _con_.body _con_.dual;
        print x;
        quit;


        Notes
        -----

        - If the statement string includes 'print', then it is automatically
          placed after solve.
        - The first parameter, `statement` could be a Statement object when internally used.

        """
        if isinstance(statement, sasoptpy.abstract.Statement):
            self._save_statement(statement, after_solve)
        elif isinstance(statement, str):
            s = sasoptpy.abstract.LiteralStatement(statement)
            self._save_statement(s, after_solve)

    def add_postsolve_statement(self, statement):
        if isinstance(statement, sasoptpy.abstract.Statement):
            self._save_statement(statement, after_solve=True)
        elif isinstance(statement, str):
            s = sasoptpy.abstract.LiteralStatement(statement)
            self._save_statement(s, after_solve=True)

    def _save_statement(self, st, after_solve=None):
        if after_solve is None or after_solve is False:
            self._statements.append(st)
        else:
            self._postsolve_statements.append(st)

    def drop_variable(self, variable):
        """
        Drops a variable from the model

        Parameters
        ----------
        variable : Variable
            The variable to be dropped from the model

        Examples
        --------

        >>> x = m.add_variable(name='x')
        >>> y = m.add_variable(name='y')
        >>> print(m.get_variable('x'))
         x
        >>> m.drop_variable(x)
        >>> print(m.get_variable('x'))
        None

        See also
        --------
        :func:`Model.drop_variables`
        :func:`Model.drop_constraint`
        :func:`Model.drop_constraints`

        """
        for i, v in enumerate(self._variables):
            if id(variable) == id(v):
                del self._variableDict[variable.get_name()]
                del self._variables[i]
                return

    @sasoptpy.containable
    def drop_constraint(self, constraint):
        """
        Drops a constraint from the model

        Parameters
        ----------
        constraint : Constraint
            The constraint to be dropped from the model

        Examples
        --------

        >>> c1 = m.add_constraint(2 * x + y <= 15, name='c1')
        >>> print(m.get_constraint('c1'))
        2 * x  +  y  <=  15
        >>> m.drop_constraint(c1)
        >>> print(m.get_constraint('c1'))
        None

        See also
        --------
        :func:`Model.drop_constraints`
        :func:`Model.drop_variable`
        :func:`Model.drop_variables`

        """
        try:
            del self._constraintDict[constraint.get_name()]
            for i, c in enumerate(self._constraints):
                if c.get_name() == constraint.get_name():
                    deleted_constraint = self._constraints[i]
                    del self._constraints[i]

                    if deleted_constraint._parent is not None:
                        if deleted_constraint._parent in self._congroups:
                            self.add_statement(
                                sasoptpy.abstract.DropStatement.model_drop_constraint(
                                    self, deleted_constraint))
        except KeyError:
            raise KeyError('Given constraint is not part of the model')

    def drop_variables(self, variables):
        """
        Drops a variable group from the model

        Parameters
        ----------
        variables : VariableGroup
            The variable group to be dropped from the model

        Examples
        --------

        >>> x = m.add_variables(3, name='x')
        >>> print(m.get_variables())
        [sasoptpy.Variable(name='x_0',  vartype='CONT'),
         sasoptpy.Variable(name='x_1',  vartype='CONT')]
        >>> m.drop_variables(x)
        >>> print(m.get_variables())
        []

        See also
        --------
        :func:`Model.drop_variable`
        :func:`Model.drop_constraint`
        :func:`Model.drop_constraints`

        """
        for v in variables:
            self.drop_variable(v)
        if variables in self._vargroups:
            self._vargroups.remove(variables)

    def drop_constraints(self, constraints):
        """
        Drops a constraint group from the model

        Parameters
        ----------
        constraints : ConstraintGroup
            The constraint group to be dropped from the model

        Examples
        --------

        >>> c1 = m.add_constraints((x[i] + y <= 15 for i in [0, 1]), name='c1')
        >>> print(m.get_constraints())
        [sasoptpy.Constraint( x[0]  +  y  <=  15, name='c1_0'),
         sasoptpy.Constraint( x[1]  +  y  <=  15, name='c1_1')]
        >>> m.drop_constraints(c1)
        >>> print(m.get_constraints())
        []

        See also
        --------
        :func:`Model.drop_constraints`
        :func:`Model.drop_variable`
        :func:`Model.drop_variables`

        """
        if constraints in self._congroups:
            self._congroups.remove(constraints)
        for c in constraints:
            self.drop_constraint(c)

    def include(self, *argv):
        """
        Adds existing variables and constraints to a model

        Parameters
        ----------
        argv : :class:`Model`, :class:`Variable`, :class:`Constraint`,\
            :class:`VariableGroup`, :class:`ConstraintGroup`,\
            :class:`Set`, :class:`Parameter`, :class:`Statement`,\
            :class:`ImplicitVar`
            Objects to be included in the model

        Examples
        --------

        Adding an existing variable

        >>> x = so.Variable(name='x', vartype=so.CONT)
        >>> m.include(x)

        Adding an existing constraint

        >>> c1 = so.Constraint(x + y <= 5, name='c1')
        >>> m.include(c1)

        Adding an existing set of variables

        >>> z = so.VariableGroup(3, 5, name='z', ub=10)
        >>> m.include(z)

        Adding an existing set of constraints

        >>> c2 = so.ConstraintGroup((x + 2 * z[i, j] >= 2 for i in range(3)
                                    for j in range(5)), name='c2')
        >>> m.include(c2)

        Adding an existing model (including all of its elements)

        >>> new_model = so.Model(name='new_model')
        >>> new_model.include(m)

        Notes
        -----
        * Including a model causes all variables and constraints inside the
          original model to be included.

        """

        include_methods = {
            Variable: self._include_variable,
            VariableGroup: self._include_vargroup,
            Constraint: self._include_constraint,
            ConstraintGroup: self._include_congroup,
            Objective: self._set_objective,
            sasoptpy.Set: self._include_set,
            sasoptpy.Parameter: self._include_parameter,
            sasoptpy.ParameterGroup: self._include_parameter_group,
            sasoptpy.abstract.LiteralStatement: self._include_statement,
            sasoptpy.ImplicitVar: self._include_expdict,
            sasoptpy.abstract.ReadDataStatement: self._include_statement,
            sasoptpy.abstract.DropStatement: self._include_statement,
            list: self.include,
            Model: self._include_model
        }

        for c in argv:
            meth = include_methods.get(type(c))
            if any(isinstance(c, i) for i in [Variable, VariableGroup, Constraint, ConstraintGroup, Objective]):
                if sasoptpy.container is not None:
                    if c._objorder > self._objorder:
                        raise ReferenceError('Object {} should be defined before Model {} inside a Workspace'.format(
                            c._expr(), self.get_name()
                    ))
            if meth is not None:
                meth(c)

    def _include_variable(self, var):
        if sasoptpy.core.util.has_parent(var):
            return
        self._variables.append(var)
        self._variableDict[var.get_name()] = var

    def _include_vargroup(self, vg):
        for i in vg:
           self._variables.append(i)
           self._variableDict[i.get_name()] = i
        self._vargroups.append(vg)

    def _include_constraint(self, con):
        if sasoptpy.core.util.has_parent(con):
            return
        self._constraints.append(con)
        self._constraintDict[con.get_name()] = con

    def _include_congroup(self, cg):
        for i in cg:
            self._constraints.append(i)
            self._constraintDict[i.get_name()] = i
        self._congroups.append(cg)

    def _set_objective(self, ob):
        self._objective = ob

    def _include_set(self, st):
        self._sets.append(st)

    def _include_parameter(self, p):
        self._parameters.append(p)

    def _include_parameter_group(self, pg):
        self._parameters.append(pg)

    def _include_statement(self, os):
        self._save_statement(os)

    def _include_expdict(self, ed):
        self._impvars.append(ed)

    def _include_model(self, model):
        self._sets.extend(s for s in model._sets)
        self._parameters.extend(s for s in model._parameters)
        self._statements.extend(s for s in model._statements)
        self._postsolve_statements.extend(s for s in model._postsolve_statements)
        self._impvars.extend(s for s in model._impvars)
        for s in model._vargroups:
            self._include_vargroup(s)
        for s in model._variables:
            self._include_variable(s)
        for s in model._congroups:
            self._include_congroup(s)
        for s in model._constraints:
            self._include_constraint(s)
        self._objective = model._objective

    def drop(self, obj):
        if isinstance(obj, sasoptpy.VariableGroup):
            self.drop_variables(obj)
        elif isinstance(obj, sasoptpy.Variable):
            self.drop_variable(obj)
        elif isinstance(obj, sasoptpy.ConstraintGroup):
            self.drop_constraints(obj)
        elif isinstance(obj, sasoptpy.Constraint):
            self.drop_constraint(obj)
        elif isinstance(obj, sasoptpy.Set):
            if obj in self._sets:
                self._sets.remove(obj)
        elif isinstance(obj, sasoptpy.Parameter) or\
             isinstance(obj, sasoptpy.ParameterGroup):
            if obj in self._parameters:
                self._parameters.remove(obj)
        elif isinstance(obj, sasoptpy.abstract.Statement):
            if obj in self._statements:
                self._statements.remove(obj)

    def set_objective(self, expression, name, sense=None):
        """
        Sets the objective function for the model

        Parameters
        ----------
        expression : Expression
            The objective function as an Expression
        sense : string, optional
            Objective value direction, 'MIN' or 'MAX'
        name : string, optional
            Name of the objective value

        Returns
        -------
        objective : Expression
            Objective function as an :class:`Expression` object

        Examples
        --------

        >>> profit = so.Expression(5 * sales - 2 * material, name='profit')
        >>> m.set_objective(profit, so.MAX)
        >>> print(m.get_objective())
         -  2.0 * material  +  5.0 * sales

        >>> m.set_objective(4 * x - 5 * y, name='obj')
        >>> print(repr(m.get_objective()))
        sasoptpy.Expression(exp =  4.0 * x  -  5.0 * y , name='obj')

        >>> f1 = m.set_objective(2 * x + y, sense=so.MIN, name='f1')
        >>> f2 = m.append_objective( (x - y) ** 2, sense=so.MIN, name='f2')
        >>> print(m.to_optmodel(options={'with': 'lso', 'obj': (f1, f2)}))
        proc optmodel;
        var x;
        var y;
        min f1 = 2 * x + y;
        min f2 = (x - y) ^ (2);
        solve with lso obj (f1 f2);
        print _var_.name _var_.lb _var_.ub _var_ _var_.rc;
        print _con_.name _con_.body _con_.dual;
        quit;

        Notes
        -----
        - Default objective sense is minimization (MIN)
        - This method replaces the existing objective of the model. When working with multiple objectives, use the
          `multiobj` parameter and use 'obj' option in :meth:`Model.solve` and :meth:`Model.to_optmodel` methods.

        """

        obj = Objective(expression, sense=sense, name=name)
        self._objective = obj
        return self._objective

    def append_objective(self, expression, name, sense=None):
        obj = Objective(expression, name=name, sense=sense)
        self._multiobjs.append(obj)
        return obj


    def get_objective(self):
        """
        Returns the objective function as an :class:`Expression` object

        Returns
        -------
        objective : Expression
            Objective function

        Examples
        --------

        >>> m.set_objective(4 * x - 5 * y, name='obj')
        >>> print(repr(m.get_objective()))
        sasoptpy.Expression(exp =  4.0 * x  -  5.0 * y , name='obj')

        """
        return self._objective

    def get_all_objectives(self):
        all_objs = list(self._multiobjs)
        all_objs.append(self._objective)
        return sorted(all_objs, key=lambda i: i._objorder)

    def get_objective_value(self):
        """
        Returns the optimal objective value, if it exists

        Returns
        -------
        objective_value : float
            Objective value at current solution

        Examples
        --------

        >>> m.solve()
        >>> print(m.get_objective_value())
        42.0

        Notes
        -----

        - This method should be used for getting the objective value after
          solve. Using :code:`m.get_objective().get_value()` actually evaluates
          the expression using optimal variable values. This may not be
          available for nonlinear expressions.

        """
        if self._objval:
            return sasoptpy.util.get_in_digit_format(self._objval)
        else:
            return self.get_objective().get_value()

    def set_objective_value(self, value):
        self._objval = value

    def get_constraint(self, name):
        """
        Returns the reference to a constraint in the model

        Parameters
        ----------
        name : string
            Name of the constraint requested

        Returns
        -------
        constraint : Constraint
            Reference to the constraint

        Examples
        --------

        >>> m.add_constraint(2 * x + y <= 15, name='c1')
        >>> print(m.get_constraint('c1'))
        2.0 * x  +  y  <=  15

        """
        if name in self._constraintDict:
            return self._constraintDict[name]
        else:
            return self.get_constraint_group(name)

    def get_constraint_group(self, name):
        for i in self._congroups:
            if i.get_name() == name:
                return i
        return None

    def get_constraints(self):
        """
        Returns a list of constraints in the model

        Returns
        -------
        constraints : list
            A list of Constraint objects

        Examples
        --------

        >>> m.add_constraint(x[0] + y <= 15, name='c1')
        >>> m.add_constraints((2 * x[i] - y >= 1 for i in [0, 1]), name='c2')
        >>> print(m.get_constraints())
        [sasoptpy.Constraint( x[0]  +  y  <=  15, name='c1'),
         sasoptpy.Constraint( 2.0 * x[0]  -  y  >=  1, name='c2_0'),
         sasoptpy.Constraint( 2.0 * x[1]  -  y  >=  1, name='c2_1')]

        """
        return self._constraints

    def get_constraints_dict(self):
        return self._constraintDict

    def get_grouped_constraints(self):
        all_cons = [*self._congroups, *self._constraints]
        all_cons = sorted(all_cons, key=lambda i: i._objorder)
        grouped_cons = OrderedDict()
        for i in all_cons:
            if sasoptpy.core.util.has_parent(i):
                continue
            grouped_cons[i.get_name()] = i
        return grouped_cons

    def get_variable(self, name):
        """
        Returns the reference to a variable in the model

        Parameters
        ----------
        name : string
            Name or key of the variable requested

        Returns
        -------
        variable : Variable
            Reference to the variable

        Examples
        --------

        >>> m.add_variable(name='x', vartype=so.INT, lb=3, ub=5)
        >>> var1 = m.get_variable('x')
        >>> print(repr(var1))
        sasoptpy.Variable(name='x', lb=3, ub=5, vartype='INT')

        """
        variables = self.get_variable_dict()
        safe_name = name.replace('\'', '')
        if name in variables:
            return variables[name]
        elif safe_name in variables:
            return variables[safe_name]
        else:
            # Search for safe names
            for v in variables.values():
                if v.get_name() == name:
                    return v
            else:
                return self.get_variable_group(name)

    def get_variable_group(self, name):
        for i in self._vargroups:
            if i.get_name() == name:
                return i
        return None

    def get_variables(self):
        """
        Returns a list of variables

        Returns
        -------
        variables : list
            List of variables in the model

        Examples
        --------

        >>> x = m.add_variables(2, name='x')
        >>> y = m.add_variable(name='y')
        >>> print(m.get_variables())
        [sasoptpy.Variable(name='x_0',  vartype='CONT'),
         sasoptpy.Variable(name='x_1',  vartype='CONT'),
         sasoptpy.Variable(name='y',  vartype='CONT')]

        """
        return self._variables

    def get_variable_dict(self):
        return self._variableDict

    def get_grouped_variables(self):
        all_vars = [*self._vargroups, *self._variables]
        all_vars = sorted(all_vars, key=lambda i: i._objorder)
        grouped_vars = OrderedDict()
        for i in all_vars:
            if sasoptpy.core.util.has_parent(i):
                continue
            grouped_vars[i.get_name()] = i
        return grouped_vars

    def get_variable_coef(self, var):
        """
        Returns the objective value coefficient of a variable

        Parameters
        ----------
        var : Variable or string
            Variable whose objective value is requested or its name

        Returns
        -------
        coef : float
            Objective value coefficient of the given variable

        Examples
        --------

        >>> x = m.add_variable(name='x')
        >>> y = m.add_variable(name='y')
        >>> m.set_objective(4 * x - 5 * y, name='obj', sense=so.MAX)
        >>> print(m.get_variable_coef(x))
        4.0
        >>> print(m.get_variable_coef('y'))
        -5.0

        """
        if isinstance(var, sasoptpy.core.Variable):
            varname = var.get_name()
        else:
            varname = var
        if varname in self._objective._linCoef:
            return self._objective._linCoef[varname]['val']
        else:
            if self.get_objective()._is_linear():
                if varname in self._variableDict:
                    return 0
                else:
                    raise RuntimeError('Variable is not a member of the model')
            else:
                warnings.warn('Objective is not linear', RuntimeWarning)

    def set_variable_coef(self, var, coef):
        varname = var.get_name()
        if varname in self._objective._linCoef:
            self._objective._linCoef[varname]['val'] = coef
        else:
            self._objective += coef*var

    def set_variable_value(self, name, value):

        variable = self.get_variable(name)
        if variable is not None:
            variable.set_value(value)
        else:
            self._set_abstract_values(name, value)

    def set_dual_value(self, name, value):
        variable = self.get_variable(name)
        if variable is not None:
            variable.set_dual(value)

    def get_variable_value(self, var):
        """
        Returns the value of a variable.

        Parameters
        ----------
        var : Variable or string
            Variable reference

        Notes
        -----
        - It is possible to get a variable's value using
          :func:`Variable.get_value` method, if the variable is not abstract.
        - This method is a wrapper around :func:`Variable.get_value` and an
          overlook function for model components
        """

        if sasoptpy.core.util.is_variable(var):
            varname = var.get_name()
        else:
            varname = var

        if varname in self._variableDict:
            return self._variableDict[varname].get_value()
        else:
            return self._get_variable_solution(varname)

    def _get_variable_solution(self, name):
        if self._primalSolution is not None:
            for _, row in self._primalSolution.iterrows():
                if (row['var'] == name):
                    return row['value']
        else:
            raise RuntimeError('No primal solution is available')

        warnings.warn('Variable could not be found')
        return None

    def get_problem_summary(self):
        """
        Returns the problem summary table to the user

        Returns
        -------
        ps : :class:`swat.dataframe.SASDataFrame`
            Problem summary obtained after :func:`Model.solve`

        Examples
        --------

        >>> m.solve()
        >>> ps = m.get_problem_summary()
        >>> print(type(ps))
        <class 'swat.dataframe.SASDataFrame'>

        >>> print(ps)
        Problem Summary
                                        Value
        Label
        Problem Name                   model1
        Objective Sense          Maximization
        Objective Function                obj
        RHS                               RHS
        Number of Variables                 2
        Bounded Above                       0
        Bounded Below                       2
        Bounded Above and Below             0
        Free                                0
        Fixed                               0
        Number of Constraints               2
        LE (<=)                             1
        EQ (=)                              0
        GE (>=)                             1
        Range                               0
        Constraint Coefficients             4

        >>> print(ps.index)
        Index(['Problem Name', 'Objective Sense', 'Objective Function', 'RHS',
        '', 'Number of Variables', 'Bounded Above', 'Bounded Below',
        'Bounded Above and Below', 'Free', 'Fixed', '',
        'Number of Constraints', 'LE (<=)', 'EQ (=)', 'GE (>=)', 'Range', '',
        'Constraint Coefficients'],
        dtype='object', name='Label')

        >>> print(ps.loc['Number of Variables'])
        Value               2
        Name: Number of Variables, dtype: object

        >>> print(ps.loc['Constraint Coefficients', 'Value'])
        4

        """
        return self._problemSummary

    def get_solution_summary(self):
        """
        Returns the solution summary table to the user

        Returns
        -------
        ss : :class:`swat.dataframe.SASDataFrame`
            Solution summary obtained after solve

        Examples
        --------

        >>> m.solve()
        >>> soln = m.get_solution_summary()
        >>> print(type(soln))
        <class 'swat.dataframe.SASDataFrame'>

        >>> print(soln)
        Solution Summary
                                       Value
        Label
        Solver                            LP
        Algorithm               Dual Simplex
        Objective Function               obj
        Solution Status              Optimal
        Objective Value                   10
        Primal Infeasibility               0
        Dual Infeasibility                 0
        Bound Infeasibility                0
        Iterations                         2
        Presolve Time                   0.00
        Solution Time                   0.01

        >>> print(soln.index)
        Index(['Solver', 'Algorithm', 'Objective Function', 'Solution Status',
               'Objective Value', '', 'Primal Infeasibility',
               'Dual Infeasibility', 'Bound Infeasibility', '', 'Iterations',
               'Presolve Time', 'Solution Time'],
              dtype='object', name='Label')

        >>> print(soln.loc['Solution Status', 'Value'])
        Optimal

        """
        return self._solutionSummary

    def get_solution(self, vtype='Primal', solution=None, pivot=False):
        """
        Returns the solution details associated with the primal or dual
        solution

        Parameters
        ----------
        vtype : string, optional
            'Primal' or 'Dual'
        solution : integer, optional
            Solution number to be returned (for MILP)
        pivot : boolean, optional
            Switch for returning multiple solutions in columns as a pivot table

        Returns
        -------
        solution : :class:`pandas.DataFrame`
            Primal or dual solution table returned from the CAS Action

        Examples
        --------

        >>> m.solve()
        >>> print(m.get_solution('Primal'))
                     var   lb             ub  value  solution
        0       x[clock]  0.0  1.797693e+308    0.0       1.0
        1          x[pc]  0.0  1.797693e+308    5.0       1.0
        2   x[headphone]  0.0  1.797693e+308    2.0       1.0
        3         x[mug]  0.0  1.797693e+308    0.0       1.0
        4        x[book]  0.0  1.797693e+308    0.0       1.0
        5         x[pen]  0.0  1.797693e+308    1.0       1.0
        6       x[clock]  0.0  1.797693e+308    0.0       2.0
        7          x[pc]  0.0  1.797693e+308    5.0       2.0
        8   x[headphone]  0.0  1.797693e+308    2.0       2.0
        9         x[mug]  0.0  1.797693e+308    0.0       2.0
        10       x[book]  0.0  1.797693e+308    0.0       2.0
        11        x[pen]  0.0  1.797693e+308    0.0       2.0
        12      x[clock]  0.0  1.797693e+308    1.0       3.0
        13         x[pc]  0.0  1.797693e+308    4.0       3.0
        ...

        >>> print(m.get_solution('Primal', solution=2))
                     var   lb             ub  value  solution
        6       x[clock]  0.0  1.797693e+308    0.0       2.0
        7          x[pc]  0.0  1.797693e+308    5.0       2.0
        8   x[headphone]  0.0  1.797693e+308    2.0       2.0
        9         x[mug]  0.0  1.797693e+308    0.0       2.0
        10       x[book]  0.0  1.797693e+308    0.0       2.0
        11        x[pen]  0.0  1.797693e+308    0.0       2.0

        >>> print(m.get_solution(pivot=True))
        solution      1.0  2.0  3.0  4.0  5.0
        var
        x[book]       0.0  0.0  0.0  1.0  0.0
        x[clock]      0.0  0.0  1.0  1.0  0.0
        x[headphone]  2.0  2.0  1.0  1.0  0.0
        x[mug]        0.0  0.0  0.0  1.0  0.0
        x[pc]         5.0  5.0  4.0  1.0  0.0
        x[pen]        1.0  0.0  0.0  1.0  0.0

        >>> print(m.get_solution('Dual'))
                             con  value  solution
        0             weight_con   20.0       1.0
        1       limit_con[clock]    0.0       1.0
        2          limit_con[pc]    5.0       1.0
        3   limit_con[headphone]    2.0       1.0
        4         limit_con[mug]    0.0       1.0
        5        limit_con[book]    0.0       1.0
        6         limit_con[pen]    1.0       1.0
        7             weight_con   19.0       2.0
        8       limit_con[clock]    0.0       2.0
        9          limit_con[pc]    5.0       2.0
        10  limit_con[headphone]    2.0       2.0
        11        limit_con[mug]    0.0       2.0
        12       limit_con[book]    0.0       2.0
        13        limit_con[pen]    0.0       2.0
        ...

        >>> print(m.get_solution('dual', pivot=True))
        solution               1.0   2.0   3.0   4.0  5.0
        con
        limit_con[book]        0.0   0.0   0.0   1.0  0.0
        limit_con[clock]       0.0   0.0   1.0   1.0  0.0
        limit_con[headphone]   2.0   2.0   1.0   1.0  0.0
        limit_con[mug]         0.0   0.0   0.0   1.0  0.0
        limit_con[pc]          5.0   5.0   4.0   1.0  0.0
        limit_con[pen]         1.0   0.0   0.0   1.0  0.0
        weight_con            20.0  19.0  20.0  19.0  0.0

        Notes
        -----

        - If :meth:`Model.solve` method is used with :code:`frame=True` option,
          MILP solver returns multiple solutions. You can obtain different
          results using :code:`solution` parameter.

        """
        if vtype == 'Primal' or vtype == 'primal':
            if pivot:
                return self._primalSolution.pivot_table(
                    index=['var'], columns=['solution'], values='value')
            elif solution and 'solution' in self._primalSolution:
                return self._primalSolution.loc[
                    self._primalSolution['solution'] == solution]
            else:
                return self._primalSolution
        elif vtype == 'Dual' or vtype == 'dual':
            if pivot:
                return self._dualSolution.pivot_table(
                    index=['con'], columns=['solution'], values='value')
            elif solution and 'solution' in self._dualSolution:
                return self._dualSolution.loc[
                    self._dualSolution['solution'] == solution]
            else:
                return self._dualSolution
        else:
            raise ValueError('Solution type should be \'primal\' or \'dual\'')

    def set_session(self, session):
        """
        Sets the CAS session for model

        Parameters
        ----------
        session : :class:`swat.cas.connection.CAS` or \
:class:`saspy.SASsession`
            CAS or SAS Session object

        Notes
        -----

        * Session of a model can be set at initialization.
          See :class:`Model`.

        """
        self._session = session

    def get_session(self):
        return self._session

    def get_sets(self):
        return self._sets

    def get_parameters(self):
        return self._parameters

    def get_statements(self):
        return self._statements

    def get_implicit_variables(self):
        return self._impvars

    def print_solution(self):
        """
        Prints the current values of the variables

        Examples
        --------

        >>> m.solve()
        >>> m.print_solution()
        x: 2.0
        y: 0.0

        See also
        --------
        :func:`Model.get_solution`

        Notes
        -----

        - This function may not work for abstract variables and nonlinear
          models.

        """
        for v in self._variables:
            print('{}: {}'.format(v.get_name(), v._value))

    def to_frame(self, **kwargs):
        warnings.warn('Use to_mps for obtaining problem in MPS format',
                      DeprecationWarning)
        self.to_mps(**kwargs)

    def to_mps(self, **kwargs):
        return sasoptpy.interface.to_mps(self, **kwargs)

    def to_optmodel(self, **kwargs):
        return sasoptpy.interface.to_optmodel(self, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the Model object.

        Examples
        --------

        >>> print(m)
        Model: [
          Name: knapsack
          Session: cashost:casport
          Objective: MAX [8 * get[clock] + 10 * get[mug] + 15 * get[headphone]\
 + 20 * get[book] + get[pen]]
          Variables (5): [
            get[clock]
            get[mug]
            get[headphone]
            get[book]
            get[pen]
          ]
          Constraints (6): [
            get[clock] <=  3
            get[mug] <=  5
            get[headphone] <=  2
            get[book] <=  10
            get[pen] <=  15
            4 * get[clock] + 6 * get[mug] + 7 * get[headphone] + \
12 * get[book] + get[pen] <=  55
          ]
        ]

        """
        s = 'Model: [\n'
        s += '  Name: {}\n'.format(self.get_name())
        if self._session is not None:
            s += '  Session: {}:{}\n'.format(self._session._hostname,
                                             self._session._port)
        s += '  Objective: {} [{}]\n'.format(self.get_objective().get_sense(),
                                             self.get_objective())
        s += '  Variables ({}): [\n'.format(len(self._variables))
        for i in self._variables:
            s += '    {}\n'.format(i)
        s += '  ]\n'
        s += '  Constraints ({}): [\n'.format(len(self._constraints))
        for i in self._constraints:
            s += '    {}\n'.format(i)
        s += '  ]\n'
        s += ']'
        return s

    def __repr__(self):
        """
        Returns a representation of the Model object.

        Examples
        --------

        >>> print(repr(m))
        sasoptpy.Model(name='model1', session=CAS('cashost', 12345,
            'username', protocol='cas', name='py-session-1',
            session='594ad8d5-6a7b-3443-a155-be59177e8d23'))

        """
        if self._session is not None:
            stype = self.get_session_type()
            if stype == 'SAS':
                s = "sasoptpy.Model(name='{}', session=saspy.SASsession(cfgname='{}'))".format(
                         self.get_name(), self._session.sascfg.name)
            elif stype == 'CAS':
                s = 'sasoptpy.Model(name=\'{}\', session={})'.format(
                    self.get_name(), self._session)
            else:
                raise TypeError('Invalid session type: {}'.format(type(self.get_session())))
        else:
            s = 'sasoptpy.Model(name=\'{}\')'.format(self.get_name())
        return s

    def _defn(self):
        s = 'problem {}'.format(self.get_name())
        vars = [s.get_name() for s in self.get_grouped_variables().values()]
        cons = [s.get_name() for s in self.get_grouped_constraints().values()]
        obj = self.get_objective()
        objs = []
        if not obj.is_default():
            objs.append(obj.get_name())
        elements = ' '.join(vars + cons + objs)
        if elements != '':
            s += ' include ' + elements
        s += ';'
        return s

    def _expr(self):
        return self.to_optmodel()

    def _is_linear(self):
        """
        Checks if the model can be written as a linear model (in MPS format)

        Returns
        -------
        is_linear : boolean
            True if model does not have any nonlinear components or abstract\
            operations, False otherwise
        """
        for c in self._constraints:
            if not c._is_linear():
                return False
        if not self._objective._is_linear():
            return False
        return True

    def get_session_type(self):
        """
        Tests if the model session is defined and still active

        Returns
        -------
        session : string
            'CAS' for CAS sessions, 'SAS' for SAS sessions, None otherwise

        """
        # Check if session is defined
        return sasoptpy.util.get_session_type(self._session)

    @sasoptpy.containable
    def solve(self, **kwargs):
        """
        Solves the model by calling CAS or SAS optimization solvers

        Parameters
        ----------
        options : dict, optional
            A dictionary solver options
        submit : boolean, optional
            Switch for calling the solver instantly
        name : string, optional
            Name of the table name
        frame : boolean, optional
            Switch for uploading problem as a MPS DataFrame format
        drop : boolean, optional
            Switch for dropping the MPS table after solve (only CAS)
        replace : boolean, optional
            Switch for replacing an existing MPS table (only CAS and MPS)
        primalin : boolean, optional
            Switch for using initial values (only MILP)
        verbose : boolean, optional (experimental)
            Switch for printing generated OPTMODEL code

        Returns
        -------
        solution : :class:`pandas.DataFrame`
            Solution of the optimization model

        Examples
        --------

        >>> m.solve()
        NOTE: Initialized model food_manufacture_1
        NOTE: Converting model food_manufacture_1 to DataFrame
        NOTE: Added action set 'optimization'.
        ...
        NOTE: Optimal.
        NOTE: Objective = 107842.59259.
        NOTE: The Dual Simplex solve time is 0.01 seconds.

        >>> m.solve(options={'maxtime': 600})

        >>> m.solve(options={'algorithm': 'ipm'})

        Notes
        -----

        * This method is essentially a wrapper for two other methods.
        * Some of the options listed under ``options`` argument may not be
          passed based on which CAS Action is being used.
        * The ``option`` argument should be a dictionary, where keys are
          option names. For example, ``m.solve(options={'maxtime': 600})``
          limits the solution time to 600 seconds.
        * See :ref:`solver-options` for a list of solver options.

        See also
        --------
        :meth:`Model.solve_on_cas`, :meth:`Model.solve_on_mva`

        """

        return sasoptpy.util.submit_for_solve(self, **kwargs)


    def _set_abstract_values(self, name, value):
        """
        Searches for the missing/abstract variable names and set their values
        """
        original_name = sasoptpy.util.get_group_name(name)
        group = self.get_variable_group(original_name)
        if group:
            v = group.get_member_by_name(name)
            v.set_value(value)

    def clear_solution(self):
        self._objval = None
        self.response = None
        self._soltime = 0

