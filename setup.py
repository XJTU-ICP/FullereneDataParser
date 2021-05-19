"""
    Setup file for FullereneDataPraser.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.0.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import os

# from setuptools import Extension
from Cython.Build import cythonize
from setuptools import setup, find_packages


def find_pyx(path='.'):
    pyx_files = []
    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith('.pyx'):
                pyx_files.append(os.path.join(root, fname))
    return pyx_files


if __name__ == "__main__":
    try:
        import numpy

        extensions = [*find_pyx()
                      # Extension("fullerenedatapraser.graph.dual", ["src/fullerenedatapraser/graph/dual/*.pyx"],
                      # include_dirs=[numpy.get_include()],
                      # libraries=[],c
                      # library_dirs=[],
                      # ),
                      ]
        setup(use_scm_version={"version_scheme": "no-guess-dev"},
              ext_modules=cythonize(extensions, language_level=3),
              include_dirs=[numpy.get_include()],
              packages=find_packages()
              )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
