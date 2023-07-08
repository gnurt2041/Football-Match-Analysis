import numpy as np
from PIL import Image, ImageDraw, ImageFont
def add_alpha(img: Image.Image, alpha: int = 100) -> Image.Image:
        """
        Add an alpha channel to an image
        Parameters
        ----------
        img : Image.Image
            Image
        alpha : int, optional
            Alpha value, by default 100
        Returns
        -------
         Image.Image
            Image with alpha channel
        """
        data = img.getdata()
        newData = []
        for old_pixel in data:

            # Don't change transparency of transparent pixels
            if old_pixel[3] != 0:
                pixel_with_alpha = old_pixel[:3] + (alpha,)
                newData.append(pixel_with_alpha)
            else:
                newData.append(old_pixel)

        img.putdata(newData)
        return img

def get_possession_background(board_img: str
    ) -> Image.Image:
        """
        Get possession counter background
        Returns
        -------
         Image.Image
            Counter background
        """
        
        counter =  Image.open(board_img).convert("RGBA")
        counter = add_alpha(counter, 210)
        counter = np.array(counter)
        width, height = counter.shape[1], counter.shape[0]
        red, green, blue, alpha = counter.T
        counter = np.array([blue, green, red, alpha])
        counter = counter.transpose()
        counter =  Image.fromarray(counter)
        counter = counter.resize((int(width * 0.6), int(height * 0.6)))
        return counter
        
def draw_possession_counter(
        team_possession,
        args,
        frame: np.array,
        counter_background: Image.Image,
        debug: bool = False
    ) -> np.ndarray:
        """
        Draw elements of the possession in frame
        Parameters
        ----------
        frame : Image.Image
            Frame
        counter_background : Image.Image
            Counter background
        debug : bool, optional
            Whether to draw extra debug information, by default False
        Returns
        -------
         Image.Image
            Frame with elements of the match
        """
        frame =  Image.fromarray(frame).copy()
        # get width of  Image
        frame_width = frame.size[0]
        counter_origin = (frame_width - 330, 20)
        if team_possession['duration'] == 0:
          possession_per_team = np.zeros(2)
        else:
          possession_per_team = np.array(list(team_possession.values())[:2],dtype=np.int32)/team_possession['duration']
        frame = draw_counter_background(
            frame,
            origin=counter_origin,
            counter_background=counter_background,
        )
        home_text = (
                f"{int(np.round(possession_per_team[0] * 100, 0))}%"
            )
        away_text = (
                f"{int(np.round(possession_per_team[1] * 100, 0))}%"
            )
        frame = draw_counter(
            frame,
            origin=(counter_origin[0] + 5, counter_origin[1] + 75),
            text=args.teams_name[0],
            counter_text = home_text,
            color=args.board_colors[0],
            text_color=args.text_colors[0],
            height=35,
            width=100,
        )
        frame = draw_counter(
            frame,
            origin=(counter_origin[0] + 5 + 110, counter_origin[1] + 75),
            text=args.teams_name[1],
            counter_text = away_text,
            color=args.board_colors[1],
            text_color=args.text_colors[1],
            height=35,
            width=100,
        )

        return np.array(frame)

def draw_counter_background(
        frame: Image.Image,
        origin: tuple,
        counter_background: Image.Image,
    ) -> Image.Image:
        """
        Draw counter background
        Parameters
        ----------
        frame : Image.Image
            Frame
        origin : tuple
            Origin (x, y)
        counter_background : Image.Image
            Counter background
        Returns
        -------
         Image.Image
            Frame with counter background
        """
        frame.paste(counter_background, origin, counter_background)
        return frame

def draw_counter(
        frame: Image.Image,
        text: str,
        counter_text: str,
        origin: tuple,
        color: tuple,
        text_color: tuple,
        height: int = 27,
        width: int = 50,
    ) -> Image.Image:
        """
        Draw counter
        Parameters
        ----------
        frame : Image.Image
            Frame
        text : str
            Text in left-side of counter
        counter_text : str
            Text in right-side of counter
        origin : tuple
            Origin (x, y)
        color : tuple
            Color
        text_color : tuple
            Color of text
        height : int, optional
            Height, by default 27
        width : int, optional
            Width, by default 120
        Returns
        -------
         Image.Image
            Frame with counter
        """

        team_begin = origin
        team_width_ratio = 0.417
        team_width = width * team_width_ratio

        team_rectangle = (
            team_begin,
            (team_begin[0] + team_width, team_begin[1] + height),
        )

        time_begin = (origin[0] + team_width, origin[1])
        time_width = width * (1 - team_width_ratio)

        time_rectangle = (
            time_begin,
            (time_begin[0] + time_width, time_begin[1] + height),
        )

        frame = half_rounded_rectangle(
            img=frame,
            rectangle=team_rectangle,
            color=color,
            radius=20,
        )

        frame = half_rounded_rectangle(
            img=frame,
            rectangle=time_rectangle,
            color=(239, 234, 229),
            radius=20,
            left=True,
        )

        frame = text_in_middle_rectangle(
            img=frame,
            origin=team_rectangle[0],
            height=height,
            width=team_width,
            text=text,
            color=text_color,
        )

        frame = text_in_middle_rectangle(
            img=frame,
            origin=time_rectangle[0],
            height=height,
            width=time_width,
            text=counter_text,
            color="black",
        )

        return frame

def half_rounded_rectangle(
        img: Image.Image,
        rectangle: tuple,
        color: tuple,
        radius: int = 15,
        left: bool = False,
    ) -> Image.Image:
        """
        Draw a half rounded rectangle on the image
        Parameters
        ----------
        img : Image.Image
            Image
        rectangle : tuple
            Rectangle to draw ( (xmin, ymin), (xmax, ymax) )
        color : tuple
            Color of the rectangle (BGR)
        radius : int, optional
            Radius of the rounded borders, by default 15
        left : bool, optional
            Whether the flat side is the left side, by default False
        Returns
        -------
         Image.Image
            Image with the half rounded rectangle drawn
        """
        overlay = img.copy()
        draw =  ImageDraw.Draw(overlay, "RGBA")
        draw.rounded_rectangle(rectangle, radius, fill=color)

        height = rectangle[1][1] - rectangle[0][1]
        stop_width = 13

        if left:
            draw.rectangle(
                (
                    rectangle[0][0] + 0,
                    rectangle[1][1] - height,
                    rectangle[0][0] + stop_width,
                    rectangle[1][1],
                ),
                fill=color,
            )
        else:
            draw.rectangle(
                (
                    rectangle[1][0] - stop_width,
                    rectangle[1][1] - height,
                    rectangle[1][0],
                    rectangle[1][1],
                ),
                fill=color,
            )
        return overlay
        
def text_in_middle_rectangle(
        img: Image.Image,
        origin: tuple,
        width: int,
        height: int,
        text: str,
        font: ImageFont = None,
        color=(255, 255, 255),
    ) -> Image.Image:
        """
        Draw text in middle of rectangle
        Parameters
        ----------
        img : Image.Image
            Image
        origin : tuple
            Origin of the rectangle (x, y)
        width : int
            Width of the rectangle
        height : int
            Height of the rectangle
        text : str
            Text to draw
        font :  ImageFont, optional
            Font to use, by default None
        color : tuple, optional
            Color of the text, by default (255, 255, 255)
        Returns
        -------
         Image.Image
            Image with the text drawn
        """

        draw = ImageDraw.Draw(img)
        if font is None:
            font = ImageFont.truetype("/content/drive/MyDrive/Football-Match-Analysis/football/draw/Gidole-Regular.ttf", size=18)
            # font =  ImageFont.load_default(size=24)

        w, h = draw.textsize(text, font=font)
        text_origin = (
            origin[0] + width / 2 - w / 2,
            origin[1] + height / 2 - h / 2,
        )

        draw.text(text_origin, text, font=font, fill=color)

        return img
        
                
