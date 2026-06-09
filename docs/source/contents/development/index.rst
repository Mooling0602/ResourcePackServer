Development
===========

This page is for developers who want to contribute to ResourcePackServer or build their own tooling around it.

Project Structure
-----------------

.. code-block::

    ResourcePackServer/
    ├── main.py                              # Root entry point
    ├── pyproject.toml                       # Project metadata & dependencies
    ├── resource_pack_server/
    │   ├── __init__.py
    │   ├── __main__.py                      # python -m entry point
    │   ├── server.py                        # HTTP server core (shared)
    │   ├── config.py                        # Configuration classes
    │   ├── logger.py                        # Dual-mode logger
    │   ├── constants.py                     # Plugin constants
    │   ├── hash_utils.py                    # SHA1 hashing utilities
    │   ├── pack_merger.py                   # Multi-pack merge logic
    │   ├── cli/
    │   │   ├── __init__.py
    │   │   └── cli_entrypoint.py            # Standalone CLI (argparse)
    │   └── mcdr/
    │       ├── __init__.py
    │       ├── mcdr_globals.py              # MCDR global references
    │       └── mcdr_entrypoint.py           # MCDR plugin hooks
    └── docs/                                # Sphinx documentation

Architecture
------------

**Dual-Mode Design**

ResourcePackServer follows the same pattern as `PrimeBackup <https://github.com/TISUnion/PrimeBackup>`__:

1. **Environment detection**: ``ServerInterface.psi_opt()`` returns ``None`` → standalone mode
2. **Shared core**: ``server.py``, ``pack_merger.py``, ``config.py`` are mode-agnostic
3. **Dual entrypoints**: ``cli/cli_entrypoint.py`` for CLI, ``mcdr/mcdr_entrypoint.py`` for MCDR
4. **Logger**: Detects MCDR environment and uses ``psi.logger`` or creates its own

**Pack Merging**

``pack_merger.py`` implements deterministic multi-pack merging:

* Packs are read into memory as ``{filename: bytes}`` dicts
* Merged from lowest to highest priority → higher priority overwrites
* ``pack.mcmeta`` is special-cased: highest-priority metadata is the base; ``description`` fields from all packs are concatenated
* ``pack.png`` is taken from the first pack that has one (highest priority)
* Result is cached; cache is invalidated when any source pack's ``mtime`` changes

Building Docs
-------------

.. code-block:: bash

    # Install doc dependencies
    pip install -r docs/requirements.docs.txt

    # Build (default language: zh_CN)
    cd docs
    ./build_docs.sh

    # Build English version
    ./build_docs.sh en_US

    # Live preview with auto-reload
    sphinx-autobuild source build/html

    # Extract/update translation strings
    make gettext
    sphinx-intl update -p build/gettext -l zh_CN -l en_US

Running Tests
-------------

.. code-block:: bash

    pytest tests/
