from HandTracker import HandDetector
import cv2

class HandControlProcessor:
    def __init__(self):
        self.detector = HandDetector()
        self.prev_states = {
            'left_thumb_up': False,
            'right_thumb_up': False,
            'left_index_open': False,
            'right_index_open': False,
            'right_pinky_up': False,
        }

    def initialize_video_capture(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Falha ao acessar a câmera.")
        return cap

    def process_frame(self, image):
        image = self.detector.find_hands(image)
        current_states = {
            'left_thumb_up': False,
            'right_thumb_up': False,
            'left_index_open': False,
            'right_index_open': False,
            'right_pinky_up': False,
        }

        if self.detector.results.multi_hand_landmarks:
            for hand_no, _ in enumerate(self.detector.results.multi_hand_landmarks):
                lm_list = self.detector.find_position(image, hand_no)
                if hand_no == 0:
                    current_states['left_index_open'] = self.detector.is_index_finger_open(lm_list)
                    current_states['left_thumb_up'] = self.detector.is_thumb_up(lm_list)
                elif hand_no == 1:
                    current_states['right_index_open'] = self.detector.is_index_finger_open(lm_list)
                    current_states['right_thumb_up'] = self.detector.is_thumb_up(lm_list)
                    current_states['right_pinky_up'] = self.detector.is_pinky_up(lm_list)

        return image, current_states

    def display_status(self, image, states):
        statuses = [
            f"Polegar Esq: {'Aberto' if states['left_thumb_up'] else 'Fechado'}",
            f"Polegar Dir: {'Aberto' if states['right_thumb_up'] else 'Fechado'}",
            f"Indicador Esq: {'Aberto' if states['left_index_open'] else 'Fechado'}",
            f"Indicador Dir: {'Aberto' if states['right_index_open'] else 'Fechado'}",
            f"Mindinho Dir: {'Aberto' if states['right_pinky_up'] else 'Fechado'}",
        ]
        for i, status in enumerate(statuses):
            cv2.putText(image, status, (10, 30 * (i + 1)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    def start_ai(self):
        cap = self.initialize_video_capture()

        while True:
            success, image = cap.read()
            if not success:
                print("Falha ao capturar imagem.")
                break

            image, current_states = self.process_frame(image)
            self.detector.process_gestures(self.prev_states, current_states)
            self.display_status(image, current_states)

            cv2.imshow('Hand Tracking', image)
            self.prev_states = current_states

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
