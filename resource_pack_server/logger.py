import functools
import logging
import sys


LOG_FORMATTER = logging.Formatter(
    "[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _create_logger() -> logging.Logger:
    from resource_pack_server.constants import PLUGIN_ID

    logger = logging.getLogger(PLUGIN_ID)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LOG_FORMATTER)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


@functools.lru_cache
def get() -> logging.Logger:
    try:
        from mcdreforged.api.all import ServerInterface

        psi = ServerInterface.psi_opt()
        if psi is not None:
            return psi.logger
    except Exception:
        pass
    return _create_logger()
