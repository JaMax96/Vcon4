import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv
from collections import deque
from utils import MenuItem
from collections import Counter

model_path = "models/gesture_recognizer.task"


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def draw_menu(frame):
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

# Create a gesture recognizer instance with the live stream mode:


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))


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


def check_for_selection(list):
    most_common = Counter(list).most_common(1)
    if most_common[0][1]>20:
        return most_common[0][0]
    return MenuItem.Default  



options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

list_of_detected_menu_items = deque(maxlen=30)

with GestureRecognizer.create_from_options(options) as recognizer:
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
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = recognizer.recognize(mp_image)
        if result.gestures:
            gesture = result.gestures[0][0].category_name
            landmark = result.hand_landmarks[0][8]

            gesture = gesture + \
                (f"X:{round(landmark.x,2)}, Y: {round(landmark.y,2)}, Z: {round(landmark.z,2)}")
            list_of_detected_menu_items.appendleft(get_menu_item(landmark.y))

        else:
            gesture = "None Detected"
            list_of_detected_menu_items.appendleft(MenuItem.Default)

        # drawing menu
        frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        draw_menu(frame)

        cv.putText(frame, gesture, (0, len(
            frame[0])-175), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_4)
        # Display the resulting frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
        menu_item = check_for_selection(list_of_detected_menu_items)

    print(menu_item)
    cap.release()
    cv.destroyAllWindows()
