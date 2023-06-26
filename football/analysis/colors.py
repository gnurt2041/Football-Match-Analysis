from dataclasses import dataclass
from typing import Tuple

white = {
    "name": "white",
    "lower_hsv": (0, 0, 184),
    "upper_hsv": (179, 39, 255),
}

red = {
    "name": "red",
    "lower_hsv": (0, 100, 0),
    "upper_hsv": (8, 255, 255),
}

blueish_red = {
    "name": "blueish_red",
    "lower_hsv": (170, 0, 0),
    "upper_hsv": (178, 255, 255),
}

orange = {
    "name": "orange",
    "lower_hsv": (7, 110, 0),
    "upper_hsv": (15, 255, 255),
}

yellow = {
    "name": "yellow",
    "lower_hsv": (23, 51, 174),
    "upper_hsv": (33, 255, 255),
}

green = {
    "name": "green",
    "lower_hsv": (48, 50, 0),
    "upper_hsv": (55, 255, 255),
}

sky_blue = {
    "name": "sky_blue",
    "lower_hsv": (95, 38, 107),
    "upper_hsv": (118, 135, 255),
}

blue = {
    "name": "blue",
    "lower_hsv": (112, 105, 0),
    "upper_hsv": (126, 255, 255),
}

black = {
    "name": "black",
    "lower_hsv": (0, 0, 0),
    "upper_hsv": (179, 255, 49),
}

gray = {
    "name": "gray",
    "lower_hsv": (0, 0, 0),
    "upper_hsv": (179, 10, 255),
}
all = [white, red, orange, yellow, green, sky_blue, blue, blueish_red, black, gray]
@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

    @property
    def bgr_tuple(self) -> Tuple[int, int, int]:
        return self.b, self.g, self.r

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b
        
    @classmethod
    def from_hex_string(cls, hex_string: str):
        r, g, b = tuple(int(hex_string[1 + i:1 + i + 2], 16) for i in (0, 2, 4))
        return Color(r=r, g=g, b=b)


