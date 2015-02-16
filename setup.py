# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from __future__ import absolute_import, division, print_function

from distutils.command.build import build
from setuptools.command.install import install
from setuptools import setup, find_packages
import os


# Access to cffi extension
def get_ext_modules():
    import skfftw.bindings.cffi as cffi
    return [cffi.ffi.verifier.get_extension()]


# Build command
class BuildCommand(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


# Intall command
class InstallCommand(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


root_dir = os.path.dirname(__file__)
with open(os.path.join(root_dir, "README.md")) as f:
    long_description = f.read()


setup(
    name="scitkit-fftw",
    version="0.1.dev1",
    description="Python bindings for FFTW",
    long_description=long_description,
    license="BSD",
    url="https://github.com/ghisvail/scikit-fftw",
    author="Ghislain Antony Vaillant",
    author_email="ghisvail@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research", 
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering",
        ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires= [
        "cffi >= 0.6",
        ],
    cmdclass={
        "build": BuildCommand,
        "install": InstallCommand,
        },
    # for cffi
    zip_safe=False, 
    ext_package="skfftw",   
    )
