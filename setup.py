#! /usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='PyDashie',
    version='0.1dev',
    packages=['pydashie',],
    install_requires=[
        'Flask >= 0.10',
        'Coffeescript >= 1.0.8',
        'pyScss >= 1.2.0'
    ],
    entry_points={
      'console_scripts': ['pydashie = pydashie.main:run_sample_app']
    },
    license='MIT',
    long_description=open('README.rst').read(),
)
