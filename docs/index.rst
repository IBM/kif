===
KIF
===

   :Version: |version|
   :Date: |today|

Welcome to the documentation of KIF_!

KIF is a knowledge integration framework based on Wikidata_.

It written in Python and is released as open-source (see :doc:`license`).

First time here? See :doc:`quickstart`.  Or go straight to
:doc:`reference/index`.

.. _KIF: https://github.com/ibm/kif
.. _Wikidata: https://www.wikidata.org/

Installation
============

Latest stable release:

.. code-block:: shell

   $ pip install kif-lib

Latest development version:

.. code-block:: shell

   $ git clone https://github.com/IBM/kif.git
   $ cd kif; pip install -e .


Hello world!
============

Prints an arbitrary statement from `Wikidata <https://www.wikidata.org/>`_:

.. code-block:: python

   from kif_lib import *      # import KIF namespacee
   kb = Store('wikidata')     # create a store pointing to Wikidata
   print(next(kb.filter()))   # obtain and print one arbitrary statement


Citation
========

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares,
Sandro R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva,
Renato Cerqueira. `"KIF: A Wikidata-Based Framework for Integrating
Heterogeneous Knowledge Sources" <https://arxiv.org/abs/2403.10304>`_,
arXiv:2403.10304, 2024.

.. toctree::
   :maxdepth: 1
   :hidden:

   quickstart
   reference/index
   license
