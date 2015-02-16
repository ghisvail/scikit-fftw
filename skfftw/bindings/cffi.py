# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

# Adapted from Donald Stufft's example at: 
# https://caremad.io/2014/11/distributing-a-cffi-project/

import binascii
import sys
import threading
from cffi import FFI
from cffi.verifier import Verifier

__all__ = ('ffi', 'api')


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


def get_cdef_sources():
    import os
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "cdef.h")) as f:
        cdef_sources = f.read()
    return cdef_sources


CDEF = get_cdef_sources()

SOURCE = """
#include "fftw3.h"
"""


ffi = FFI()
ffi.cdef(CDEF)
ffi.verifier = Verifier(
    ffi,
    SOURCE,
    modulename=_create_modulename(CDEF, SOURCE, sys.version),
    libraries=['fftw3', 'fftw3f', 'fftw3l'],
    ext_package="skfftw",
    # ... Any other arguments that were being passed to FFI().verify()
)


# Patch the Verifier() instance to prevent CFFI from compiling the module
ffi.verifier.compile_module = _compile_module
ffi.verifier._compile_module = _compile_module


# Export api
api = LazyLibrary(ffi)
