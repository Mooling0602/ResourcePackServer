from resource_pack_server.config import RpsConfig


def test_default_config_instances_do_not_share_nested_state() -> None:
    first = RpsConfig.get_default()
    second = RpsConfig.get_default()

    first.server.port = 9000
    first.merge.pack_priority.append("first.zip")

    assert second.server.port == 8080
    assert second.merge.pack_priority == []


def test_cached_config_get_returns_independent_copy() -> None:
    first = RpsConfig.get()
    first.merge.pack_priority.append("cached.zip")

    second = RpsConfig.get()

    assert second.merge.pack_priority == []
