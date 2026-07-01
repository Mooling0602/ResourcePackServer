Usage
=====

ResourcePackServer hosts ``.zip`` resource pack files over HTTP. Minecraft clients can download packs via the ``resource-pack`` field in ``server.properties``.

Quick Start
-----------

**1. Prepare your packs**

Place ``.zip`` resource pack files in a directory (default: ``./resource_packs``):

.. code-block::

    resource_packs/
    ├── vanilla_tweaks.zip
    ├── xray_ultimate.zip
    └── custom_sounds.zip

**2. Start the server**

.. code-block:: bash

    python -m resource_pack_server --port 8080 --pack-dir ./resource_packs

**3. Browse the pack list**

Open ``http://localhost:8080/`` in a browser. You'll see a table of all packs with their SHA1 hashes.

**4. Configure Minecraft**

Edit ``server.properties``:

.. code-block:: properties

    resource-pack=http://yourserver:8080/merged.zip
    resource-pack-sha1=abc123...  (copy from the web page)

The merged pack combines all your packs into one zip. See :doc:`/contents/config/index` for merge options.

----

Standalone CLI Arguments
------------------------

.. code-block:: bash

    python -m resource_pack_server [OPTIONS]

.. list-table::
   :header-rows: 1

   * - Argument
     - Default
     - Description
   * - ``--host``
     - ``0.0.0.0``
     - IP address to bind
   * - ``--port``
     - ``8080``
     - Port to listen on
   * - ``--pack-dir``
     - ``./resource_packs``
     - Directory containing ``.zip`` packs
   * - ``--public-url``
     - *(empty)*
     - Public URL prefix for external access
   * - ``--merge`` / ``--no-merge``
     - ``--merge``
     - Enable/disable merged pack generation
   * - ``--priority``
     - *(empty)*
     - Pack filenames in merge priority order (highest first)
   * - ``--debug``
     - ``false``
     - Enable debug logging
   * - ``--version``
     -
     - Show version and exit

----

Merged Pack
-----------

Minecraft only accepts **one** resource pack URL. ResourcePackServer solves this by merging multiple packs into a single ``merged.zip``, available at ``/merged.zip``.

* Packs are merged in **priority order** (configurable via ``--priority`` or the config file)
* Higher-priority packs **override** lower-priority ones on file-level
* The ``pack.mcmeta`` description combines all pack descriptions
* The ``pack.png`` icon is taken from the highest-priority pack that has one
* The merged pack is **cached** and automatically regenerated when any source pack changes
* Use ``--no-merge`` to disable ``/merged.zip`` and list individual packs only

Example with priority:

.. code-block:: bash

    python -m resource_pack_server \
        --port 8080 \
        --priority "base_pack.zip" "addon.zip" "extra_sounds.zip"

----

HTTP Endpoints
--------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Description
   * - ``GET /``
     - HTML page listing all packs and the merged pack
   * - ``GET /merged.zip``
     - Download the merged resource pack
   * - ``GET /<filename>.zip``
     - Download an individual pack

Each ``.zip`` response includes these headers:

* ``Content-Type: application/zip``
* ``X-Resource-Pack-SHA1: <sha1>`` — the SHA1 hash Minecraft needs
* ``Content-Disposition: attachment``
* ``Cache-Control: public, max-age=3600``
