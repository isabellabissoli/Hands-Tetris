import os
import webbrowser
from pynput.keyboard import Controller
import time
import cv2
import mediapipe as mp
from HandTracker import HandDetector

            

    
def main():

    #camminho absolto
    # html_file = os.path.abspath("tetris_js/index.html") 

    # # Abre o arquivo HTML no navegador padrão
    # webbrowser.open(f"file://{html_file}")

    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    # Cria um controlador de teclado    
    keyboard = Controller() 
    
    left_thumb_up_prev, right_thumb_up_prev = False, False
    left_index_open_prev, right_index_open_prev = False, False
    right_pinky_up_prev = False    #mindinho direito

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Falha ao capturar imagem.")
            break
        
        image = detector.find_hands(image)
        
        # Inicializa variáveis de estado dos dedos
        left_index_open = False
        right_index_open = False
        left_thumb_up = False
        right_thumb_up = False
        right_pinky_up = False

        if detector.results.multi_hand_landmarks:
            for hand_no, hand_landmarks in enumerate(detector.results.multi_hand_landmarks):
                lm_list = detector.find_position(image, hand_no)
                
                if hand_no == 0:
                    left_index_open = detector.is_index_finger_open(lm_list)
                    left_thumb_up = detector.is_thumb_up(lm_list)
                elif hand_no == 1:
                    right_index_open = detector.is_index_finger_open(lm_list)
                    right_thumb_up = detector.is_thumb_up(lm_list)
                    right_pinky_up = detector.is_pinky_up(lm_list)

        # Simula os comandos de teclado usando pynput
        if right_index_open_prev and not right_index_open: #Indicaador direito
            keyboard.press('w')  # Pressiona a tecla 'w'
            keyboard.release('w')  # Solta a tecla 'w'
        if left_thumb_up_prev and not left_thumb_up: #dedao esquerdo
            keyboard.press('a')  
            keyboard.release('a')  
        if right_thumb_up_prev and not right_thumb_up: 
            keyboard.press('d')  
            keyboard.release('d')  
        if left_index_open_prev and not left_index_open:
            keyboard.press(' ')  #espaço
            keyboard.release(' ')  
        if right_pinky_up_prev and not right_pinky_up:  
            keyboard.press('s')
            keyboard.release('s')

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

        # Exibe a imagem com os estados
        cv2.imshow('Hand Tracking', image)
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()