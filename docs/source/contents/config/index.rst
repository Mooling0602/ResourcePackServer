Configuration
=============

.. note::

    In **standalone mode**, use CLI arguments (see :doc:`/contents/usage/index`).
    In **MCDR mode**, configuration is loaded from MCDR's config file at ``config/resource_pack_server/config.json``.

Configuration File
------------------

The config file is auto-generated on first load. Default path (MCDR mode): ``config/resource_pack_server/config.json``.

Default config:

.. code-block:: json

    {
        "enabled": true,
        "debug": false,
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "pack_dir": "./resource_packs",
            "public_url": ""
        },
        "command": {
            "enabled": true,
            "prefix": "!!rps",
            "permission_level": 1
        },
        "merge": {
            "enabled": true,
            "pack_priority": []
        }
    }

Top-Level Fields
----------------

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Default
     - Description
   * - ``enabled``
     - ``bool``
     - ``true``
     - Set to ``false`` to disable the plugin entirely
   * - ``debug``
     - ``bool``
     - ``false``
     - Enable debug logging

Server Configuration
--------------------

``server`` section:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Default
     - Description
   * - ``host``
     - ``str``
     - ``0.0.0.0``
     - HTTP server bind address
   * - ``port``
     - ``int``
     - ``8080``
     - HTTP server port
   * - ``pack_dir``
     - ``str``
     - ``./resource_packs``
     - Directory containing ``.zip`` resource pack files
   * - ``public_url``
     - ``str``
     - *(empty)*
     - Public-facing URL (used if server is behind a proxy)

Command Configuration
---------------------

``command`` section (MCDR mode only):

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Default
     - Description
   * - ``enabled``
     - ``bool``
     - ``true``
     - Whether to register MCDR commands
   * - ``prefix``
     - ``str``
     - ``!!rps``
     - Command prefix
   * - ``permission_level``
     - ``int``
     - ``1``
     - Minimum MCDR permission level for commands

Merge Configuration
-------------------

``merge`` section:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Default
     - Description
   * - ``enabled``
     - ``bool``
     - ``true``
     - Enable the ``/merged.zip`` endpoint
   * - ``pack_priority``
     - ``list[str]``
     - ``[]``
     - Ordered list of pack filenames (highest priority first). Unlisted packs are appended alphabetically.

Example: priority ordering
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "merge": {
            "enabled": true,
            "pack_priority": [
                "vanilla_tweaks.zip",
                "custom_sounds.zip",
                "default_xray.zip"
            ]
        }
    }

With this config, ``vanilla_tweaks.zip`` has the highest priority — its assets override any conflicting assets from lower-priority packs.
