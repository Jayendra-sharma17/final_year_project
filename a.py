import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk

class HandEyeTrackingApp:
    def __init__(self, master):
        self.master = master
        master.title("Hand and Eye Tracking")

        self.eye_tracking_button = tk.Button(master, text="Start Eye Tracking", command=self.start_eye_tracking)
        self.eye_tracking_button.pack()

        self.hand_tracking_button = tk.Button(master, text="Start Hand Tracking", command=self.start_hand_tracking)
        self.hand_tracking_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

        self.tracking_mode = None

    def start_eye_tracking(self):
        if self.tracking_mode != 'eye':
            self.tracking_mode = 'eye'
            self.eye_tracking_button.config(text="Stop Eye Tracking")
            self.hand_tracking_button.config(state="disabled")

            cam = cv2.VideoCapture(0)
            face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
            screen_w, screen_h = pyautogui.size()
            while True:
                _, frame = cam.read()
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                output = face_mesh.process(rgb_frame)
                landmark_points = output.multi_face_landmarks
                frame_h, frame_w, _ = frame.shape
                if landmark_points:
                    landmarks = landmark_points[0].landmark
                    for id, landmark in enumerate(landmarks[474:478]):
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 0))
                        if id == 1:
                            screen_x = screen_w * landmark.x
                            screen_y = screen_h * landmark.y
                            pyautogui.moveTo(screen_x, screen_y)
                    left = [landmarks[145], landmarks[159]]
                    for landmark in left:
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 255))
                    if (left[0].y - left[1].y) < 0.004:
                        pyautogui.click()
                        pyautogui.sleep(1)
                cv2.imshow('Eye Controlled Mouse', frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

            cam.release()
            cv2.destroyAllWindows()

            self.tracking_mode = None
            self.eye_tracking_button.config(text="Start Eye Tracking")
            self.hand_tracking_button.config(state="normal")

    def start_hand_tracking(self):
        if self.tracking_mode != 'hand':
            self.tracking_mode = 'hand'
            self.hand_tracking_button.config(text="Stop Hand Tracking")
            self.eye_tracking_button.config(state="disabled")

            cap = cv2.VideoCapture(0)
            hand_detector = mp.solutions.hands.Hands()
            drawing_utils = mp.solutions.drawing_utils
            screen_width, screen_height = pyautogui.size()
            index_y = 0
            while True:
                _, frame = cap.read()
                frame = cv2.flip(frame, 1)
                frame_height, frame_width, _ = frame.shape
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                output = hand_detector.process(rgb_frame)
                hands = output.multi_hand_landmarks
                if hands:
                    for hand in hands:
                        drawing_utils.draw_landmarks(frame, hand)
                        landmarks = hand.landmark
                        for id, landmark in enumerate(landmarks):
                            x = int(landmark.x*frame_width)
                            y = int(landmark.y*frame_height)
                            if id == 8:
                                cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                                index_x = screen_width/frame_width*x
                                index_y = screen_height/frame_height*y

                            if id == 4:
                                cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                                thumb_x = screen_width/frame_width*x
                                thumb_y = screen_height/frame_height*y
                                print('outside', abs(index_y - thumb_y))
                                if abs(index_y - thumb_y) < 20:
                                    pyautogui.click()
                                    pyautogui.sleep(1)
                                elif abs(index_y - thumb_y) < 100:
                                    pyautogui.moveTo(index_x, index_y)
                cv2.imshow('Virtual Mouse', frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            self.tracking_mode = None

root = tk.Tk()
app = HandEyeTrackingApp(root)
root.mainloop()