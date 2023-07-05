from typing import List
import numpy as np
from analysis.base_classifier import BaseClassifier
from util.detection import Detection

class InertiaClassifier:

    def __init__(
        self,
        classifier: BaseClassifier,
        inertia: int = 20,
        mode: int = 1,
    ):
        """

        Improves classification by using tracker IDs.
        It uses past classifications of the object to filter out noise.

        Parameters
        ----------
        classifier : BaseClassifier
            Classifier to use.
        inertia : int, optional
            Number of previous classifications to use, by default 20
        mode : int, optional
            Mode to use, by default WINDOW
        """
        self.inertia = inertia
        self.classifier = classifier
        self.classifications_per_id = {}
        self.mode = mode

    def add_first_classification_to_id(self, detection: Detection):
        """
        Add the first classification to the id.

        Parameters
        ----------
        detection : Detection
            Detection to add the classification to.
        """
        self.classifications_per_id[detection.tracker_id] = [
            detection.classification
        ]

    def add_new_clasification_to_id(self, detection: Detection):
        """
        Add a new classification to the existing id.

        Parameters
        ----------
        detection : Detection
            Detection to add the classification to.
        """
        self.classifications_per_id[detection.tracker_id].append(
            detection.classification
        )

    def add_classification_to_frame(self, detection: Detection):
        """
        Add a new classification using window mode.

        Parameters
        ----------
        detection : Detection
            Detection to add the classification to.
        """

        if detection.tracker_id not in self.classifications_per_id:
            self.add_first_classification_to_id(detection)

        elif len(self.classifications_per_id[detection.tracker_id]) < self.inertia:
            self.add_new_clasification_to_id(detection)

        elif len(self.classifications_per_id[detection.tracker_id]) == self.inertia:
            self.classifications_per_id[detection.tracker_id].pop(0)
            self.add_new_clasification_to_id(detection)

    def add_new_clasifications(self, detections: List[Detection]):
        """
        Load internal dictionary with new classifications.

        Parameters
        ----------
        detections : List[Detection]
            Detections to add the classification to.
        """

        for detection in detections:
            self.add_classification_to_frame(detection)

    def set_detections_classification(
        self, detections: List[Detection]
    ) -> List[Detection]:
        """
        Set the detections classification to the mode of the previous classifications.

        Parameters
        ----------
        detections : List[Detection]
            Detections to set the classification to.

        Returns
        -------
        List[Detection]
            Detections with the classification set.
        """

        for detection in detections:
            previous_classifications = self.classifications_per_id[detection.tracker_id]
            detection.classification = max(
                set(previous_classifications), key=previous_classifications.count
            )
        return detections

    def predict_from_detections(
        self, detections: List[Detection], img: np.ndarray
    ) -> List[Detection]:
        """
        Predict the classification of the detections.

        Parameters
        ----------
        detections : List[Detection]
            Detections to predict the classification of.
        img : np.ndarray
            Image to predict the classification of.

        Returns
        -------
        List[Detection]
            Detections with the classification set.
        """

        # Filter detections for clasificiations
        detections_classified = self.classifier.predict_from_detections(
            detections=detections,
            img=img,
        )

        # Add detections to internal dictionary
        self.add_new_clasifications(detections_classified)

        # Set detections classification
        detections = self.set_detections_classification(detections)

        return detections
