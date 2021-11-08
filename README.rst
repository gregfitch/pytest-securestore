==================
pytest-securestore
==================

.. image:: https://img.shields.io/pypi/v/pytest-securestore.svg
    :target: https://pypi.org/project/pytest-securestore
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-securestore.svg
    :target: https://pypi.org/project/pytest-securestore
    :alt: Python versions

.. image:: https://travis-ci.org/gregfitch/pytest-securestore.svg?branch=master
    :target: https://travis-ci.org/gregfitch/pytest-securestore
    :alt: See Build Status on Travis CI

An encrypted password store for use within pytest cases

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

Provide a way to include encrypted data in a test repo so project team members may share test account data (logins, password, keys) while only having to share the decryption password and store filename outside of the repository.


Requirements
------------

SecureStore makes use of PyAesCrypt by Marco Bellaccini:
"pyAesCrypt is a Python 3 file-encryption module and script that uses AES256-CBC to encrypt/decrypt files and binary streams."

Files must be formatted as YAML data (`YAML Reference`_) and will be loaded into a Python dictionary.


Installation
------------

You can install "pytest-securestore" via `pip`_ from `PyPI`_::

    $ pip install pytest-securestore


Usage
-----

Generic YAML layout:

.. code-block:: yaml

    ---
    # a comment
    a_general_user:
        username: the_username
        password: a_password
        usertype: some_defined_type
    ...

Encrypt the YAML file (`file encryption`_):

.. code-block:: yaml

    import os
    import pyAesCrypt

    buffer_size = 64 * 1024  # 64K
    filename = os.getenv('SECURE_STORE_FILE')
    password = os.getenv('SECURE_STORE_PASSWORD')
    pyAesCrypt.encryptFile("/path/to/yaml/file", filename, password, buffer_size)

Include the encrypted file in the repository.

Within a test:
*Note: A ``'password'`` key triggers an internal class ``Secret`` to obscure
passwords stored in the yaml. Use ``.value`` to get the plain text back.*

.. code-block:: yaml

    def test_get_store_values(store):
        # one way to get the value
        user = store.get('a_general_user')
        username = user['username']
        # or another
        username = store.get('a_general_user').get('username')
        # or even another
        password = store.get('a_general_user')['password'].value
        # or
        user_type = store['a_general_user']['usertype']
        # ...
        some_site.log_in(username, password, user_type)

And to kick it off:

CLI with environment variables:

.. code-block:: bash

    $ pytest --secure-store-filename=$SECURE_STORE_FILE --secure-store-password=$SECURE_STORE_PASSWORD

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-securestore" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/gregfitch/pytest-securestore/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`YAML Reference`: https://yaml.org/refcard.html
.. _`file encryption`: https://pypi.org/project/pyAesCrypt/#module-usage-example
