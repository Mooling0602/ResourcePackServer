import unittest

from resource_pack_server.cli.cli_entrypoint import create_parser


class CliParserTest(unittest.TestCase):
    def test_merge_flag_defaults_to_enabled(self) -> None:
        args = create_parser().parse_args([])

        self.assertIs(args.merge, True)

    def test_no_merge_flag_disables_merge(self) -> None:
        args = create_parser().parse_args(["--no-merge"])

        self.assertIs(args.merge, False)

    def test_merge_flag_enables_merge(self) -> None:
        args = create_parser().parse_args(["--merge"])

        self.assertIs(args.merge, True)


if __name__ == "__main__":
    unittest.main()
