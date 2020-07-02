===========
PyRETROICOR
===========


.. image:: https://img.shields.io/pypi/v/pyretroicor.svg
        :target: https://pypi.python.org/pypi/pyretroicor

.. image:: https://img.shields.io/travis/htwangtw/pyretroicor.svg
        :target: https://travis-ci.com/htwangtw/pyretroicor

.. .. image:: https://readthedocs.org/projects/pyretroicor/badge/?version=latest
..         :target: https://pyretroicor.readthedocs.io/en/latest/?badge=latest
..         :alt: Documentation Status


.. image:: https://pyup.io/repos/github/htwangtw/pyretroicor/shield.svg
     :target: https://pyup.io/repos/github/htwangtw/pyretroicor/
     :alt: Updates



Python implementation of RETROICOR (Glover et al., 2000) - physiology regressors for fMRI preprocessing.

Dependencies
------------

The required dependencies to use the software are:

* Python >= 3.5
* NumPy >= 1.18
* Nibabel >= 2.5

Install
-------

First make sure you have installed all the dependencies listed above.
Then you can install pyretroicor by running the following command in
a command prompt::

    pip install -U --user pyretroicor

Reference
---------

Glover, G. H., Li, T. Q., & Ress, D. (2000). Image‐based method for retrospective correction of physiological motion effects in fMRI: RETROICOR. Magnetic Resonance in Medicine: An Official Journal of the International Society for Magnetic Resonance in Medicine, 44(1), 162-167.

MATLAB implementation from: https://github.com/mkassinopoulos/PRF_estimation


Support
-------
Please use `GitHub issues <https://github.com/htwangtw/pyretroicor/issues>`_ for questions, bug reports or feature requests.


License
-------
This project is licensed under `BSD-3-Clause <https://opensource.org/licenses/BSD-3-Clause>`_.
