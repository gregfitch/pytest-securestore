#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-securestore',
    version='0.2.0',
    author='Greg Fitch',
    author_email='greg@openstax.org',
    maintainer='Greg Fitch',
    maintainer_email='greg@openstax.org',
    license='MIT',
    url='https://github.com/gregfitch/pytest-securestore',
    description='An encrypted password store for use within pytest cases',
    long_description=read('README.rst'),
    py_modules=['pytest_securestore'],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'pytest>=3.7.0',
        'PyYAML>=3.13',
        'pyAesCrypt>=0.4.2', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'securestore = pytest_securestore',
        ],
    },
)
