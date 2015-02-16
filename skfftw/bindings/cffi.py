# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

import os
from .utils import LazyLibrary, build_ffi_for_binding

__all__ = ('ffi', 'lib')


ffi = build_ffi_for_binding(
    module_prefix='skfftw.bindings',
    modules=["_fftw",],
    pre_include="",
    post_include="",
    libraries=["fftw3", "fftw3f", "fftw3l"],
    extra_compile_args=[],
    extra_link_args=[],
)
lib = LazyLibrary(ffi)