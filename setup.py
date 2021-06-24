"""
    Setup file for FullereneDataPraser.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.0.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

from setuptools import setup
from setuptools import Extension
USE_CYTHON = False
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ModuleNotFoundError:
    USE_CYTHON = False

ext = '.pyx'if USE_CYTHON else'.cpp'


if __name__ == "__main__":
    try:
        import numpy

        extensions = [  # *find_pyx()
            Extension("fullerenedatapraser.graph.algorithm.dual", ["src/fullerenedatapraser/graph/algorithm/dual" + ext],
                      include_dirs=[numpy.get_include(), "e3rdpackage/boost"],
                      language="c++",
                      # libraries=[],
                      # library_dirs=[],
                      ),
        ]
        setup(use_scm_version={"version_scheme": "no-guess-dev"},
              ext_modules=extensions if not USE_CYTHON else cythonize(extensions, language_level=3),
              # include_dirs=[numpy.get_include()],
              # packages=find_packages()
              )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
