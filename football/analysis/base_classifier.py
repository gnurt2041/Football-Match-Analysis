from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd

from analysis.box import Box
from util.detection import Detection
class BaseClassifier(ABC):
    @abstractmethod
    def predict(self, input_image: List[np.ndarray]) -> List[str]:
        """
        Predicts the class of the objects in the image

        Parameters
        ----------

        input_image: List[np.ndarray]
            List of input images

        Returns
        -------
        result: List[str]
            List of class names
        """
        pass

    def predict_from_df(self, df: pd.DataFrame, img: np.ndarray) -> pd.DataFrame:
        """
        Predicts the class of the objects in the image and adds a column
        in the dataframe for classification

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the bounding boxes
        img : np.ndarray
            Image

        Returns
        -------
        pd.DataFrame
            DataFrame containing the bounding boxes and the class of the objects

        Raises
        ------
        TypeError
            If df is not a pandas DataFrame
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        box_images = []

        for index, row in df.iterrows():

            xmin = round(row["xmin"])
            ymin = round(row["ymin"])
            xmax = round(row["xmax"])
            ymax = round(row["ymax"])

            box = Box((xmin, ymin), (xmax, ymax), img)

            box_images.append(box.img)

        class_name = self.predict(box_images)

        df["classification"] = class_name

        return df

    def predict_from_detections(
        self, detections: List[Detection], img: np.ndarray
    ) -> List[Detection]:
        """
        Predicts the class of the objects in the image and adds the class in
        detection.data["classification"]

        Parameters
        ----------
        detections : List[norfair.Detection]
            List of detections
        img : np.ndarray
            Image

        Returns
        -------
        List[norfair.Detection]
            List of detections with the class of the objects
        """

        box_images = []

        for detection in detections:
            box = Box(detection.rect.top_left.int_xy_tuple, detection.rect.bottom_right.int_xy_tuple, img)
            box_images.append(box.img)

        class_name = self.predict(box_images)

        for detection, name in zip(detections, class_name):
            detection.classification = name

        return detections