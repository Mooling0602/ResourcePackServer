Installation
============

ResourcePackServer can run in two modes: as a **standalone HTTP server** or as an **MCDReforged plugin**.

You only need to choose **one** mode that fits your setup.

----

Standalone Mode (pip install)
-----------------------------

Install from source or PyPI (future):

.. code-block:: bash

    pip install resource-pack-server

Or install with uv:

.. code-block:: bash

    uv add resource-pack-server

Then run:

.. code-block:: bash

    python -m resource_pack_server --port 8080 --pack-dir ./resource_packs

See :doc:`/contents/usage/index` for more CLI options.

----

MCDReforged Plugin Mode
-----------------------

1. Install the plugin via MCDR command:

.. code-block::

    !!MCDR plg install resource_pack_server --confirm

2. Alternatively, download the ``.mcdr`` package from
   `GitHub Releases <https://github.com/Mooling0602/ResourcePackServer/releases>`__
   and place it into the ``plugins/`` directory.

3. The plugin will auto-load. Use ``!!rps status`` to verify.

Dependencies
------------

This plugin depends on:

* `MCDReforged <https://github.com/MCDReforged/MCDReforged>`__ >= 2.0.0

No other external dependencies are required (stdlib-only HTTP server).

.. note::

    Make sure MCDReforged is installed and configured first.
    Visit the `MCDR docs <https://docs.mcdreforged.com>`__ for guidance.
