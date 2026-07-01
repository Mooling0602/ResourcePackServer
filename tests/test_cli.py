from resource_pack_server.cli.cli_entrypoint import create_parser


def test_merge_flag_defaults_to_enabled() -> None:
    args = create_parser().parse_args([])

    assert args.merge is True


def test_no_merge_flag_disables_merge() -> None:
    args = create_parser().parse_args(["--no-merge"])

    assert args.merge is False


def test_merge_flag_enables_merge() -> None:
    args = create_parser().parse_args(["--merge"])

    assert args.merge is True
