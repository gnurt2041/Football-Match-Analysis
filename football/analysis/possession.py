from typing import List, Optional
import numpy as np
from util.detection import Detection

# resolves which player is currently in ball possession based on player-ball proximity

def get_player_in_possession(
    player_detections: List[Detection],
    ball_detections: List[Detection],
    proximity: int,
    min_distance: int = 500,
    min_proximity: int = 5
) -> Optional[Detection]:
    if len(ball_detections) != 1:
        return None,[]
    ball_detection = ball_detections[0]
    player_closest_to_ball = None
    for player_detection in player_detections:
        left_foot_distance = np.linalg.norm(ball_detection.rect.center.int_xy_array - player_detection.rect.bottom_left.int_xy_array)
        right_foot_distance = np.linalg.norm(ball_detection.rect.center.int_xy_array - player_detection.rect.bottom_right.int_xy_array)
        distance_to_ball = min(left_foot_distance, right_foot_distance)
        if distance_to_ball < min_distance :
           player_closest_to_ball = player_detection
           min_distance = distance_to_ball
    # if min_distance > distance_threshold :
    if player_closest_to_ball:
            # scale_x = 0.4
            # scale_y = 0.45
            # right_foot_error_box, left_foot_error_box = player_closest_to_ball.rect.pad_specific(scale_x = scale_x, scale_y = scale_y)
            if player_closest_to_ball.rect.pad(proximity).contains_point(point=ball_detection.rect.center):
                #     if get_iou(ball_detection.rect, right_foot_error_box) < 0.5 or get_iou(ball_detection.rect, left_foot_error_box) < 0.5: 
                # if not left_foot_error_box.contains_point(point=ball_detection.rect.center) and not right_foot_error_box.contains_point(point=ball_detection.rect.center):
                # if min_distance < proximity:
                return player_closest_to_ball, ball_detections
            else:
                return None, ball_detections
            # else:
            #     return None, ball_detections
    
    else:
      return None, ball_detections

# MCI dang co bong, bong bay qua 1 tk RMA, thi van tinh cho tim hien tai la team MCI 1 khung hinh co bong,
# thoi gian van tan + them 1, 
# khi nay dieu khien team hien tai se khac vs team cua tk RMA do RMA != MCI
# bat dau dem so khung hinh (counter = 0)
# cong them 1 vi tinh tu day la khung hinh dau tien RMA gan bong nhat
# neu so khung hinh dem cua team moi( khac team cu >=20) va thang hien tai co tk player thi doi team hien tai sang tk player
# bat dau dem thoi gian moi cua doi moi
# khi nao so khung hinh doi moi co bong >= 20 thi moi cho phep doi duoc thuc su kiem soat bong

# Khi bat dau tran dau, doi da truoc se la doi hien tai co bong
# van cong so khung hinh doi co bong, ke ca hon 20 thi doi co bong van la doi hien tai
# neu sau 20 khung hinh, co mot khung hinh doi doi phuong co bong thi se xu ly nhu tren
def get_team_in_possession(player_possession: Detection, args, team_possession: dict = {}) -> dict:
        if not team_possession :
            team_possession[args.teams_name[0]] = 0
            team_possession[args.teams_name[1]] = 0
            team_possession['duration'] = 0
            team_possession['current_team'] = args.teams_name[0]
            team_possession['true_current_team'] = args.teams_name[0]
            team_possession['counter'] = 0

        if player_possession is not None:
           #   if team_possession['current_team'] == team_possession['true_current_team']
           team_possession[team_possession['true_current_team']] += 1
           team_possession['duration'] += 1
           
           if team_possession['current_team'] != player_possession.classification :
                team_possession['counter'] = 0
                team_possession['current_team'] = player_possession.classification

           team_possession['counter'] += 1

           if team_possession['counter'] >= args.possession_threshold :
                team_possession['true_current_team'] = team_possession['current_team']

        return team_possession

def inertia_possession(player_possession: Detection, team_possession: dict) -> Optional[Detection]:
  if player_possession:
     if player_possession.classification == team_possession['true_current_team'] :
        return player_possession
     else:
        return None
  else:
    return None