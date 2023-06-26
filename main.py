
import cv2
import PIL
import matplotlib
import torch

from analysis.filter import filters
from analysis.hsv_classifier import HSVClassifier
from analysis.inertia_classifier import InertiaClassifier
from analysis.colors import Color
from draw.annotate import BaseAnnotator
from draw.marker import MarkerAnntator

from draw.draw_possession import get_possession_background, draw_possession_counter
from analysis.possession import get_player_in_possession, get_team_in_possession, inertia_possession

from util.video import Video
from util.detection import Detection, filter_class, filter_classification, true_ball
from util.track import BYTETrackerArgs, detections2boxes, tracks2boxes, match_detections_with_tracks

from util.options import args_parser

from yolox.tracker.byte_tracker import BYTETracker

args = args_parser()
print(args)
# color settings

# home color
HOME_COLOR_HEX = matplotlib.colors.cnames[args.colors_draw[0]]
HOME_COLOR = Color.from_hex_string(HOME_COLOR_HEX)

# away color
AWAY_COLOR_HEX = matplotlib.colors.cnames[args.colors_draw[1]]
AWAY_COLOR = Color.from_hex_string(AWAY_COLOR_HEX)

# possession board and text color
HOME_BOARD_HEX = matplotlib.colors.cnames['skyblue']
args.board_colors[0] = Color.from_hex_string(HOME_BOARD_HEX).bgr_tuple
HOME_TEXT_HEX = matplotlib.colors.cnames['white']
args.text_colors[0] = Color.from_hex_string(HOME_TEXT_HEX).bgr_tuple
AWAY_BOARD_HEX = matplotlib.colors.cnames['royalblue']
args.board_colors[1] = Color.from_hex_string(AWAY_BOARD_HEX).bgr_tuple
AWAY_TEXT_HEX = matplotlib.colors.cnames['white']
args.text_colors[1] = Color.from_hex_string(AWAY_TEXT_HEX).bgr_tuple

# annotation color
# refree color
REFEREE_COLOR_HEX = matplotlib.colors.cnames[args.colors_draw[2]]
REFEREE_COLOR = Color.from_hex_string(REFEREE_COLOR_HEX)

# marker color
MARKER_CONTOUR_COLOR_HEX = "000000"
MARKER_CONTOUR_COLOR = Color.from_hex_string(MARKER_CONTOUR_COLOR_HEX)

# player maker color
PLAYER_MARKER_FILL_COLOR_HEX = "FF0000"
PLAYER_MARKER_FILL_COLOR = Color.from_hex_string(PLAYER_MARKER_FILL_COLOR_HEX)

# ball maker color
BALL_MERKER_FILL_COLOR_HEX = "00FF00"
BALL_MARKER_FILL_COLOR = Color.from_hex_string(BALL_MERKER_FILL_COLOR_HEX)

# markar parameters
MARKER_CONTOUR_THICKNESS = 2
MARKER_WIDTH = 15
MARKER_HEIGHT = 15
MARKER_MARGIN = 7

# distance in pixels from the player's bounding box where we consider the ball is in his possession
PLAYER_IN_POSSESSION_PROXIMITY = 45

SOURCE_VIDEO_PATH = "./mun_sev_test.mp4"
BOARD_IMG = "./football/draw/possession_board.png"

# initiate video reader and writer
video = Video(input_path=SOURCE_VIDEO_PATH)
args.fps = video.video_capture.get(cv2.CAP_PROP_FPS)

# initiate annotators
THICKNESS = 4
player_home_annotator = BaseAnnotator(
    colors = HOME_COLOR,thickness=THICKNESS)
player_away_annotator = BaseAnnotator(
    colors = AWAY_COLOR,thickness=THICKNESS)
referee_annotator = BaseAnnotator(
    colors = REFEREE_COLOR,thickness=THICKNESS)

ball_marker_annotator = MarkerAnntator(
    color=BALL_MARKER_FILL_COLOR)
player_in_possession_marker_annotator = MarkerAnntator(
    color=PLAYER_MARKER_FILL_COLOR)
# Load the model
model = torch.hub.load('.', 'custom', args.model, source='local')
# HSV Classifier
filters = filters(args)
hsv_classifier = HSVClassifier(filters=filters)
# Add inertia to classifier
classifier = InertiaClassifier(classifier=hsv_classifier, inertia=20)
possession_background  = get_possession_background(board_img = BOARD_IMG)
# initiate tracker
byte_tracker = BYTETracker(BYTETrackerArgs())
team_possession = {}


# loop over frames
for index, frame in enumerate(video):

    annotated_image = frame.copy()
    # run detector
    results = model(frame[...,::-1], size=1280)
    detections = Detection.from_numpy(
        pred=results.pred[0].cpu().numpy(),
        names=model.names)

    ball_detections = filter_class(detections=detections, class_id=0)
    ball_detection = true_ball(detections=ball_detections, ball_confidence = args.ball_conf) 
    tracked_person_detections = filter_class(detections=detections, class_id=0, reverse=True)

    # track
    if len(tracked_person_detections) != 0:
        tracks = byte_tracker.update(
                output_results=detections2boxes(detections=tracked_person_detections),
                img_info=frame.shape,
                img_size=frame.shape
        )
        tracked_detections = match_detections_with_tracks(detections=tracked_person_detections, tracks=tracks)
        tracked_person_detections_pd = classifier.predict_from_detections(detections=tracked_detections.copy(), img=frame)

        tracked_referee_detections = filter_classification(detections = tracked_person_detections_pd, classification="Referee")
        tracked_player_home_detections = filter_classification(detections = tracked_person_detections_pd, classification = args.teams_name[0])
        tracked_player_away_detections = filter_classification(detections = tracked_person_detections_pd, classification = args.teams_name[1])

        player_detections = tracked_player_home_detections + tracked_player_away_detections

        # calculate player in possession
        player_in_possession_detection, ball_detection = get_player_in_possession(
                                        player_detections=player_detections,
                                        ball_detections=ball_detection,
                                        proximity=PLAYER_IN_POSSESSION_PROXIMITY)


        team_possession = get_team_in_possession(
                          team_possession = team_possession,
                          player_possession = player_in_possession_detection,
                          args=args)

        player_in_possession_detection = inertia_possession(player_possession = player_in_possession_detection, team_possession = team_possession)

        annotated_image = player_home_annotator.annotate(
          image=annotated_image,
          detections=tracked_player_home_detections)

        annotated_image = player_away_annotator.annotate(
          image=annotated_image,
          detections=tracked_player_away_detections)

        annotated_image = referee_annotator.annotate(
          image=annotated_image,
          detections=tracked_referee_detections)

        annotated_image = ball_marker_annotator.annotate(
          image=annotated_image,
          detections=ball_detection,
          width = MARKER_WIDTH,
          height = MARKER_HEIGHT,
          margin = MARKER_MARGIN,
          thickness = MARKER_CONTOUR_THICKNESS,
          color_contour=MARKER_CONTOUR_COLOR)

        annotated_image = player_in_possession_marker_annotator.annotate(
          image=annotated_image,
          detections=[player_in_possession_detection] if player_in_possession_detection else [],
          width = MARKER_WIDTH,
          height = MARKER_HEIGHT,
          margin = MARKER_MARGIN,
          thickness = MARKER_CONTOUR_THICKNESS,
          color_contour=MARKER_CONTOUR_COLOR)

        annotated_image = draw_possession_counter(
                          team_possession=team_possession,
                          frame=PIL.Image.fromarray(annotated_image).copy(),
                          counter_background=possession_background,
                          args=args)

    # save video frame
    video.write(annotated_image)
