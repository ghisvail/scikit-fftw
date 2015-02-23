# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from skfftw.fftw import plan
import numpy


class TestPlanCall():
    
    def setup_method(self, method):
        self.input_array = numpy.empty([64, 64], dtype=numpy.complex128)
        self.output_array = numpy.empty([64, 64], dtype=numpy.complex128)
        self.plan = plan(self.input_array, self.output_array)
        self.input_array[:, :] = (
            numpy.random.randn(*self.input_array.shape) + 
            1j * numpy.random.randn(*self.input_array.shape))

    def test_no_args(self):
        output_array = self.plan()
        assert self.plan.output_array is output_array

    def test_with_input_update(self):
        input_array = (
            numpy.random.randn(*self.input_array.shape) + 
            1j * numpy.random.randn(*self.input_array.shape))
        assert input_array is not self.plan.input_array
        output_array = self.plan(input_array=input_array)
        assert self.plan.input_array is input_array

    def test_with_output_update(self):
        output_array = numpy.empty([64, 64], dtype=numpy.complex128)
        assert output_array is not self.plan.output_array
        _ = self.plan(output_array=output_array)
        assert self.plan.output_array is output_array

    def test_without_normalize(self):
        self.input_array.ravel()[:] = 1
        output_array = self.plan()
        assert output_array.ravel()[0] == self.plan.N
                
    def test_with_normalize(self):
        self.input_array.ravel()[:] = 1
        output_array = self.plan(normalize=True)
        assert output_array.ravel()[0] == 1

    def test_with_sqrt_normalize(self):
        self.input_array.ravel()[:] = 1
        output_array = self.plan(normalize_by_sqrt=True)
        assert output_array.ravel()[0] == numpy.sqrt(self.plan.N)