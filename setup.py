from setuptools import setup

setup(
    name="pyretroicor",
    description=("Python implementation of RETROICOR."),
    license="BSD-3-clause",
    version="0.0.1",
    url="https://github.com/htwangtw/pyretroicor",
    author="Hao-Ting Wang",
    packages=["pyretroicor"],
    install_requires=["numpy>=1.18"],
    keywords=["fmri", "physiology"],
    zip_safe=True,
    entry_points={
    "console_scripts": [
        "pyretroicor = pyretroicor.__main__:main",
        ]},
    )
