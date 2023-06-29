import argparse

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="./test.mp4",
        type=str,
        help="Path to the input "
    )
    parser.add_argument(
        "--model", default="/model.pt", type=str, help="Path to the model"
    )
    parser.add_argument(
        "--fps", default=30, type=int, help="FPS of the video"
    )
    parser.add_argument(
        "--possession",
        action="store_true",
        help="Enable possession counter"
    )
    parser.add_argument(
            "--possession_threshold",
            type=int,
            default=20,
            help="Amount of consecutive frames new team has to have the ball in order to change possession"
    )
    parser.add_argument(
            "--ball_conf",
            type=float,
            default=0.3,
            help="Ball confidence threshold"
    )
    parser.add_argument(
        "--teams_name",
        nargs='+',
        type=str,
        default=['MUN','SEV'],
        help="Name of two teams"
    )
    parser.add_argument(
        "--colors",
        nargs='+',
        type=str,
        default=[],
        help="Colors of two teams and refee, format: [c1,c2,c3,c4,c5] -> [T1,T1,T2,T2,R]"
    )
    parser.add_argument(
        "--color_t1",
        nargs='+',
        type=str,
        default=['red','blue','sky_blue','blueish_red'], #['sky_blue','orange'], # ['sky_blue','blueish_red','red']
        help="Colors of two teams and refee, format: [c1,c2] -> [T1,T1]"
    )
    parser.add_argument(
        "--color_t2",
        nargs='+',
        type=str,
        default=['white','yellow'],   #['black','red'], # ['blue','orange']
        help="Colors of two teams and refee, format: [c3,c4] -> [T2,T2]"
    )
    parser.add_argument(
        "--color_rf",
        type=str,
        default='black', # 'yellow'
        help="Colors of two teams and refee, format: [c5] -> [R]"
    )
    parser.add_argument(
        "--colors_draw",
        nargs='+',
        type=str,
        default=['blue','salmon','yellow'],
        help="Colors to draw classification of teams and refee, format: [c1,c2,c3] -> [T1,T2,R]"
    )
    parser.add_argument(
        "--board_colors",
        nargs='+',
        type=tuple,
        default=['',''],
        help="Colors to draw classification of teams and refee, format: [c1,c2,c3] -> [T1,T2,R]"
    )
    parser.add_argument(
        "--text_colors",
        nargs='+',
        type=tuple,
        default=['',''],
        help="Colors to draw classification of teams and refee, format: [c1,c2,c3] -> [T1,T2,R]"
    )
    # args = parser.parse_args(args=[])
    return parser.parse_args()