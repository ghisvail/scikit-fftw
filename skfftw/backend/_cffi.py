# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-2-Clause).

from __future__ import absolute_import, division, print_function

import binascii
import os
import sys
import threading

from cffi import FFI
from cffi.verifier import Verifier

__all__ = ('ffi', 'lib')


class LazyLibrary(object):
    def __init__(self, ffi):
        self._ffi = ffi
        self._lib = None
        self._lock = threading.Lock()

    def __getattr__(self, name):
        if self._lib is None:
            with self._lock:
                if self._lib is None:
                    self._lib = self._ffi.verifier.load_library()
        return getattr(self._lib, name)


def _create_modulename(cdef_sources, source, sys_version):
    """
    This is the same as CFFI's create modulename except we don't include the
    CFFI version.
    """
    key = '\x00'.join([sys_version[:3], source, cdef_sources])
    key = key.encode('utf-8')
    k1 = hex(binascii.crc32(key[0::2]) & 0xffffffff)
    k1 = k1.lstrip('0x').rstrip('L')
    k2 = hex(binascii.crc32(key[1::2]) & 0xffffffff)
    k2 = k2.lstrip('0').rstrip('L')
    return '_{0}_cffi_{1}{2}'.format("skfftw", k1, k2)


def _compile_module(*args, **kwargs):
    raise RuntimeError(
        "Attempted implicit compile of a cffi module. All cffi modules should "
        "be pre-compiled at installation time."
    )


# Load the cffi definitions
here = os.path.dirname(__file__)

with open(os.path.join(here, '_cdefs.h')) as f:
    _cdefs_source = f.read()

with open(os.path.join(here, '_verify.c')) as f:
    _verify_source = f.read()


# Make the ffi instance
ffi = FFI()
ffi.cdef(_cdefs_source)
ffi.verifier = Verifier(
    ffi,
    _verify_source,
    modulename=_create_modulename(_cdefs_source, _verify_source, sys.version),
    ext_package='skfftw',
    libraries=['fftw3', 'fftw3_threads', 'fftw3f', 'fftw3f_threads',
                'fftw3l', 'fftw3l_threads'],
    include_dirs=[],
    library_dirs=[],
    runtime_library_dirs=[],
)

# Patch the Verifier() instance to prevent CFFI from compiling the module
ffi.verifier.compile_module = _compile_module
ffi.verifier._compile_module = _compile_module

# Export the library object
lib = LazyLibrary(ffi)