"""Global references to MCDR objects, set during on_load."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcdreforged.api.all import PluginServerInterface, Metadata

server: "PluginServerInterface"
metadata: "Metadata"


def _init() -> None:
    global server, metadata
    from mcdreforged.api.all import PluginServerInterface

    psi = PluginServerInterface.psi_opt()
    if psi is not None:
        server = PluginServerInterface.psi()
        metadata = server.get_self_metadata()
    else:
        import os
        import warnings
        warnings.warn(
            f"Loading {os.path.basename(__file__)} outside MCDR environment",
            stacklevel=3,
        )


_init()
