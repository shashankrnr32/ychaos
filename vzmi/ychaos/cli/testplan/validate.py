from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, List

from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel

from vzmi.ychaos.testplan.validator import TestPlanValidator
from vzmi.ychaos.utils.argparse import SubCommand

__all__ = ["TestPlanValidatorCommand"]


class TestPlanValidatorCommand(SubCommand):
    """
    Test plan validator subcommand is used to validate whether the testplan
    files adheres to the YChaos Test plan schema.

    ```
    $ ychaos testplan validate -h
    usage: ychaos testplan validate [-h] paths [paths ...]

    positional arguments:
      paths       Space separated list of file/directory paths to validate

    optional arguments:
      -h, --help  show this help message and exit
    ```
    """

    name = "validate"
    help = "Validate YChaos Test plans"

    _exitcode = 0

    @classmethod
    def build_parser(cls, parser: ArgumentParser) -> ArgumentParser:
        parser.add_argument(
            "paths",
            type=Path,
            nargs="+",
            help="Space separated list of file/directory paths to validate",
        )

        return parser

    def __init__(self, **kwargs):
        assert kwargs.pop("cls") == self.__class__

        self.app = kwargs.pop("app")
        self.console: Console = self.app.console

        self.paths: List[Path] = kwargs.pop("paths")

    def resolve_validation_paths(self) -> List[Path]:
        file_types = ("json", "yaml", "yml")
        resolved_filepaths: List[Path] = list()
        for input_path in self.paths:
            if input_path.resolve().is_dir():
                for file_type in file_types:
                    resolved_filepaths.extend(
                        list(input_path.glob("**/*.{}".format(file_type)))
                    )
            else:
                resolved_filepaths.append(input_path)

        return resolved_filepaths

    def set_exitcode(self, exitcode=0):
        self._exitcode = exitcode

    def do_testplans_validation(self):
        exitcode = 0
        self.console.log("Getting Test plans")

        resolved_filepaths = self.resolve_validation_paths()

        if len(resolved_filepaths) == 0:
            self.console.line()
            self.console.print(
                ":open_file_folder: No Test plans found", style="orange3"
            )
            return

        self.console.log("Validating Test plans")
        self.console.line()

        with self.console.status("Validating...") as status:
            for file in sorted(resolved_filepaths):
                try:
                    TestPlanValidator.validate_file(file)
                    self.console.print(
                        ":white_check_mark: {file}".format(file=str(file)),
                        style="green",
                    )

                except ValidationError as validation_error:
                    self.set_exitcode(1)

                    self.console.print("")
                    self.console.print(
                        ":exclamation: {file}".format(file=str(file)), style="bold red"
                    )
                    self.console.print(
                        Panel.fit(
                            str(validation_error), title="Validation Error", style="red"
                        )
                    )
                    self.console.print("")

                except FileNotFoundError as file_not_found_error:
                    self.set_exitcode(1)
                    self.console.print(
                        ":mag: {file} [italic]not found[/italic]".format(
                            file=str(file)
                        ),
                        style="indian_red",
                    )

        return exitcode

    @classmethod
    def main(cls, args: Namespace) -> Any:
        validator = TestPlanValidatorCommand(**vars(args))
        validator.do_testplans_validation()

        return validator._exitcode