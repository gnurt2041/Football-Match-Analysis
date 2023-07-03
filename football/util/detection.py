# detection utilities

from dataclasses import dataclass
from typing import Optional, List, Dict

import numpy as np
from draw.point import Rect
@dataclass
class Detection:
    rect: Rect
    class_id: int
    class_name: str
    confidence: float
    tracker_id: Optional[int] = None
    classification: Optional[str] = None

    @classmethod
    def from_numpy(cls, pred: np.ndarray, names: Dict[int, str]) :
        result = []
        for x_min, y_min, x_max, y_max, confidence, class_id in pred:
            class_id=int(class_id)
            result.append(Detection(
                rect=Rect(
                    x=float(x_min),
                    y=float(y_min),
                    width=float(x_max - x_min),
                    height=float(y_max - y_min)
                ),
                class_id=class_id,
                class_name=names[class_id],
                confidence=float(confidence)
            ))
        return result

def filter_class(detections: List[Detection], class_id: int, reverse: bool = False) -> List[Detection]:
    if not reverse:
        return [
              detection for detection in detections if detection.class_id == class_id
        ]
    else:
        return [
            detection for detection in detections if detection.class_id != class_id
        ]

def filter_classification(detections: List[Detection], classification: str, reverse: bool = False) -> List[Detection]:
    if not reverse:
        return [
              detection for detection in detections if detection.classification == classification
        ]
    else:
        # pre_detections =  [detection for detection in detections if detection.classification != classification]
        mean_area_detections = np.mean(np.array([detection.rect.area for detection in detections if detection.classification != classification]))
        return [detection for detection in detections if detection.rect.area > mean_area_detections*0.2 and detection.classification != classification]

def true_ball(detections: List[Detection], ball_confidence: float):

    if len(detections) != 0:
        max_conf = 0.0
        for detection in detections:
          if detection.confidence > max_conf:
             result = detection
             max_conf = detection.confidence
        if result.confidence > ball_confidence:
            return result
        else:
            return None
    else:
        return None
