#!/usr/bin/python
# coding: utf8

# Copyright (c) 2014, 2015 Ghislain Antony Vaillant.
#
# This file is distributed under the new BSD License, see the LICENSE file or 
# checkout the license terms at http://opensource.org/licenses/BSD-3-Clause).

from __future__ import absolute_import, division, print_function

from distutils.command.build import build
from distutils.command.install import install
from distutils.command.clean import clean
from setuptools import setup, find_packages
import os
import shutil


packages = find_packages(exclude=['docs', 'tests'])

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

# Clean command
# adapted from blaze/setup.py
class CleanCommand(clean):
    """Custom command to clean build artefacts."""
    
    user_options = [("all", "a", "")]
    
    def initialize_options(self):
        clean.initialize_options(self)
        self._clean_me = []
        self._clean_trees = []
        
        for toplevel in packages:
            for root, dirs, files in list(os.walk(toplevel)):
                for f in files:
                    if os.path.splitext(f)[-1] in ('.pyc', '.so', '.o', '.pyd'):
                        self._clean_me.append(os.path.join(root, f))
                
                for d in dirs:
                    if d in ('__pycache__',):
                        self._clean_trees.append(os.path.join(root, d))

        for d in os.listdir(os.curdir):
            if d in ('build', 'dist'):
                self._clean_trees.append(d)
            if d.endswith('.egg-info'):
                self._clean_trees.append(d)

    def finalize_options(self):
        clean.finalize_options(self)

    def run(self):
        for clean_me in self._clean_me:
            try:
                print('removing', clean_me)
                os.unlink(clean_me)
            except Exception:
                pass
        for clean_tree in self._clean_trees:
            try:
                print('removing', clean_tree)
                shutil.rmtree(clean_tree)
            except Exception:
                pass


with open(os.path.join("README.md")) as f:
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
    packages=packages,
    install_requires= [
        "cffi >= 0.6",
        ],
    cmdclass={
        "build": BuildCommand,
        "install": InstallCommand,
        "clean": CleanCommand,
        },
    # for cffi
    zip_safe=False, 
    ext_package="skfftw",   
    )
