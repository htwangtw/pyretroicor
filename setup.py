#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["numpy>=1.18", "nibabel>=2.5"]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Hao-Ting Wang",
    author_email='htwangtw@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python implementation of RETROICOR.",
    entry_points={
        'console_scripts': [
            'pyretroicor=pyretroicor.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD-3-clause",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=["fmri", "physiology"],
    name='pyretroicor',
    packages=find_packages(include=['pyretroicor', ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/htwangtw/pyretroicor',
    version='0.0.3',
    zip_safe=False,
)
