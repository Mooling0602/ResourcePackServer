Installation
============

ResourcePackServer can run in two modes: as a **standalone HTTP server** or as an **MCDReforged plugin**.

You only need to choose **one** mode that fits your setup.

----

Standalone Mode
----------------

Download the ``.pyz`` file from `GitHub Releases <https://github.com/Mooling0602/ResourcePackServer/releases>`__,
then run it directly:

.. code-block:: bash

    python ResourcePackServer-v0.1.0.pyz --port 8080 --pack-dir ./resource_packs

Or install from source:

.. code-block:: bash

    git clone https://github.com/Mooling0602/ResourcePackServer.git
    cd ResourcePackServer
    pip install .
    python -m resource_pack_server --port 8080 --pack-dir ./resource_packs

See :doc:`/contents/usage/index` for more CLI options.

----

MCDReforged Plugin Mode
-----------------------

Download the ``.pyz`` file from `GitHub Releases <https://github.com/Mooling0602/ResourcePackServer/releases>`__
and place it into your MCDR ``plugins/`` directory.

The plugin will auto-load. Use ``!!rps status`` to verify.

Dependencies
------------

This plugin depends on:

* MCDReforged >= 2.14.1

No other external dependencies are required (stdlib-only HTTP server).

.. note::

    Make sure MCDReforged is installed and configured first.
    Visit the `MCDR docs <https://docs.mcdreforged.com>`__ for guidance.
