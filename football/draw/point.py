# geometry utilities
from dataclasses import dataclass
from typing import Tuple

import numpy as np

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    @property
    def int_xy_tuple(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    @property
    def int_xy_array(self) -> np.ndarray:
        return np.asarray(self.int_xy_tuple)

@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def min_x(self) -> float:
        return self.x

    @property
    def min_y(self) -> float:
        return self.y

    @property
    def max_x(self) -> float:
        return self.x + self.width

    @property
    def max_y(self) -> float:
        return self.y + self.height

    @property
    def top_left(self) -> Point:
        return Point(x=self.x, y=self.y)
  
    @property
    def bottom_right(self) -> Point:
        return Point(x=self.x + self.width, y=self.y + self.height)
    
    @property
    def bottom_left(self) -> Point:
        return Point(x=self.x, y= self.y + self.height)
        
    @property
    def bottom_center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y + self.height)

    @property
    def top_center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y)

    @property
    def center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y + self.height / 2)

    def pad(self, padding: float):
        return Rect(
            x=self.x - padding,
            y=self.y - padding,
            width=self.width + 2*padding,
            height=self.height + 2*padding
        )
    def pad_specific(self, scale_x: float, scale_y: float):
        return Rect(
            width=self.width*scale_x,
            height=self.height*scale_y,
            x=self.x,
            y=self.y + self.height*(1 - scale_y)
        ),Rect(
            width=self.width*scale_x,
            height=self.height*scale_y,
            x=self.x + (self.width*scale_x)*(1-scale_x),
            y=self.y + self.height*(1 - scale_y)
        )

    def contains_point(self, point: Point) -> bool:
        return self.min_x < point.x < self.max_x and self.min_y < point.y < self.max_y
