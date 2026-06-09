import datetime
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

# Mock MCDR to avoid import errors during doc build
from unittest.mock import MagicMock
mock_mcdr = MagicMock()
sys.modules["mcdreforged.plugin.si.server_interface"] = mock_mcdr
sys.modules["mcdreforged.api.all"] = mock_mcdr
sys.modules["mcdreforged"] = mock_mcdr

import resource_pack_server.constants as rps_consts  # noqa: E402

# -- Project information -----------------------------------------------------
project = "ResourcePackServer"
copyright = f"{datetime.datetime.now().year}, Mooling0602"
author = "Mooling0602"
release = rps_consts.PLUGIN_VERSION

# -- General configuration ---------------------------------------------------
RTD: bool = os.environ.get("READTHEDOCS", "").lower() == "true"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinxcontrib.jquery",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinx_design",
]

source_suffix = [".rst"]

templates_path = ["_templates"]

exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

html_static_path = ["../static"]

html_search_language = "en"

html_css_files = [
    "css/theme_overrides.css",
    "css/codeblock_tab.css",
    "css/rtd_addon.css",
]

html_js_files = [
    ("js/readthedoc-flyout.js", {"defer": "defer"}),
]

html_theme_options = {
    "navigation_depth": 6,
    "logo_only": True,
}

# -- Options for sphinx-intl -------------------------------------------------
language: str = os.environ.get("READTHEDOCS_LANGUAGE", "zh_CN")

locale_dirs = ["locales"]
gettext_compact = False

# -- Options for sphinx.ext.autodoc ------------------------------------------
autodoc_member_order = "bysource"
autodoc_inherit_docstrings = False

# -- Options for sphinx.ext.autosectionlabel ---------------------------------
autosectionlabel_prefix_document = True

# -- Options for sphinx.ext.intersphinx --------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
intersphinx_disabled_reftypes = ["std:*"]
intersphinx_timeout = 30
