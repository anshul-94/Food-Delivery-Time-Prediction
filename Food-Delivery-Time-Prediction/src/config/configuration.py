from pathlib import Path

from src.entity.config_entity import DataIngestionConfig
from src.utils.common import read_yaml, create_directories


class ConfigurationManager:
    """
    Reads project configuration and returns
    configuration objects for different components.
    """

    def __init__(
        self,
        config_filepath: Path = Path("config/config.yaml")
    ):

        self.config = read_yaml(config_filepath)

        create_directories(
            [Path(self.config["artifacts_root"])]
        )

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config["data_ingestion"]

        create_directories(
            [Path(config["root_dir"])]
        )

        return DataIngestionConfig(

            root_dir=Path(config["root_dir"]),

            source_data_path=Path(config["source_data_path"]),

            raw_data_path=Path(config["raw_data_path"]),

            train_data_path=Path(config["train_data_path"]),

            test_data_path=Path(config["test_data_path"]),

            test_size=config["test_size"],

            random_state=config["random_state"],
        )
