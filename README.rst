paka.breadcrumbs
================
.. image:: https://travis-ci.org/PavloKapyshin/paka.breadcrumbs.svg?branch=master
    :target: https://travis-ci.org/PavloKapyshin/paka.breadcrumbs

``paka.breadcrumbs`` is a Python library with helpers (currently few data
structures) for breadcrumbs navigation building.


Features
--------
- Python 2.7 and 3.5 are supported
- PyPy (Python 2.7) is supported
- does not depend on any web framework
- does not require use of WSGI


Examples
--------
.. code-block:: pycon

    >>> from paka import breadcrumbs

Create breadcrumbs container:

.. code-block:: pycon

    >>> bcrumbs = breadcrumbs.Bread("Example Site")

Add crumbs for parent (with ``url_path``) and current (without ``url_path``,
as there is no need to link to yourself) pages:

.. code-block:: pycon

    >>> bcrumbs.add("Some category", url_path="/some/")
    >>> bcrumbs.add("Some page")

Now breadcrumbs container can be iterated over:

.. code-block:: pycon

    >>> [crumb.label for crumb in bcrumbs]
    ['Example Site', 'Some category', 'Some page']

And value you can put into ``<title></title>`` may be constructed
(it is actually an instance of ``markupsafe.Markup``):

.. code-block:: pycon

    >>> print(bcrumbs.get_title("<-"))
    Some page &lt;- Some category &lt;- Example Site


Installation
------------
Library is `available on PyPI <https://pypi.python.org/pypi/paka.breadcrumbs>`_,
you can use ``pip`` for installation:

.. code-block:: console

    $ pip install paka.breadcrumbs


Getting documentation
---------------------
Build HTML docs:

.. code-block:: console

    $ tox -e docs

View built docs:

.. code-block:: console

    $ sensible-browser .tox/docs/tmp/docs_html/index.html


Running tests
-------------
.. code-block:: console

    $ tox


Getting coverage
----------------
Collect info:

.. code-block:: console

    $ tox -e coverage

View HTML report:

.. code-block:: console

    $ sensible-browser .tox/coverage/tmp/cov_html/index.html


Checking code style
-------------------
Run code checkers:

.. code-block:: console

    $ tox -e checks
