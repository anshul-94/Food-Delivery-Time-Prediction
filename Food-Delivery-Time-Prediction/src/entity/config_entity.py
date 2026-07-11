from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for Data Ingestion Component
    """

    root_dir: Path

    source_data_path: Path

    raw_data_path: Path

    train_data_path: Path

    test_data_path: Path

    train_ratio: float

    random_state: int
