import cv2
import requests
import mediapipe as mp


previous_state = "open"
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
VisionRunningMode = mp.tasks.vision.RunningMode
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions


def process_live_stream(result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global previous_state

    if result.face_landmarks:
        eye_threshold = 0.02
        eye_blink = result.face_landmarks[0][22].y - result.face_landmarks[0][157].y

        current_state = "closed" if eye_blink < eye_threshold else "open"

        if current_state == "closed" and previous_state == "open":
            requests.get('http://localhost:8000/api/increment-eye-count')

        previous_state = current_state


class EyeTracker:
    def __init__(self, model_asset_path):
        self.model_asset_path = model_asset_path

        self.options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_asset_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=(process_live_stream)
        )

    def capture_live_stream(self):
        cap = cv2.VideoCapture(0)

        with FaceLandmarker.create_from_options(self.options) as landmarker:
            calc_ts = [0.0]

            while (cap.isOpened()):
                ret, frame = cap.read()
                fps = cap.get(cv2.CAP_PROP_FPS)

                if ret == True:
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                    calc_ts.append(int(calc_ts[-1] + 1000/fps))
                    landmarker.detect_async(mp_image, calc_ts[-1])
                else:
                    break

        cap.release()


if __name__ == "__main__":
    eye_tracker = EyeTracker("src/assets/face_landmarker.task")
    eye_tracker.capture_live_stream()
