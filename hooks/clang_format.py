#!/usr/bin/env python3
"""Wrapper script for clang-format"""
###############################################################################
import sys

from hooks.utils import FormatterCmd


class ClangFormatCmd(FormatterCmd):
    """Class for the ClangFormat command."""

    command = "clang-format"
    lookbehind = "clang-format version "

    def __init__(self, args):
        super().__init__(self.command, self.lookbehind, args)
        self.check_installed()
        known_args = self.parse_args(args)
        self.edit_in_place = "-i" in self.args
        self.silent = known_args.silent

    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('--silent', '-s', action='store_true', dest='silent')
        return parser

    def run(self):
        """Run clang-format. Error if diff is incorrect."""
        for filename in self.files:
            self.compare_to_formatted(filename)
        if self.returncode != 0:
            if not self.silent:
                sys.stdout.write(self.stderr)
            sys.exit(self.returncode)


def main(argv=None):
    cmd = ClangFormatCmd(argv)
    cmd.run()


if __name__ == "__main__":
    main()
