from pathlib import Path
from typing import Any, Union

import yaml

from vzmi.ychaos.testplan.schema import TestPlan


class TestPlanValidator:
    """
    The Test plan validator class. Provides utility methods
    to validate the test plan files or raw data.
    """

    @classmethod
    def validate_file(cls, path: Union[str, Path]) -> None:
        """
        Validate a file (JSON/YAML) if the file content adheres to
        the testplan schema or not. This method on successful validation
        should not throw any errors.

        Raises:
            pydantic.ValidationError: If the content of the file does not follow the test plan schema
            FileNotFoundError: If the path passed to the method does not exist

        Args:
            path: A pathlike object

        Returns:
            None.
        """
        path = Path(path)
        with open(path, "r") as file:
            data = yaml.safe_load(file)

        cls.validate_data(data)

    @classmethod
    def validate_data(cls, data: Any) -> None:
        """
        Validate raw data (e.g. dictionary) whether it follows the Test plan schema.
        This method on successful validation should not throw any errors.

        Raises:
            pydantic.ValidationError: If the data does not follow the test plan schema

        Args:
            data: A data object (dictionary)

        Returns:
            None
        """
        TestPlan.validate(data)
