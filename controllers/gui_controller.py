from controllers.abstractController import AbstractController
from utils import MenuItem
import re
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv
from collections import deque, Counter
import time


def get_menu_item(y):
    if 0.11 < y < 0.22:
        return MenuItem.OnePlayer
    if 0.33 < y < 0.44:
        return MenuItem.TwoPlayer
    if 0.55 < y < 0.66:
        return MenuItem.Highscore
    if 0.77 < y < 0.88:
        return MenuItem.Exit
    return MenuItem.Default


def get_column(x):
    if 0 < x < 1/7:
        return 0
    if 1/7 < x < 2/7:
        return 1
    if 2/7 < x < 3/7:
        return 2
    if 3/7 < x < 4/7:
        return 3
    if 4/7 < x < 5/7:
        return 4
    if 5/7 < x < 6/7:
        return 5
    return 6


def check_for_selection(list):
    most_common = Counter(list).most_common(1)
    if most_common[0][1] > 20:

        return most_common[0][0]
    return MenuItem.Default


def check_for_column(list):
    most_common = Counter(list).most_common(1)
    if most_common[0][1] > 20:

        return most_common[0][0]
    return -1


def draw_menu(frame, frame_width, frame_height):
    # MenuItem 1 Player Game
    lp = (int(0.5*frame_width), int(2/9*frame_height))
    rp = (int(0.9*frame_width), int(1/9*frame_height))
    cv.rectangle(frame, lp, rp, (0, 255, 255), 3)
    lp = (lp[0]+5, lp[1]-17)
    cv.putText(frame, "1 Player Game", lp,
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_4)

    # MenuItem 2 Player Game
    lp = (int(0.5*frame_width), int(4/9*frame_height))
    rp = (int(0.9*frame_width), int(3/9*frame_height))
    cv.rectangle(frame, lp, rp, (0, 255, 255), 3)
    lp = (lp[0]+5, lp[1]-17)
    cv.putText(frame, "2 Player Game", lp,
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_4)

    # MenuItem Highscore Player Game
    lp = (int(0.5*frame_width), int(6/9*frame_height))
    rp = (int(0.9*frame_width), int(5/9*frame_height))
    cv.rectangle(frame, lp, rp, (0, 255, 255), 3)
    lp = (lp[0]+5, lp[1]-17)
    cv.putText(frame, "Highscore", lp, cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 0, 0), 2, cv.LINE_4)

    # MenuItem Exit Player Game
    lp = (int(0.5*frame_width), int(8/9*frame_height))
    rp = (int(0.9*frame_width), int(7/9*frame_height))
    cv.rectangle(frame, lp, rp, (0, 255, 255), 3)
    lp = (lp[0]+5, lp[1]-17)
    cv.putText(frame, "Exit", lp, cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 0, 0), 2, cv.LINE_4)


def draw_line(frame, startpoint, endpoint):
    cv.line(frame, startpoint, endpoint, (255, 0, 0), 2)
   # cv.line(frame,(0,0),(511,511),(255,0,0),5)


def draw_circle(frame, center, radius, color):
    cv.circle(frame, center, radius, color, -1)


def draw_gamefield(frame, frame_width, frame_height, gamefield):
    # draw vertical lines
    fraction = 1/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))
    fraction = 2/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))
    fraction = 3/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))
    fraction = 4/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))
    fraction = 5/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))
    fraction = 6/7
    draw_line(frame, (int(fraction*frame_width), 0),
              (int(fraction*frame_width), int(frame_height)))

    # draw horizontal lines
    fraction = 1/6
    draw_line(frame, (0, (int(fraction*frame_height))),
              (int(frame_width), int(fraction*frame_height)))
    fraction = 2/6
    draw_line(frame, (0, (int(fraction*frame_height))),
              (int(frame_width), int(fraction*frame_height)))
    fraction = 3/6
    draw_line(frame, (0, (int(fraction*frame_height))),
              (int(frame_width), int(fraction*frame_height)))
    fraction = 4/6
    draw_line(frame, (0, (int(fraction*frame_height))),
              (int(frame_width), int(fraction*frame_height)))
    fraction = 5/6
    draw_line(frame, (0, (int(fraction*frame_height))),
              (int(frame_width), int(fraction*frame_height)))

    # draw tokens
    i_mult = 6

    for i in range(gamefield.height):
        for j in range(gamefield.width):
            player = gamefield.board[i][j]

            if player != 0:
                # x is height
                # y is width
                x = i_mult * 1/6 * frame_height - 1/6 * frame_height / 2

                y = j * 1/7 * frame_width + 1/7 * frame_width / 2

                color = (0, 255, 255)
                if player == 1:
                    color = (0, 0, 255)
                draw_circle(frame, (int(y), int(x)), 30, color)

        i_mult -= 1


class GuiController(AbstractController):

    def __init__(self):
        super().__init__()
        model_path = "models/gesture_recognizer.task"
        BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.list_of_detected_menu_items = deque(maxlen=50)
        self.list_of_detected_columns = deque(maxlen=50)

        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE)

    def getMenuItem(self):
        self.list_of_detected_menu_items.clear()

        with self.GestureRecognizer.create_from_options(self.options) as recognizer:
            cap = cv.VideoCapture(0)

            menu_item = MenuItem.Default
            while menu_item == MenuItem.Default:
                # Capture frame-by-frame
                ret, frame = cap.read()

                # if frame is read correctly ret is Trueq
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Our operations on the frame come here
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB, data=frame)
                result = recognizer.recognize(mp_image)
                if result.gestures:
                    gesture = result.gestures[0][0].category_name

                    landmark = result.hand_landmarks[0][8]

                    gesture = gesture + \
                        (f"X:{round(landmark.x,2)}, Y: {round(landmark.y,2)}, Z: {round(landmark.z,2)}")
                    self.list_of_detected_menu_items.appendleft(
                        get_menu_item(landmark.y))

                else:
                    gesture = "None Detected"
                    self.list_of_detected_menu_items.appendleft(
                        MenuItem.Default)

                # drawing menu
                frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
                frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

                draw_menu(frame, frame_width, frame_height)

                cv.putText(frame, gesture, (0, len(
                    frame[0])-175), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_4)
                # Display the resulting frame
                cv.imshow('frame', frame)
                if cv.waitKey(1) == ord('q'):
                    break
                menu_item = check_for_selection(
                    self.list_of_detected_menu_items)

                if menu_item != MenuItem.Default:
                    break

            cap.release()
            cv.destroyAllWindows()
            return menu_item.name

    def getMove(self, game):
        self.list_of_detected_columns.clear()

        with self.GestureRecognizer.create_from_options(self.options) as recognizer:
            cap = cv.VideoCapture(0)

            column = -1
            while column == -1:
                # Capture frame-by-frame
                ret, frame = cap.read()

                # if frame is read correctly ret is Trueq
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Our operations on the frame come here
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB, data=frame)
                result = recognizer.recognize(mp_image)
                if result.gestures:
                    gesture = result.gestures[0][0].category_name

                    landmark = result.hand_landmarks[0][8]

                    gesture = gesture + \
                        (f"X:{round(landmark.x,2)}, Y: {round(landmark.y,2)}, Z: {round(landmark.z,2)}")
                    self.list_of_detected_columns.appendleft(
                        get_column(landmark.x))

                else:
                    gesture = "None Detected"
                    self.list_of_detected_columns.appendleft(-1)

                # drawing gamiefield
                frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
                frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

                draw_gamefield(frame, frame_width, frame_height, game)

                cv.putText(frame, gesture, (0, len(
                    frame[0])-175), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_4)
                # Display the resulting frame
                cv.imshow('frame', frame)
                if cv.waitKey(1) == ord('q'):
                    break
                column = check_for_column(self.list_of_detected_columns)

                if column != -1:
                    break
            time.sleep(1)
            cap.release()
            cv.destroyAllWindows()          
            return column

    def getWinningWindow(self, winner):
        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()

            frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
            frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

            #cv.putText(frame, f"Player {winner} has Won", (frame_width/2, frame_height/2),
            #          cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_4)
            cv.putText(frame, "WOLOLO", (0, len(
                        frame[0])-175), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_4)
            
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                    break            
            
        cap.release()
        cv.destroyAllWindows()
