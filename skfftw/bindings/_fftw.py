# coding: utf8

# Copyright (c) 2014-2015 Ghislain Antony Vaillant
#
# This file is distributed under the MIT License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/MIT).

from __future__ import absolute_import, division, print_function


INCLUDES = """
#include <fftw3.h>
"""

TYPES = """
typedef ... fftw_complex;
typedef ... *fftw_plan;

typedef ... fftwf_complex;
typedef ... *fftwf_plan;

typedef ... fftwl_complex;
typedef ... *fftwl_plan;
"""

FUNCTIONS = """
void fftw_execute(const fftw_plan);
fftw_plan fftw_plan_dft(int, const int *, fftw_complex *, fftw_complex *,
                        int, unsigned);
void fftw_execute_dft(const fftw_plan, fftw_complex *, fftw_complex *);
void fftw_destroy_plan(fftw_plan);

void fftwf_execute(const fftwf_plan);
fftwf_plan fftwf_plan_dft(int, const int *, fftwf_complex *, fftwf_complex *,
                          int, unsigned);
void fftwf_execute_dft(const fftwf_plan, fftwf_complex *, fftwf_complex *);
void fftwf_destroy_plan(fftwf_plan);

void fftwl_execute(const fftwl_plan);
fftwl_plan fftwl_plan_dft(int, const int *, fftwl_complex *, fftwl_complex *,
                          int, unsigned);
void fftwl_execute_dft(const fftwl_plan, fftwl_complex *, fftwl_complex *);
void fftwl_destroy_plan(fftwl_plan);
"""

MACROS = """
#define FFTW_FORWARD ...
#define FFTW_BACKWARD ...

#define FFTW_MEASURE ...
#define FFTW_DESTROY_INPUT ...
#define FFTW_UNALIGNED ...
#define FFTW_CONSERVE_MEMORY ...
#define FFTW_EXHAUSTIVE ...
#define FFTW_PRESERVE_INPUT ...
#define FFTW_PATIENT ...
#define FFTW_ESTIMATE ...
#define FFTW_WISDOM_ONLY ...
"""

CUSTOMIZATIONS = """
"""

CONDITIONAL_NAMES = {}