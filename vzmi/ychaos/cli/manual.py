from argparse import ArgumentParser, Namespace
from io import StringIO
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.markdown import Markdown

from vzmi.ychaos.utils.argparse import SubCommand

__all__ = ["Manual"]


class Manual(SubCommand):
    """
    Used to print the manual for the entire CLI command.

    ```
    $ ychaos manual -h
    usage: ychaos manual [-h] [-f FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Print YChaos CLI Manual to a file
    ```
    """

    name = "manual"
    help = "Print the manual for YChaos CLI"

    _exitcode = 0

    def __init__(self, **kwargs):
        assert kwargs.pop("cls") == self.__class__

        self.app = kwargs.pop("app")
        self.console: Console = self.app.console

        self.file: Optional[Path] = kwargs.pop("file", None)

    @classmethod
    def build_parser(cls, parser: ArgumentParser) -> ArgumentParser:
        parser.add_argument(
            "-f",
            "--file",
            type=Path,
            help="Print YChaos CLI Manual to a file",
            required=False,
        )

        return parser

    def set_exitcode(self, exitcode=0):
        self._exitcode = exitcode

    def do_print_manual_entry(self):
        tempfile = StringIO()
        for cmd, msg in self.app.manual_entry().items():
            tempfile.write(
                "{header} {cmd}".format(header="#" * len(cmd.split()), cmd=cmd)
            )
            tempfile.write("\n")
            tempfile.write("```\n")
            tempfile.write(msg)
            tempfile.write("\n```\n")

        if self.file is not None:
            try:
                self.file.write_text(tempfile.getvalue())
                self.console.log(
                    "{prog} manual entry written to {file}".format(
                        prog=self.app.settings.PROG, file=self.file
                    )
                )
            except FileNotFoundError as file_not_found_error:
                self.set_exitcode(1)
                self.console.print(
                    ":mag: {file} [italic]not found[/italic]".format(
                        file=str(self.file)
                    ),
                    style="indian_red",
                )
            except IsADirectoryError as is_a_directory_error:
                self.set_exitcode(1)
                self.console.print(
                    ":file_folder: The input path ({path}) is not a valid testplan file".format(
                        path=self.file
                    )
                )
        else:
            self.console.print(Markdown(tempfile.getvalue()))

    @classmethod
    def main(cls, args: Namespace) -> Any:  # pragma: no cover
        manual = Manual(**vars(args))
        manual.do_print_manual_entry()

        return manual._exitcode