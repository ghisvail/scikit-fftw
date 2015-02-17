# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from skfftw.bindings.cffi import ffi, lib

__all__ = ('execute', 'plan_dft', 'execute_dft', 'destroy_plan')


def execute(plan):
    lib.fftwl_execute(plan)


def plan_dft(in_array, out_array, sign, flags):
    return lib.fftwl_plan_dft(
        in_array.ndim,
        ffi.new('const int []', in_array.shape),
        ffi.cast('fftwl_complex *', in_array.ctypes.data),
        ffi.cast('fftwl_complex *', out_array.ctypes.data),
        sign,
        flags,
    )


def execute_dft(plan, in_array, out_array):
    lib.fftwl_execute_dft(
        plan,
        ffi.cast('fftwl_complex *', in_array.ctypes.data),
        ffi.cast('fftwl_complex *', out_array.ctypes.data),
    )


def destroy_plan(plan):
    lib.fftwl_destroy_plan(plan)