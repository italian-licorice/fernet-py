#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

is_py3 = sys.version_info >= (3,)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'fernet',
]

requires = [
#    'M2Crypto>=0.21.1',
    'py>=1.4.18',
    'python-dateutil>=2.2',  # TODO only used with tests
    'should-dsl>=2.1.2',  # TODO only used with tests
    'six>=1.4.1'  # TODO NOT used
]

if is_py3:
    requires.append('pycryptodome')
else:  # assume is_py2
    requires.append('pycryptodome==3.7.2')  # TODO review, see if there is a later one

with open('README.md') as f:
    readme = f.read()
with open('HISTORY') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='fernet',
    version='1.0.1',
    description='Delicious HMAC Digest(if) authentication and AES-128-CBC encryption.',
    long_description=readme + '\n\n' + history,
    author='Scott Persinger',
    author_email='scottp@heroku.com',
    url='https://github.com/heroku/fernet-py',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'requests': 'requests'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
