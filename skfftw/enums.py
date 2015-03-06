# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from __future__ import absolute_import, division, print_function

from .wrappers.constants import *
from enum import IntEnum, unique

__all__ = ('Directions', 'Flags')


@unique
class Directions(IntEnum):
    forward = FFTW_FORWARD
    backward = FFTW_BACKWARD


@unique
class Flags(IntEnum):
    measure = FFTW_MEASURE
    destroy_input = FFTW_DESTROY_INPUT
    unaligned = FFTW_UNALIGNED
    conserve_memory = FFTW_CONSERVE_MEMORY
    exhaustive = FFTW_EXHAUSTIVE
    preserve_input = FFTW_PRESERVE_INPUT
    patient = FFTW_PATIENT
    estimate = FFTW_ESTIMATE
    wisdom_only = FFTW_WISDOM_ONLY


def _get_sign_int(direction):
    # default to forward transform
    sign_int = directions.forward
    if direction in directions:
        sign_int = direction
    else:
        try:
            sign_int = getattr(directions, str(direction).lower())
        except AttributeError:
            pass
    return sign_int


def _get_flag_int(flags_list):
    # default to max planning effort
    flag_int = flags.measure
    try:
        for flag in flags_list:
            if flag in flags:
                flag_int |= flag
            else:
                try:
                    flag_int |= getattr(flags, str(flag).lower())
                except AttributeError:
                    pass
    except TypeError:
        pass
    return flag_int
