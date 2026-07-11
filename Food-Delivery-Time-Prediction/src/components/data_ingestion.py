import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:
    """
    Handles data ingestion process:
    - Read raw dataset
    - Save raw dataset
    - Train-test split
    - Save train/test datasets
    """

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):

        logger.info("Data Ingestion Started")

        try:

            # Read Dataset
            df = pd.read_csv(self.config.source_data_path)

            logger.info("Dataset Loaded Successfully")

            # Save Raw Dataset
            df.to_csv(
                self.config.raw_data_path,
                index=False
            )

            logger.info("Raw Dataset Saved")

            # Train Test Split
            train_df, test_df = train_test_split(

                df,

                test_size=self.config.test_size,

                random_state=self.config.random_state,
            )

            # Save Train Dataset
            train_df.to_csv(
                self.config.train_data_path,
                index=False
            )

            # Save Test Dataset
            test_df.to_csv(
                self.config.test_data_path,
                index=False
            )

            logger.info("Train/Test Split Completed")

            return (

                self.config.train_data_path,

                self.config.test_data_path

            )

        except Exception as e:

            logger.error(e)

            raise CustomException(e, sys)
