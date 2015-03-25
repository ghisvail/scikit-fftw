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
from setuptools.command.test import test
from setuptools import setup, find_packages
import os
import shutil
import sys


packages = find_packages(exclude=['docs', 'tests'])


SETUP_REQUIRES_ERROR = (
    "Requested setup command that needs 'setup_requires' while command line "
    "arguments implied a side effect free command or option."
)

NO_SETUP_REQUIRES_ARGUMENTS = [
    "-h", "--help",
    "-n", "--dry-run",
    "-q", "--quiet",
    "-v", "--verbose",
    "-v", "--version",
    "--author",
    "--author-email",
    "--classifiers",
    "--contact",
    "--contact-email",
    "--description",
    "--egg-base",
    "--fullname",
    "--help-commands",
    "--keywords",
    "--licence",
    "--license",
    "--long-description",
    "--maintainer",
    "--maintainer-email",
    "--name",
    "--no-user-cfg",
    "--obsoletes",
    "--platforms",
    "--provides",
    "--requires",
    "--url",
    "clean",
    "egg_info",
    "register",
    "sdist",
    "upload",
]


# Access to cffi extension
def get_ext_modules():
    import skfftw.bindings.cffi as cffi
    return [cffi.ffi.verifier.get_extension()]


# Build command
class BuildCommand(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)

class DummyBuildCommand(build):
    def run(self):
        raise RuntimeError(SETUP_REQUIRES_ERROR)

# Intall command
class InstallCommand(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)

class DummyInstallCommand(install):
    def run(self):
        raise RuntimeError(SETUP_REQUIRES_ERROR)


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


# from py.test documentation
class TestCommand(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def keywords_with_side_effects(argv):
    def is_short_option(argument):
        """Check whether a command line argument is a short option."""
        return len(argument) >= 2 and argument[0] == '-' and argument[1] != '-'

    def expand_short_options(argument):
        """Expand combined short options into canonical short options."""
        return ('-' + char for char in argument[1:])

    def argument_without_setup_requirements(argv, i):
        """Check whether a command line argument needs setup requirements."""
        if argv[i] in NO_SETUP_REQUIRES_ARGUMENTS:
            # Simple case: An argument which is either an option or a command
            # which doesn't need setup requirements.
            return True
        elif (is_short_option(argv[i]) and
              all(option in NO_SETUP_REQUIRES_ARGUMENTS
                  for option in expand_short_options(argv[i]))):
            # Not so simple case: Combined short options none of which need
            # setup requirements.
            return True
        elif argv[i - 1:i] == ['--egg-base']:
            # Tricky case: --egg-info takes an argument which should not make
            # us use setup_requires (defeating the purpose of this code).
            return True
        else:
            return False

    if all(argument_without_setup_requirements(argv, i)
           for i in range(1, len(argv))):
        return {
            "cmdclass": {
                "build": DummyBuildCommand,
                "install": DummyInstallCommand,
                "clean": CleanCommand,
                "test": TestCommand,
            }
        }
    else:
        return {
            "setup_requires": ["cffi"],
            "cmdclass": {
                "build": BuildCommand,
                "install": InstallCommand,
                "clean": CleanCommand,
                "test": TestCommand,
            },
            "ext_package": "skfftw",
        }


with open(os.path.join("README.md")) as f:
    long_description = f.read()


setup(
    name="scikit-fftw",
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
    # for cffi
    zip_safe=False, 
    **keywords_with_side_effects(sys.argv)   
    )
