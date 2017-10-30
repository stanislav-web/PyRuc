#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from setuptools import setup, find_packages

VERSION = '1.0.0'
try:
    LONG_DESCRIPTION = open('../README.md').read()
except FileNotFoundError:
    LONG_DESCRIPTION = 'Docker build images in progress...'

setup(name='PyRuc',

      # Versions should comply with PEP440.  For a discussion on single-sourcing
      # the version across setup.py and the project code, see
      # https://packaging.python.org/en/latest/single_source_version.html

      version=VERSION,

      description='User Access Control', long_description=LONG_DESCRIPTION,

      # The project's main homepage.
      url='https://github.com/stanislav-web/PyRuc',

      # Author details
      author='Stanislav WEB',
      author_email='stanisov@gmail.com',
      maintainer='Stanislav WEB',

      # You can just specify the packages manually here if your project is
      # simple. Or you can use find_packages().
      packages=find_packages(),
      include_package_data=True,

      # Choose your license
      license='GPL',
      # Unittests suite directory
      test_suite='tests',

      setup_requires=[
          'pytest-runner',
      ],

      # What does your project relate to?
      keywords=[
          'PyRus',
          'Python REST UAC',
          'UAC',
          'User Access Control',
      ],

      download_url='https://github.com/stanislav-web/PyRuc',

      # To provide executable scripts, use entry points in preference to the
      # "scripts" keyword. Entry points provide cross-platform support and allow
      # pip to create the appropriate form of executable for the target platform.
      entry_points={'console_scripts': [
          'coveralls = coveralls.cli:main'
      ]},

      install_requires=[line.rstrip('\n') for line in open('requirements.txt')],
      tests_require=[line.rstrip('\n') for line in open('requirements-dev.txt')],

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      # How mature is this project? Common values are
      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 5 - Production/Stable',

          # Language
          'Natural Language :: English',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Intended Audience :: Customer Service',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Legal Industry',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Religion',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Telecommunications Industry',

          # OS which support this package
          'Operating System :: MacOS',
          'Operating System :: Unix',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.

          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',

          # Specify the additional categories
          'Topic :: Internet :: WWW/HTTP :: Site Management',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
          'Topic :: Software Development :: User Interface'
      ])
