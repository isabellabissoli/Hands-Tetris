import cv2
import mediapipe as mp
from pynput.keyboard import Controller

class HandDetector:
    def __init__(self, static_mode=False, max_hands=2, detection_confidence=0.7, track_confidence=0.5):
        self.mode = static_mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.track_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        self.keyboard = Controller()

    def find_hands(self, image, draw=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)
        
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        return image
    
    def find_position(self, image, hand_no=0, draw=True):
        lm_list = []
        
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            
            for id, lm in enumerate(hand.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                
                if draw:
                    cv2.circle(image, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        
        return lm_list

    def is_index_finger_open(self, lm_list):
        if lm_list:
            return lm_list[self.tip_ids[1]][2] < lm_list[self.tip_ids[1] - 2][2]
        return False

    def is_thumb_up(self, lm_list):
        if lm_list:
            return lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]
        return False
    
    def is_pinky_up(self, lm_list):
        if lm_list:
            return lm_list[self.tip_ids[4]][2] < lm_list[self.tip_ids[4] - 2][2]
        return False

    def process_gestures(self, prev_states, current_states):
        if current_states['left_thumb_up'] and not prev_states['left_thumb_up']:
            self.keyboard.press('a')
            self.keyboard.release('a')
        if current_states['right_thumb_up'] and not prev_states['right_thumb_up']:
            self.keyboard.press('d')
            self.keyboard.release('d')
        if current_states['left_index_open'] and not prev_states['left_index_open']:
            self.keyboard.press(' ')
            self.keyboard.release(' ')
        if current_states['right_index_open'] and not prev_states['right_index_open']:
            self.keyboard.press('w')
            self.keyboard.release('w')
        if current_states['right_pinky_up'] and not prev_states['right_pinky_up']:
            self.keyboard.press('s')
            self.keyboard.release('s')
        