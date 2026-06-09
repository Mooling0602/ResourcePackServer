Installation
============

ResourcePackServer can run in two modes: as a **standalone HTTP server** or as an **MCDReforged plugin**.

You only need to choose **one** mode that fits your setup.

----

Standalone Mode (install from source)
--------------------------------------

Clone the repository and install:

.. code-block:: bash

    git clone https://github.com/Mooling0602/ResourcePackServer.git
    cd ResourcePackServer
    pip install .

Or install with uv:

.. code-block:: bash

    git clone https://github.com/Mooling0602/ResourcePackServer.git
    cd ResourcePackServer
    uv pip install .

Then run:

.. code-block:: bash

    python -m resource_pack_server --port 8080 --pack-dir ./resource_packs

See :doc:`/contents/usage/index` for more CLI options.

----

MCDReforged Plugin Mode
-----------------------

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/Mooling0602/ResourcePackServer.git

2. Copy the ``src/resource_pack_server/`` folder into your MCDR ``plugins/`` directory.

3. The plugin will auto-load. Use ``!!rps status`` to verify.

Dependencies
------------

This plugin depends on:

* MCDReforged >= 2.14.1

No other external dependencies are required (stdlib-only HTTP server).

.. note::

    Make sure MCDReforged is installed and configured first.
    Visit the `MCDR docs <https://docs.mcdreforged.com>`__ for guidance.
