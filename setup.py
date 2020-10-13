#! /usr/bin/env python
import sys
try:
    from setuptools import setup
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAVE_SETUPTOOLS = False


VERSION = '0.1.3'

setup_kwargs = {
    "version": VERSION,
    "description": ('A fast, drop-in replacement for pygments `get_*()` and `guess_*()` funtions'),
    "license": 'BSD 3-clause',
    "author": 'The xonsh developers',
    "author_email": 'xonsh@googlegroups.com',
    "url": 'https://github.com/xonsh/pygments-cache',
    "download_url": "https://github.com/xonsh/pygments-cache/zipball/" + VERSION,
    "classifiers": [
        "License :: OSI Approved",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Utilities",
        ],
    "zip_safe": False,
    "data_files": [("", ['LICENSE', 'README.rst']),],
    }
if HAVE_SETUPTOOLS:
    setup_kwargs["install_requires"] = ['pygments']


if __name__ == '__main__':
    setup(
        name='pygments_cache',
        py_modules=['pygments_cache'],
        long_description=open('README.rst').read(),
        **setup_kwargs
)
