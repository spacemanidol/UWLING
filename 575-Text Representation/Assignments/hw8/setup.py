import glob
import os
import platform
import subprocess
import sys

from setuptools import Command, Extension, setup, find_packages
from setuptools.command.test import test as TestCommand


def define_extensions(cythonize=False):

    compile_args = ['-fopenmp',
                    '-ffast-math']

    # There are problems with illegal ASM instructions
    # when using the Anaconda distribution (at least on OSX).
    # This could be because Anaconda uses its own assembler?
    # To work around this we do not add -march=native if we
    # know we're dealing with Anaconda
    if 'anaconda' not in sys.version.lower():
        compile_args.append('-march=native')

    if cythonize:
        glove_cython = "glove/glove_cython.pyx"
        glove_metrics = "glove/metrics/accuracy_cython.pyx"
        glove_corpus = "glove/corpus_cython.pyx"
    else:
        glove_cython = "glove/glove_cython.c"
        glove_metrics = "glove/metrics/accuracy_cython.c"
        glove_corpus = "glove/corpus_cython.cpp"

    return [Extension("glove.glove_cython", [glove_cython],
                      extra_link_args=["-fopenmp"],
                      extra_compile_args=compile_args),
            Extension("glove.metrics.accuracy_cython",
                      [glove_metrics],
                      extra_link_args=["-fopenmp"],
                      extra_compile_args=compile_args),
            Extension("glove.corpus_cython", [glove_corpus],
                      language='C++',
                      libraries=["stdc++"],
                      extra_link_args=compile_args,
                      extra_compile_args=compile_args)]


def set_gcc():
    """
    Try to find and use GCC on OSX for OpenMP support.
    """

    # For macports and homebrew
    patterns = ['/opt/local/bin/gcc-mp-[0-9].[0-9]',
                '/opt/local/bin/gcc-mp-[0-9]',
                '/usr/local/bin/gcc-[0-9].[0-9]',
                '/usr/local/bin/gcc-[0-9]']

    if 'darwin' in platform.platform().lower():

        gcc_binaries = []
        for pattern in patterns:
            gcc_binaries += glob.glob(pattern)
        gcc_binaries.sort()

        if gcc_binaries:
            _, gcc = os.path.split(gcc_binaries[-1])
            os.environ["CC"] = gcc

        else:
            raise Exception('No GCC available. Install gcc from Homebrew '
                            'using brew install gcc.')


class Cythonize(Command):
    """
    Compile the extension .pyx files.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        import Cython
        from Cython.Build import cythonize

        cythonize(define_extensions(cythonize=True))


class Clean(Command):
    """
    Clean build files.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        pth = os.path.dirname(os.path.abspath(__file__))

        subprocess.call(['rm', '-rf', os.path.join(pth, 'build')])
        subprocess.call(['rm', '-rf', os.path.join(pth, '*.egg-info')])
        subprocess.call(['find', pth, '-name', '*.pyc', '-type', 'f', '-delete'])
        subprocess.call(['rm', os.path.join(pth, 'glove', 'corpus_cython.so')])
        subprocess.call(['rm', os.path.join(pth, 'glove', 'glove_cython.so')])

setup(
    name='glove_python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    cmdclass={'cythonize': Cythonize, 'clean': Clean},
    ext_modules=define_extensions()
)
