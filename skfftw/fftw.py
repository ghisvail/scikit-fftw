# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from __future__ import absolute_import, division, print_function

from skfftw.enums import _get_flag_int, _get_sign_int
from skfftw.wrappers import libfftw, libfftwf, libfftwl
import numpy as np


__all__ = ('plan',)


class plan(object):
    
    """
    The FFTW plan class.
    """
    
    __planner_funcs = {np.dtype('cdouble'): libfftw.plan_dft,
                       np.dtype('csingle'): libfftwf.plan_dft,
                       np.dtype('clongdouble'): libfftwl.plan_dft}
    __execute_funcs = {np.dtype('cdouble'): libfftw.execute_dft,
                       np.dtype('csingle'): libfftwf.execute_dft,
                       np.dtype('clongdouble'): libfftwl.execute_dft}
    __destroy_funcs = {np.dtype('cdouble'): libfftw.destroy_plan,
                       np.dtype('csingle'): libfftwf.destroy_plan,
                       np.dtype('clongdouble'): libfftwl.destroy_plan}
    
    def __init__(self, input_array, output_array, direction='forward',
                 flags=('estimate',), *args, **kwargs):
        """
        Instantiate a DFT plan.
        """
        self._handle = None
        dt = np.dtype(input_array.dtype)
        try:
            self._planner = self.__planner_funcs[dt]
            self._execute = self.__execute_funcs[dt]
            self._destroy = self.__destroy_funcs[dt]
        except:
            raise ValueError("Unsupported data type: {}".format(dt))
        self._input_array = input_array
        self._output_array = output_array
        sign_int = _get_sign_int(direction)
        self._direction = direction
        flag_int = _get_flag_int(flags)
        self._flags = flags
        self._handle = self._planner(self._input_array, self._output_array,
                                     sign_int, flag_int)
    
    def __del__(self):
        if self._handle is not None:
            self._destroy(self._handle)
    
    def __call__(self, input_array=None, output_array=None, normalize=False,
                 normalize_by_sqrt=False, *args, **kwargs):
        """
        Execute DFT from plan.
        
        Returns the result of the DFT as a Numpy array.        
        
        The input and output arrays used for DFT computation may be updated 
        using the input_array and output_array parameters. If the supplied
        array(s) is (are) not compatible with the original one(s) supplied 
        at construct time, a RuntimeError is raised.
        
        The resulting array may be optionally scaled by setting one of the 
        normalize flags to True. The choice of scaling convention (none, 
        by N or by sqrtN) is left to the user.
        """
        self.execute_dft(input_array, output_array)
        if normalize or normalize_by_sqrt:
            if normalize_by_sqrt:
                self._output_array /= np.sqrt(self.N)
            else:
                self._output_array /= self.N
        return self._output_array

    def execute(self):
        """
        Execute DFT from plan.
        
        For more options, please use the __call__ method of this plan.
        """
        self._execute(self._handle, self._input_array, self._output_array)

    def execute_dft(self, input_array=None, output_array=None):
        """
        Execute DFT from plan with optional update of the internal arrays.
        
        For more options, please use the __call__ method of this plan.
        """
        self._update_arrays(input_array, output_array)
        self.execute()

    def _update_arrays(self, input_array, output_array):
        """
        Private method used for safe update of the internal arrays.
        """
        # check input array
        if input_array is not None:
            if (input_array.flags.c_contiguous and
                input_array.shape == self.input_array.shape and
                input_array.dtype == self.input_array.dtype):
                self._input_array = input_array                
            else:
                raise RuntimeError('Incompatible input array')
        # check output array        
        if output_array is not None:
            if (output_array.flags.c_contiguous and
                output_array.shape == self.output_array.shape and
                output_array.dtype == self.output_array.dtype):
                self._output_array = output_array                
            else:
                raise RuntimeError('Incompatible output array')

    @property
    def direction(self):
        return self._direction

    @property
    def flags(self):
        return self._flags

    @property
    def input_array(self):
        return self._input_array

    @property
    def output_array(self):
        return self._output_array

    @property
    def N(self):
        return self._output_array.size