#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)

reqs = [str(ir.req) for ir in install_reqs]


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-securestore',
    version='0.1.2',
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
    install_requires=reqs,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'securestore = pytest_securestore',
        ],
    },
)
