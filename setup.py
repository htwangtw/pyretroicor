from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pyretroicor",
    description=("Python implementation of RETROICOR."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="BSD-3-clause",
    version="0.0.2",
    url="https://github.com/htwangtw/pyretroicor",
    author="Hao-Ting Wang",
    author_email="htwangtw@gmail.com",
    packages=["pyretroicor"],
    install_requires=["numpy>=1.18", "nibabel>=2.5"],
    keywords=["fmri", "physiology"],
    zip_safe=True,
    entry_points={
    "console_scripts": [
        "pyretroicor = pyretroicor.__main__:main",
        ]},
    )
