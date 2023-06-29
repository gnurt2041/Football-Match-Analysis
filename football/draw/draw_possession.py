import os
import PIL
import numpy as np

def add_alpha(img: PIL.Image.Image, alpha: int = 100) -> PIL.Image.Image:
        """
        Add an alpha channel to an image
        Parameters
        ----------
        img : PIL.Image.Image
            Image
        alpha : int, optional
            Alpha value, by default 100
        Returns
        -------
        PIL.Image.Image
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
    ) -> PIL.Image.Image:
        """
        Get possession counter background
        Returns
        -------
        PIL.Image.Image
            Counter background
        """
        
        counter = PIL.Image.open(board_img).convert("RGBA")
        counter = add_alpha(counter, 210)
        counter = np.array(counter)
        width, height = counter.shape[1], counter.shape[0]
        red, green, blue, alpha = counter.T
        counter = np.array([blue, green, red, alpha])
        counter = counter.transpose()
        counter = PIL.Image.fromarray(counter)
        counter = counter.resize((int(width * 0.6), int(height * 0.6)))
        return counter
        
def draw_possession_counter(
        team_possession,
        args,
        frame: np.array,
        counter_background: PIL.Image.Image,
        debug: bool = False
    ) -> np.ndarray:
        """
        Draw elements of the possession in frame
        Parameters
        ----------
        frame : PIL.Image.Image
            Frame
        counter_background : PIL.Image.Image
            Counter background
        debug : bool, optional
            Whether to draw extra debug information, by default False
        Returns
        -------
        PIL.Image.Image
            Frame with elements of the match
        """
        frame = PIL.Image.fromarray(frame).copy()
        # get width of PIL.Image
        frame_width = frame.size[0]
        counter_origin = (frame_width - 260, 20)
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
            origin=(counter_origin[0] + 5, counter_origin[1] + 90),
            text=args.teams_name[0],
            counter_text = home_text,
            color=args.board_colors[0],
            text_color=args.text_colors[0],
            height=35,
            width=100,
        )
        frame = draw_counter(
            frame,
            origin=(counter_origin[0] + 5 + 105, counter_origin[1] + 90),
            text=args.teams_name[1],
            counter_text = away_text,
            color=args.board_colors[1],
            text_color=args.text_colors[1],
            height=35,
            width=100,
        )

        return np.array(frame)
def get_time_possession(possession, fps: int) -> str:
        """
        Return team possession in time format
        Parameters
        ----------
        fps : int
            Frames per second
        Returns
        -------
        str
            Team possession in time format (mm:ss)
        """

        seconds = round(possession / fps)
        minutes = seconds // 60
        seconds = seconds % 60

        # express seconds in 2 digits
        seconds = str(seconds)
        if len(seconds) == 1:
            seconds = "0" + seconds

        # express minutes in 2 digits
        minutes = str(minutes)
        if len(minutes) == 1:
            minutes = "0" + minutes

        return f"{minutes}:{seconds}"
        
def draw_counter_background(
        frame: PIL.Image.Image,
        origin: tuple,
        counter_background: PIL.Image.Image,
    ) -> PIL.Image.Image:
        """
        Draw counter background
        Parameters
        ----------
        frame : PIL.Image.Image
            Frame
        origin : tuple
            Origin (x, y)
        counter_background : PIL.Image.Image
            Counter background
        Returns
        -------
        PIL.Image.Image
            Frame with counter background
        """
        frame.paste(counter_background, origin, counter_background)
        return frame

def draw_counter(
        frame: PIL.Image.Image,
        text: str,
        counter_text: str,
        origin: tuple,
        color: tuple,
        text_color: tuple,
        height: int = 27,
        width: int = 50,
    ) -> PIL.Image.Image:
        """
        Draw counter
        Parameters
        ----------
        frame : PIL.Image.Image
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
        PIL.Image.Image
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
def possession_bar(percentage_possession, args,
    frame: PIL.Image.Image, origin: tuple) -> PIL.Image.Image:
        """
        Draw possession bar
        Parameters
        ----------
        frame : PIL.Image.Image
            Frame
        origin : tuple
            Origin (x, y)
        Returns
        -------
        PIL.Image.Image
            Frame with possession bar
        """

        bar_x = origin[0]
        bar_y = origin[1]
        bar_height = 30
        bar_width = 200

        ratio = percentage_possession[0]

        # Protect against too small rectangles
        if ratio < 0.07:
            ratio = 0.07

        if ratio > 0.93:
            ratio = 0.93

        left_rectangle = (
            origin,
            [int(bar_x + ratio * bar_width), int(bar_y + bar_height)],
        )

        right_rectangle = (
            [int(bar_x + ratio * bar_width), bar_y],
            [int(bar_x + bar_width), int(bar_y + bar_height)],
        )

        left_color = args.board_colors[0]
        right_color = args.board_colors[1]

        frame = draw_counter_rectangle(
            frame=frame,
            ratio=ratio,
            left_rectangle=left_rectangle,
            left_color=left_color,
            right_rectangle=right_rectangle,
            right_color=right_color,
        )

        # Draw home text
        if ratio > 0.15:
            home_text = (
                f"{int(percentage_possession[0] * 100)}%"
            )

            frame = text_in_middle_rectangle(
                img=frame,
                origin=left_rectangle[0],
                width=left_rectangle[1][0] - left_rectangle[0][0],
                height=left_rectangle[1][1] - left_rectangle[0][1],
                text=home_text,
                color=args.text_colors[0],
            )

        # Draw away text
        if ratio < 0.85:
            away_text = (
                f"{int(percentage_possession[1] * 100)}%"
            )

            frame = text_in_middle_rectangle(
                img=frame,
                origin=right_rectangle[0],
                width=right_rectangle[1][0] - right_rectangle[0][0],
                height=right_rectangle[1][1] - right_rectangle[0][1],
                text=away_text,
                color=args.text_colors[1],
            )

        return frame

def draw_counter_rectangle(
        frame: PIL.Image.Image,
        ratio: float,
        left_rectangle: tuple,
        left_color: tuple,
        right_rectangle: tuple,
        right_color: tuple,
    ) -> PIL.Image.Image:
        """Draw counter rectangle for both teams
        Parameters
        ----------
        frame : PIL.Image.Image
            Video frame
        ratio : float
            counter proportion
        left_rectangle : tuple
            rectangle for the left team in counter
        left_color : tuple
            color for the left team in counter
        right_rectangle : tuple
            rectangle for the right team in counter
        right_color : tuple
            color for the right team in counter
        Returns
        -------
        PIL.Image.Image
            Drawed video frame
        """

        # Draw first one rectangle or another in orther to make the
        # rectangle bigger for better rounded corners

        if ratio < 0.15:
            left_rectangle[1][0] += 20

            frame = half_rounded_rectangle(
                frame,
                rectangle=left_rectangle,
                color=left_color,
                radius=15,
            )

            frame = half_rounded_rectangle(
                frame,
                rectangle=right_rectangle,
                color=right_color,
                left=True,
                radius=15,
            )
        else:
            right_rectangle[0][0] -= 20

            frame = half_rounded_rectangle(
                frame,
                rectangle=right_rectangle,
                color=right_color,
                left=True,
                radius=15,
            )

            frame = half_rounded_rectangle(
                frame,
                rectangle=left_rectangle,
                color=left_color,
                radius=15,
            )

        return frame
def half_rounded_rectangle(
        img: PIL.Image.Image,
        rectangle: tuple,
        color: tuple,
        radius: int = 15,
        left: bool = False,
    ) -> PIL.Image.Image:
        """
        Draw a half rounded rectangle on the image
        Parameters
        ----------
        img : PIL.Image.Image
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
        PIL.Image.Image
            Image with the half rounded rectangle drawn
        """
        overlay = img.copy()
        draw = PIL.ImageDraw.Draw(overlay, "RGBA")
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
        img: PIL.Image.Image,
        origin: tuple,
        width: int,
        height: int,
        text: str,
        font: PIL.ImageFont = None,
        color=(255, 255, 255),
    ) -> PIL.Image.Image:
        """
        Draw text in middle of rectangle
        Parameters
        ----------
        img : PIL.Image.Image
            Image
        origin : tuple
            Origin of the rectangle (x, y)
        width : int
            Width of the rectangle
        height : int
            Height of the rectangle
        text : str
            Text to draw
        font : PIL.ImageFont, optional
            Font to use, by default None
        color : tuple, optional
            Color of the text, by default (255, 255, 255)
        Returns
        -------
        PIL.Image.Image
            Image with the text drawn
        """

        draw = PIL.ImageDraw.Draw(img)
        root_dir =  os.getcwd().replace('\\','/')

        if font is None:
            font = PIL.ImageFont.truetype("/root_dir/draw/Gidole-Regular.ttf", size=18)
            # font = PIL.ImageFont.load_default(size=24)

        w, h = draw.textsize(text, font=font)
        text_origin = (
            origin[0] + width / 2 - w / 2,
            origin[1] + height / 2 - h / 2,
        )

        draw.text(text_origin, text, font=font, fill=color)

        return img
