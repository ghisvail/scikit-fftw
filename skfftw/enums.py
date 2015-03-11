# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from __future__ import absolute_import, division, print_function

from .wrappers.constants import *
import enum

__all__ = ('Direction', 'Flag', 'Normalization')


@enum.unique
class Direction(enum.IntEnum):
    forward = FFTW_FORWARD
    backward = FFTW_BACKWARD


@enum.unique
class Flag(enum.IntEnum):
    measure = FFTW_MEASURE
    destroy_input = FFTW_DESTROY_INPUT
    unaligned = FFTW_UNALIGNED
    conserve_memory = FFTW_CONSERVE_MEMORY
    exhaustive = FFTW_EXHAUSTIVE
    preserve_input = FFTW_PRESERVE_INPUT
    patient = FFTW_PATIENT
    estimate = FFTW_ESTIMATE
    wisdom_only = FFTW_WISDOM_ONLY


class Normalization(enum.Enum):
    none = 0
    sqrt = 1
    full = 2
    # aliases
    by_sqrt_N = 1
    by_N = 2