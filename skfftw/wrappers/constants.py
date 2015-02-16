# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from skfftw.bindings.cffi import lib

__all__ = (
    'FFTW_FORWARD',
    'FFTW_BACKWARD',
    'FFTW_ESTIMATE',
    'FFTW_MEASURE',
    'FFTW_PATIENT',
    'FFTW_EXHAUSTIVE',
    'FFTW_WISDOM_ONLY',
    'FFTW_DESTROY_INPUT',
    'FFTW_PRESERVE_INPUT',
    'FFTW_UNALIGNED',
)


FFTW_FORWARD = lib.FFTW_FORWARD
FFTW_BACKWARD = lib.FFTW_BACKWARD
FFTW_ESTIMATE = lib.FFTW_ESTIMATE
FFTW_MEASURE = lib.FFTW_MEASURE
FFTW_PATIENT = lib.FFTW_PATIENT
FFTW_EXHAUSTIVE = lib.FFTW_EXHAUSTIVE
FFTW_WISDOM_ONLY = lib.FFTW_WISDOM_ONLY
FFTW_DESTROY_INPUT = lib.FFTW_DESTROY_INPUT
FFTW_PRESERVE_INPUT = lib.FFTW_PRESERVE_INPUT
FFTW_UNALIGNED = lib.FFTW_UNALIGNED