Commands (MCDR Mode)
====================

When running as an MCDReforged plugin, ResourcePackServer registers in-game commands. The default command prefix is ``!!rps``.

.. note::

    Command prefix and permission level can be changed in the config file.
    See :doc:`/contents/config/index`.

Command Reference
-----------------

.. list-table::
   :header-rows: 1

   * - Command
     - Permission
     - Description
   * - ``!!rps``
     - User
     - Show plugin version and available subcommands
   * - ``!!rps help``
     - User
     - Show help message with all subcommands
   * - ``!!rps list``
     - User
     - List all resource packs and their SHA1 hashes
   * - ``!!rps status``
     - User
     - Show HTTP server status and merged pack info
   * - ``!!rps merge rebuild``
     - Admin
     - Force rebuild the merged pack (clears cache)
   * - ``!!rps reload``
     - Admin
     - Reload the plugin (re-reads config and restarts HTTP server)

----

Example Usage
-------------

.. code-block::

    # Check server status
    !!rps status
    > [RPS] Server running on 0.0.0.0:8080
    > Pack dir: ./resource_packs
    > Merged pack: 12.3 MB, SHA1=a1b2c3d4e5f6...

    # List available packs
    !!rps list
    > [RPS] vanilla_tweaks.zip (5.2 MB, a1b2c3d4…)
    > custom_sounds.zip (3.1 MB, f6e5d4c3…)
    > default_xray.zip (4.0 MB, b2a1c3d4…)

    # Force rebuild merged pack
    !!rps merge rebuild
    > [RPS] Merged pack rebuilt: 12.3 MB, SHA1=a1b2c3d4e5f6...
