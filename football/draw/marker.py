from typing import List
from dataclasses import dataclass
import numpy as np
from analysis.colors import Color
from draw.point import Point
from draw.annotate import draw_filled_polygon, draw_polygon
from util.detection import Detection
# calculates coordinates of possession marker
def calculate_marker(anchor: Point, width: int, height: int, margin: int) -> np.ndarray:
    x, y = anchor.int_xy_tuple
    return(np.array([
        [x - width // 2, y - height - margin],
        [x, y - margin],
        [x + width // 2, y - height - margin]
    ]))


# draw single possession marker
def draw_marker(image: np.ndarray, color: Color, color_contour: Color, thickness: int, countour: np.ndarray) -> np.ndarray:
    image = draw_filled_polygon(
        image=image,
        countour=countour,
        color=color)
    image = draw_polygon(
        image=image,
        countour=countour,
        color=color_contour,
        thickness=thickness)
    return image


# dedicated annotator to draw possession markers on video frames
@dataclass
class MarkerAnntator:

    color: Color

    def annotate(self, image: np.ndarray, detections: List[Detection], width: int, height: int, margin: int, thickness: int, color_contour: Color) -> np.ndarray:
        annotated_image = image.copy()
        for detection in detections:
            possession_marker_countour = calculate_marker(anchor=detection.rect.top_center, width = width, height = height, margin = margin)   
            annotated_image = draw_marker(
                image=image,
                countour = possession_marker_countour,
                color=self.color,
                color_contour = color_contour,
                thickness = thickness)
        return annotated_image