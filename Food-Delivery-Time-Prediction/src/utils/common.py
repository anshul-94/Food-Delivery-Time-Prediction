from pathlib import Path
from typing import Iterable
import yaml
import os
import sys

from src.exception import CustomException


def read_yaml(path_to_yaml: Path) -> dict:
    """
    Read a YAML file and return its contents.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise CustomException(e, sys)


def create_directories(paths: Iterable[Path]) -> None:
    """
    Create one or more directories if they don't exist.
    """
    try:
        for path in paths:
            os.makedirs(path, exist_ok=True)

    except Exception as e:
        raise CustomException(e, sys)
