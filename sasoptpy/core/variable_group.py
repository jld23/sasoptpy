
from collections import OrderedDict
from itertools import product
from math import inf
import warnings

import sasoptpy
from sasoptpy._libs import (pd, np)
from sasoptpy.core import (Expression, Variable)


class VariableGroup:
    """
    Creates a group of :class:`Variable` objects

    Parameters
    ----------
    argv : list, dict, int, :class:`pandas.Index`
        Loop index for variable group
    name : string, optional
        Name (prefix) of the variables
    vartype : string, optional
        Type of variables, `BIN`, `INT`, or `CONT`
    lb : list, dict, :class:`pandas.Series`, optional
        Lower bounds of variables
    ub : list, dict, :class:`pandas.Series`, optional
        Upper bounds of variables
    init : float, optional
        Initial values of variables

    Examples
    --------

    >>> PERIODS = ['Period1', 'Period2', 'Period3']
    >>> production = so.VariableGroup(PERIODS, vartype=so.INT,
                                      name='production', lb=10)
    >>> print(production)
    Variable Group (production) [
      [Period1: production['Period1']]
      [Period2: production['Period2']]
      [Period3: production['Period3']]
    ]

    >>> x = so.VariableGroup(4, vartype=so.BIN, name='x')
    >>> print(x)
    Variable Group (x) [
      [0: x[0]]
      [1: x[1]]
      [2: x[2]]
      [3: x[3]]
    ]

    >>> z = so.VariableGroup(2, ['a', 'b', 'c'], name='z')
    >>> print(z)
    Variable Group (z) [
      [(0, 'a'): z[0, 'a']]
      [(0, 'b'): z[0, 'b']]
      [(0, 'c'): z[0, 'c']]
      [(1, 'a'): z[1, 'a']]
      [(1, 'b'): z[1, 'b']]
      [(1, 'c'): z[1, 'c']]
    ]
    >>> print(repr(z))
    sasoptpy.VariableGroup([0, 1], ['a', 'b', 'c'], name='z')

    Notes
    -----
    * When working with a single model, use the
      :func:`sasoptpy.Model.add_variables` method.
    * If a variable group object is created, it can be added to a model using
      the :func:`sasoptpy.Model.include` method.
    * An individual variable inside the group can be accessed using indices.

      >>> z = so.VariableGroup(2, ['a', 'b', 'c'], name='z', lb=0, ub=10)
      >>> print(repr(z[0, 'a']))
      sasoptpy.Variable(name='z_0_a', lb=0, ub=10, vartype='CONT')

    See also
    --------
    :func:`sasoptpy.Model.add_variables`
    :func:`sasoptpy.Model.include`

    """

    def __init__(self, *argv, name, vartype=None, lb=None,
                 ub=None, init=None, abstract=False):
        self._vardict = OrderedDict()
        self._varlist = []
        self._groups = OrderedDict()
        self._keyset = []

        if vartype is None:
            vartype = sasoptpy.CONT

        if vartype == sasoptpy.BIN and ub is None:
            ub = 1
        if vartype == sasoptpy.BIN and lb is None:
            lb = 0

        if lb is None:
            lb = -inf
        if ub is None:
            ub = inf

        self._recursive_add_vars(*argv, name=name,
                                 vartype=vartype, lb=lb, ub=ub, init=init,
                                 vardict=self._vardict, varlist=self._varlist,
                                 abstract=abstract)

        self._lb = lb
        self._ub = ub
        self._init = init
        self._type = vartype

        name = sasoptpy.util.assign_name(name, 'vg')
        self._name = name
        self._objorder = sasoptpy.util.register_globally(name, self)

        self._abstract = abstract
        for arg in argv:
            if isinstance(arg, int):
                self._keyset.append(sasoptpy.util._extract_argument_as_list(arg))
            else:
                self._keyset.append(sasoptpy.util._extract_argument_as_list(arg))
                if not self._abstract and sasoptpy.util.is_set_abstract(arg):
                    self._abstract = True
                    for _, v in self._vardict.items():
                        v._abstract = True

        self._shadows = OrderedDict()
        self._set_var_info()

    def get_name(self):
        """
        Returns the name of the variable group

        Returns
        -------
        name : string
            Name of the variable group

        Examples
        --------

        >>> m = so.Model(name='m')
        >>> var1 = m.add_variables(4, name='x')
        >>> print(var1.get_name())
        x
        """
        return self._name

    def add_member(self, key, var=None, name=None, vartype=None, lb=None,
                   ub=None, init=None, shadow=False):
        """
        (Experimental) Adds a new member to Variable Group
        Notes
        -----
        - This method is mainly intended for internal use.
        """

        key = sasoptpy.util.pack_to_tuple(key)
        dict_to_add = self._vardict if not shadow else self._shadows

        if var is not None:
            dict_to_add[key] = var
            return var
        else:
            vartype = vartype if vartype is not None else self._type
            lb = lb if lb is not None else self._lb
            ub = ub if ub is not None else self._ub
            if name is not None:
                varname = name
            else:
                varname = '{}['.format(self._name) + ','.join(
                        format(k) for k in key) + ']'
            new_var = sasoptpy.Variable(
                name=varname, lb=lb, ub=ub, init=init, vartype=vartype,
                shadow=shadow, abstract=False)
            dict_to_add[key] = new_var
            return new_var

    def set_abstract(self, abstract=True):
        self._abstract = abstract

    def _recursive_add_vars(self, *argv, name, vartype, lb, ub, init,
                            vardict, varlist, vkeys=(), abstract=False):

        next_arg = sasoptpy.util._extract_argument_as_list(argv[0])

        for _, i in enumerate(next_arg):
            if isinstance(i, tuple):
                current_keys = vkeys + i
            else:
                current_keys = vkeys + (i,)

            if len(argv) == 1:
                varname = sasoptpy.core.util.get_name_from_keys(
                    name, current_keys)

                self._register_keys(current_keys)

                varlb = sasoptpy.util.extract_list_value(current_keys, lb)
                varub = sasoptpy.util.extract_list_value(current_keys, ub)
                varin = sasoptpy.util.extract_list_value(current_keys, init)

                new_var = sasoptpy.Variable(
                    name=varname, lb=varlb, ub=varub, init=varin,
                    vartype=vartype, abstract=abstract)
                vardict[current_keys] = new_var
                varlist.append(current_keys)
            else:
                self._recursive_add_vars(*argv[1:], vardict=vardict,
                                         vkeys=current_keys,
                                         name=name, vartype=vartype,
                                         lb=lb, ub=ub, init=init,
                                         varlist=varlist)

    def _register_keys(self, keys):
        for j, k in enumerate(keys):
            try:
                self._groups[j] = self._groups[j].union(pd.Index([k]))
            except KeyError:
                self._groups[j] = pd.Index([k])

    def _set_var_info(self):
        for i in self._vardict:
            self._vardict[i]._set_info(parent=self, key=i)

    def __getitem__(self, key):
        """
        Overloaded method to access individual variables

        Parameters
        ----------
        key : tuple, string or int
            Key of the variable

        Returns
        -------
        ref : Variable or list
            Reference to a single Variable or a list of Variable objects

        """
        if self._abstract or sasoptpy.util.is_key_abstract(key):
            tuple_key = sasoptpy.util.pack_to_tuple(key)
            tuple_key = tuple(i for i in sasoptpy.util.flatten_tuple(tuple_key))
            if tuple_key in self._shadows:
                return self._shadows[tuple_key]
            else:
                k = list(self._vardict)[0]
                v = self._vardict[k]
                vname = self._name
                vname = vname.replace(' ', '')
                shadow = Variable(name=vname, vartype=v._type, lb=v._lb,
                                  ub=v._ub, init=v._init, abstract=True,
                                  shadow=True)
                ub = sasoptpy.abstract.ParameterValue(shadow, key=tuple_key,
                                                  suffix='.ub')
                lb = sasoptpy.abstract.ParameterValue(shadow, key=tuple_key,
                                                  suffix='.lb')
                shadow._ub = ub
                shadow._lb = lb
                shadow._iterkey = tuple_key
                self._shadows[tuple_key] = shadow
                return shadow

        k = sasoptpy.util.pack_to_tuple(key)
        if k in self._vardict:
            return self._vardict[k]
        else:
            indices_to_filter = []
            filter_values = {}
            list_of_variables = []
            for i, _ in enumerate(k):
                if k[i] != '*':
                    indices_to_filter.append(i)
                    filter_values[i] = sasoptpy.util.pack_to_list(k[i])
            for v in self._vardict:
                eligible = True
                for f in indices_to_filter:
                    if v[f] not in filter_values[f]:
                        eligible = False
                if eligible:
                    list_of_variables.append(self._vardict[v])
            if not list_of_variables:
                warnings.warn('Requested variable group is empty:' +
                              ' {}[{}] ({})'.
                              format(self._name, key, type(key)),
                              RuntimeWarning, stacklevel=2)
            return list_of_variables

    def __iter__(self):
        """
        Yields an iterable list of variables inside the variable group

        Returns
        -------
        i : list
            Iterable list of Variable objects
        """
        for i in self._varlist:
            yield self._vardict[i]

    def _defn(self, tabs=''):
        """
        Returns string to be used in OPTMODEL definition

        Parameters
        ----------

        tabs : string, optional
            Tab string that is used in :meth:`Model.to_optmodel` method

        """
        s = tabs + 'var {}'.format(self._name)
        s += ' {'
        for i in self._keyset:
            ind_list = []
            for j in i:
                ind_list.append(sasoptpy.util._to_optmodel_quoted_string(j))
            s += '{{{}}}, '.format(','.join(ind_list))
        s = s[:-2]
        s += '} '

        # Grab features
        CONT = sasoptpy.CONT
        BIN = sasoptpy.BIN
        INT = sasoptpy.INT
        if self._type != CONT:
            if self._type == BIN:
                s += 'binary '
            if self._type == INT:
                s += 'integer '
        if self._lb is not None and\
           np.isinstance(type(self._lb), np.number) and\
           self._lb != -inf and\
           not(self._lb == 0 and self._type == BIN):
            s += '>= {} '.format(self._lb)
        if self._ub is not None and\
           np.isinstance(type(self._ub), np.number) and\
           self._ub != inf and\
           not(self._ub == 1 and self._type == BIN):
            s += '<= {} '.format(self._ub)
        if self._init is not None:
            s += 'init {} '.format(self._init)

        s = s.rstrip()
        s += ';'
        # Check bounds to see if they are parameters
        if self._abstract:
            for i in self._shadows:
                v = self._shadows[i]
                lbparam = str(v) + '.lb' != str(v._lb)
                ubparam = str(v) + '.ub' != str(v._ub)
                if lbparam or ubparam:
                    s += '\n' + tabs
                    in_a_loop = False
                    if any(sasoptpy.abstract.util.is_key_abstract(e) for e in i):
                        loop_text = sasoptpy.util._to_optmodel_loop(i)
                        s += 'for' + loop_text + ' '
                        in_a_loop = True
                    if lbparam:
                        s += str(v) + '.lb=' + sasoptpy.util._to_optmodel_expr(v._lb)
                        s += ' '
                        if not in_a_loop:
                            s = s.rstrip() + ';\n'
                    if ubparam:
                        s += str(v) + '.ub=' + sasoptpy.util._to_optmodel_expr(
                            v._ub)
                        s += ' '
                    s = s.rstrip()
                    s += ';'
                initparam = v._init is not None and v._init != self._init
                if initparam:
                    s += '\n' + tabs
                    if any(sasoptpy.abstract.util.is_key_abstract(e) for e in i):
                        loop_text = sasoptpy.util._to_optmodel_loop(i)
                        s += 'for' + loop_text + ' '
                    s += str(v) + ' = ' + str(v._init)
                    s = s.rstrip()
                    s += ';'
        else:
            for _, v in self._vardict.items():
                # Check if LB needs to be printed
                printlb = False
                defaultlb = 0 if self._type is BIN else -inf
                if v._lb is not None:
                    condition1 = self._lb is None or not np.isinstance(type(self._lb), np.number)
                    condition2 = v._lb == defaultlb and (self._lb is not None and self._lb != defaultlb)
                    condition3 = v._lb != self._lb
                    if condition1 or condition2 or condition3:
                        printlb = True
                if printlb:
                    s += '\n' + tabs + '{}.lb = {};'.format(v._expr(), v._lb if v._lb != -inf else "-constant('BIG')")

                # Check if UB needs to be printed
                printub = False
                defaultub = 1 if self._type is BIN else inf
                if v._ub is not None:
                    condition1 = self._ub is None or not np.isinstance(type(self._ub), np.number)
                    condition2 = v._ub == defaultub and (self._ub is not None and self._ub != defaultub)
                    condition3 = v._ub != self._ub
                    if condition1 or condition2 or condition3:
                        printub = True
                if printub:
                    s += '\n' + tabs + '{}.ub = {};'.format(v._expr(), v._ub if v._ub != inf else "constant('BIG')")

                # Check if init needs to be printed
                if v._init is not None:
                    if v._init != self._init:
                        s += '\n' + tabs + '{} = {};'.format(v._expr(), v._init)

        return(s)

    def sum(self, *argv):
        """
        Quick sum method for the variable groups

        Parameters
        ----------
        argv : Arguments
            List of indices for the sum

        Returns
        -------
        r : Expression
            Expression that represents the sum of all variables in the group

        Examples
        --------

        >>> z = so.VariableGroup(2, ['a', 'b', 'c'], name='z', lb=0, ub=10)
        >>> e1 = z.sum('*', '*')
        >>> print(e1)
        z[1, 'c']  +  z[1, 'a']  +  z[1, 'b']  +  z[0, 'a']  +  z[0, 'b']  +
        z[0, 'c']
        >>> e2 = z.sum('*', 'a')
        >>> print(e2)
         z[1, 'a']  +  z[0, 'a']
        >>> e3 = z.sum('*', ['a', 'b'])
        >>> print(e3)
         z[1, 'a']  +  z[0, 'b']  +  z[1, 'b']  +  z[0, 'a']

        """
        if self._abstract:
            r = Expression()
            symbolic_sum = False
            ind_set = list()
            iter_key = list()
            for i, a in enumerate(argv):
                if isinstance(a, str) and a == '*':
                    sub_list = list()
                    for j in self._keyset[i]:
                        if sasoptpy.abstract.util.is_abstract_set(j):
                            si = sasoptpy.abstract.SetIterator(j)
                            iter_key.append(si)
                            ind_set.append(si)
                            symbolic_sum = True
                        else:
                            #ind_set.append(j)
                            sub_list.append(j)
                    if sub_list:
                        ind_set.append(sub_list)
                else:
                    if hasattr(a, '__iter__'):
                        ind_set.append(a)
                    else:
                        ind_set.append([a])
            combs = product(*ind_set)
            for i in combs:
                var_key = sasoptpy.util.pack_to_tuple(i)
                r = r.add(self[var_key], 1)
            if symbolic_sum:
                #r = r.add(self[tuple(ind_set)])
                r._operator = 'sum'
                r._iterkey = iter_key
            return r
        else:
            r = Expression(temp=True)
            feas_set = []
            for i, a in enumerate(argv):
                if a == '*':
                    feas_set.append(self._groups[i])
                elif hasattr(a, "__iter__") and not isinstance(a, str):
                    feas_set.append(a)
                else:
                    feas_set.append([a])
            combs = product(*feas_set)
            for i in combs:
                var_key = sasoptpy.util.pack_to_tuple(i)
                if var_key in self._vardict:
                    r.add(self._vardict[var_key], 1)
            r.set_permanent()
            return r

    def mult(self, vector):
        """
        Quick multiplication method for the variable groups

        Parameters
        ----------
        vector : list, dictionary, :class:`pandas.Series`,\
                 or :class:`pandas.DataFrame`
            Vector to be multiplied with the variable group

        Returns
        -------
        r : Expression
            An expression that is the product of the variable group with the
            given vector

        Examples
        --------

        Multiplying with a list

        >>> x = so.VariableGroup(4, vartype=so.BIN, name='x')
        >>> e1 = x.mult([1, 5, 6, 10])
        >>> print(e1)
         10.0 * x[3]  +  6.0 * x[2]  +  x[0]  +  5.0 * x[1]

        Multiplying with a dictionary

        >>> y = so.VariableGroup([0, 1], ['a', 'b'], name='y', lb=0, ub=10)
        >>> dvals = {(0, 'a'): 1, (0, 'b'): 2, (1, 'a'): -1, (1, 'b'): 5}
        >>> e2 = y.mult(dvals)
        >>> print(e2)
         2.0 * y[0, 'b']  -  y[1, 'a']  +  y[0, 'a']  +  5.0 * y[1, 'b']

        Multiplying with a pandas.Series object

        >>> u = so.VariableGroup(['a', 'b', 'c', 'd'], name='u')
        >>> ps = pd.Series([0.1, 1.5, -0.2, 0.3], index=['a', 'b', 'c', 'd'])
        >>> e3 = u.mult(ps)
        >>> print(e3)
         1.5 * u['b']  +  0.1 * u['a']  -  0.2 * u['c']  +  0.3 * u['d']

        Multiplying with a pandas.DataFrame object

        >>> data = np.random.rand(3, 3)
        >>> df = pd.DataFrame(data, columns=['a', 'b', 'c'])
        >>> print(df)
        NOTE: Initialized model model1
                  a         b         c
        0  0.966524  0.237081  0.944630
        1  0.821356  0.074753  0.345596
        2  0.065229  0.037212  0.136644
        >>> y = m.add_variables(3, ['a', 'b', 'c'], name='y')
        >>> e = y.mult(df)
        >>> print(e)
        0.9665237354418064 * y[0, 'a']  +  0.23708064143289442 * y[0, 'b']  +
        0.944629500537536 * y[0, 'c']  +  0.8213562592159828 * y[1, 'a']  +
        0.07475256894157478 * y[1, 'b']  +  0.3455957019116668 * y[1, 'c']  +
        0.06522945752546017 * y[2, 'a']  +  0.03721153533250843 * y[2, 'b']  +
        0.13664422498043194 * y[2, 'c']

        """

        r = Expression()
        if isinstance(vector, list) or isinstance(vector, np.ndarray):
            for i, key in enumerate(vector):
                var = self._vardict[i, ]
                r._linCoef[var._name] = {'ref': var, 'val': vector[i]}
        elif isinstance(vector, pd.Series):
            for key in vector.index:
                k = sasoptpy.util.pack_to_tuple(key)
                var = self._vardict[k]
                r._linCoef[var._name] = {'ref': var, 'val': vector[key]}
        elif isinstance(vector, pd.DataFrame):
            vectorflat = sasoptpy.util.flatten_frame(vector)
            for key in vectorflat.index:
                k = sasoptpy.util.pack_to_tuple(key)
                var = self._vardict[k]
                r._linCoef[var._name] = {'ref': var, 'val': vectorflat[key]}
        else:
            for i, key in enumerate(vector):
                if isinstance(key, tuple):
                    k = key
                else:
                    k = (key,)
                var = self._vardict[k]
                try:
                    r._linCoef[var._name] = {'ref': var, 'val': vector[i]}
                except KeyError:
                    r._linCoef[var._name] = {'ref': var, 'val': vector[key]}

        return r

    def set_init(self, init):
        """
        Sets / updates initial value for the given variable

        Parameters
        ----------
        init : float, list, dict, :class:`pandas.Series`
            Initial value of the variables

        Examples
        --------

        >>> m = so.Model(name='m')
        >>> y = m.add_variables(3, name='y')
        >>> print(y._defn())
        var y {{0,1,2}};
        >>> y.set_init(5)
        >>> print(y._defn())
        var y {{0,1,2}} init 5;

        """
        self._init = init
        for v in self._vardict:
            inval = sasoptpy.util.extract_list_value(v, init)
            self._vardict[v].set_init(inval)
        for v in self._shadows:
            self._shadows[v].set_init(init)

    def set_bounds(self, lb=None, ub=None):
        """
        Sets / updates bounds for the given variable

        Parameters
        ----------
        lb : float, :class:`pandas.Series`, optional
            Lower bound
        ub : float, :class:`pandas.Series`, optional
            Upper bound

        Examples
        --------

        >>> z = so.VariableGroup(2, ['a', 'b', 'c'], name='z', lb=0, ub=10)
        >>> print(repr(z[0, 'a']))
        sasoptpy.Variable(name='z_0_a', lb=0, ub=10, vartype='CONT')
        >>> z.set_bounds(lb=3, ub=5)
        >>> print(repr(z[0, 'a']))
        sasoptpy.Variable(name='z_0_a', lb=3, ub=5, vartype='CONT')

        >>> u = so.VariableGroup(['a', 'b', 'c', 'd'], name='u')
        >>> lb_vals = pd.Series([1, 4, 0, -1], index=['a', 'b', 'c', 'd'])
        >>> u.set_bounds(lb=lb_vals)
        >>> print(repr(u['b']))
        sasoptpy.Variable(name='u_b', lb=4, ub=inf, vartype='CONT')

        """
        if lb is not None:
            self._lb = lb
        if ub is not None:
            self._ub = ub
        for v in self._vardict:
            varlb = sasoptpy.util.extract_list_value(v, lb)
            if lb is not None:
                self._vardict[v].set_bounds(lb=varlb)
            varub = sasoptpy.util.extract_list_value(v, ub)
            if ub is not None:
                self._vardict[v].set_bounds(ub=varub)

    def __str__(self):
        """
        Generates a representation string
        """
        s = 'Variable Group ({}) [\n'.format(self._name)
        for k in self._vardict:
            v = self._vardict[k]
            s += '  [{}: {}]\n'.format(sasoptpy.util.get_first_member(k), v)
        s += ']'
        return s

    def __repr__(self):
        """
        Returns a string representation of the object.
        """
        s = 'sasoptpy.VariableGroup('
        keylen = max(map(len, self._vardict))
        for i in range(keylen):
            ls = []
            for k in self._vardict:
                if k[i] not in ls:
                    ls.append(k[i])
            s += '{}, '.format(ls)
        s += 'name=\'{}\')'.format(self._name)
        return s
