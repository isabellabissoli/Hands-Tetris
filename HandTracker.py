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
        self.detector = HandDetector()

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
    
    def start_hands(self):
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Falha ao capturar imagem.")
                break
            
            image = self.detector.find_hands(image)

            self.process_fingers(image)
        

    def process_fingers(self, image):

        left_thumb_up_prev, right_thumb_up_prev = False, False
        left_index_open_prev, right_index_open_prev = False, False
        right_pinky_up_prev = False    #mindinho direito
        
        # Inicializa variáveis de estado dos dedos
        left_index_open = False
        right_index_open = False
        left_thumb_up = False
        right_thumb_up = False
        right_pinky_up = False

        if self.detector.results.multi_hand_landmarks:
            for hand_no, _ in enumerate(self.detector.results.multi_hand_landmarks):
                lm_list = self.detector.find_position(image, hand_no)
                
                if hand_no == 0:
                    left_index_open = self.detector.is_index_finger_open(lm_list)
                    left_thumb_up = self.detector.is_thumb_up(lm_list)
                elif hand_no == 1:
                    right_index_open = self.detector.is_index_finger_open(lm_list)
                    right_thumb_up = self.detector.is_thumb_up(lm_list)
                    right_pinky_up = self.detector.is_pinky_up(lm_list)

        # Simula os comandos de teclado usando pynput
        if right_index_open_prev and not right_index_open: #Indicaador direito
            self.keyboard.press('w')  # Pressiona a tecla 'w'
            self.keyboard.release('w')  # Solta a tecla 'w'
        if left_thumb_up_prev and not left_thumb_up: #dedao esquerdo
            self.keyboard.press('a')  
            self.keyboard.release('a')  
        if right_thumb_up_prev and not right_thumb_up: 
            self.keyboard.press('d')  
            self.keyboard.release('d')  
        if left_index_open_prev and not left_index_open:
            self.keyboard.press(' ')  #espaço
            self.keyboard.release(' ')  
        if right_pinky_up_prev and not right_pinky_up:  
            self.keyboard.press('s')
            self.keyboard.release('s')

        # Atualiza os estados dos dedos
        left_thumb_up_prev, right_thumb_up_prev = left_thumb_up, right_thumb_up
        left_index_open_prev, right_index_open_prev = left_index_open, right_index_open
        right_pinky_up_prev = right_pinky_up

        statuses = [
            f'Polegar Esq: {"Aberto" if left_thumb_up else "Fechado"}',
            f'Polegar Dir: {"Aberto" if right_thumb_up else "Fechado"}',
            f'Indicador Esq: {"Aberto" if left_index_open else "Fechado"}',
            f'Indicador Dir: {"Aberto" if right_index_open else "Fechado"}',
            f'Mindinho Dir: {"Aberto" if right_pinky_up else "Fechado"}'
        ]

        for i, status in enumerate(statuses):
            cv2.putText(image, status, (10, 30 * (i + 1)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)   

