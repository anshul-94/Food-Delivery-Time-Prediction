import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join(
        "artifacts",
        "preprocessor.pkl"
    )


class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Creates and returns the preprocessing object.
        """

        try:

            logging.info("Creating preprocessing object...")

            numerical_columns = [
                "Delivery_person_Age",
                "Delivery_person_Ratings",
                "multiple_deliveries"
            ]

            categorical_columns = [
                "Weatherconditions",
                "Road_traffic_density",
                "Type_of_order",
                "Type_of_vehicle",
                "Festival",
                "City"
            ]

            numeric_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore",
                            sparse_output=False
                        )
                    )
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "num_pipeline",
                        numeric_pipeline,
                        numerical_columns
                    ),
                    (
                        "cat_pipeline",
                        categorical_pipeline,
                        categorical_columns
                    )
                ]
            )

            logging.info("Preprocessing object created successfully.")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformation(
        self,
        train_path,
        test_path
    ):

        try:

            logging.info("Reading train and test datasets.")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessor = self.get_data_transformer_object()

            target_column = "Time_taken(min)"

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            logging.info("Applying preprocessing on training data.")

            X_train_processed = preprocessor.fit_transform(X_train)

            logging.info("Applying preprocessing on test data.")

            X_test_processed = preprocessor.transform(X_test)

            train_arr = np.c_[X_train_processed, np.array(y_train)]
            test_arr = np.c_[X_test_processed, np.array(y_test)]

            logging.info("Saving preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor
            )

            logging.info("Data Transformation Completed Successfully.")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
