import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2
import mediapipe as mp
import numpy as np
import logging
from typing import Tuple, Dict, List, Optional
import math

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HandGestureRecognizer:


    def __init__(self, static_mode: bool = False, max_hands: int = 2):

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.logger = logging.getLogger('HandGestureRecognizer')

        # Definiciones de los puntos clave para los dedos
        self.FINGER_TIPS = {
            'thumb': self.mp_hands.HandLandmark.THUMB_TIP,
            'index': self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            'middle': self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            'ring': self.mp_hands.HandLandmark.RING_FINGER_TIP,
            'pinky': self.mp_hands.HandLandmark.PINKY_TIP
        }
        self.FINGER_PIPS = {
            'thumb': self.mp_hands.HandLandmark.THUMB_IP,
            'index': self.mp_hands.HandLandmark.INDEX_FINGER_PIP,
            'middle': self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
            'ring': self.mp_hands.HandLandmark.RING_FINGER_PIP,
            'pinky': self.mp_hands.HandLandmark.PINKY_PIP,
        }
        self.FINGER_MCPS = {
            'thumb': self.mp_hands.HandLandmark.THUMB_CMC,
            'index': self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
            'middle': self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
            'ring': self.mp_hands.HandLandmark.RING_FINGER_MCP,
            'pinky': self.mp_hands.HandLandmark.PINKY_MCP,
        }
        self.FINGER_NAMES = ['thumb', 'index', 'middle', 'ring', 'pinky']

    def _is_finger_extended(self, landmarks, finger_name: str) -> bool:

        try:
            if finger_name == 'thumb':
                # Para el pulgar, comparamos la punta con la articulación IP
                tip = landmarks.landmark[self.FINGER_TIPS['thumb']]
                ip = landmarks.landmark[self.FINGER_PIPS['thumb']]
                mcp = landmarks.landmark[self.FINGER_MCPS['thumb']]
                
                # El pulgar está extendido si se aleja del centro de la mano
                wrist = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                
                # Calculamos si el pulgar está "hacia afuera"
                dist_tip_wrist = math.hypot(tip.x - wrist.x, tip.y - wrist.y)
                dist_ip_wrist = math.hypot(ip.x - wrist.x, ip.y - wrist.y)
                
                return dist_tip_wrist > dist_ip_wrist
            else:
                # Para otros dedos, la punta debe estar más arriba que la articulación PIP
                tip_y = landmarks.landmark[self.FINGER_TIPS[finger_name]].y
                pip_y = landmarks.landmark[self.FINGER_PIPS[finger_name]].y
                
                return tip_y < pip_y
        except (KeyError, AttributeError):
            return False

    def _get_extended_fingers(self, landmarks) -> List[str]:
        
        return [finger for finger in self.FINGER_NAMES if self._is_finger_extended(landmarks, finger)]

    def _is_thumb_up(self, landmarks) -> bool:
        
        extended = self._get_extended_fingers(landmarks)
        
        # Solo el pulgar extendido
        if len(extended) == 1 and 'thumb' in extended:
            thumb_tip = landmarks.landmark[self.FINGER_TIPS['thumb']]
            thumb_mcp = landmarks.landmark[self.FINGER_MCPS['thumb']]
            
            # El pulgar debe estar apuntando hacia arriba
            return thumb_tip.y < thumb_mcp.y
        return False

    def _is_thumb_down(self, landmarks) -> bool:
        
        extended = self._get_extended_fingers(landmarks)
        
        # Solo el pulgar extendido
        if len(extended) == 1 and 'thumb' in extended:
            thumb_tip = landmarks.landmark[self.FINGER_TIPS['thumb']]
            thumb_mcp = landmarks.landmark[self.FINGER_MCPS['thumb']]
            
            # El pulgar debe estar apuntando hacia abajo
            return thumb_tip.y > thumb_mcp.y
        return False

    def _is_middle_finger(self, landmarks) -> bool:
        
        extended = self._get_extended_fingers(landmarks)
        
        # Dedo medio extendido, otros doblados (puede incluir pulgar parcialmente)
        if 'middle' in extended:
            # Verificar que índice, anular y meñique NO estén extendidos
            forbidden_fingers = ['index', 'ring', 'pinky']
            for finger in forbidden_fingers:
                if finger in extended:
                    return False
            
            # Verificar que el medio esté significativamente más alto
            middle_tip = landmarks.landmark[self.FINGER_TIPS['middle']]
            index_tip = landmarks.landmark[self.FINGER_TIPS['index']]
            ring_tip = landmarks.landmark[self.FINGER_TIPS['ring']]
            
            # El medio debe estar más alto que índice y anular
            return (middle_tip.y < index_tip.y - 0.03 and 
                   middle_tip.y < ring_tip.y - 0.03)
        return False

    def _is_peace_sign(self, landmarks) -> bool:
        
        extended = self._get_extended_fingers(landmarks)
        
        # Solo índice y medio extendidos
        if len(extended) == 2 and 'index' in extended and 'middle' in extended:
            # Verificar que los dedos estén separados
            index_tip = landmarks.landmark[self.FINGER_TIPS['index']]
            middle_tip = landmarks.landmark[self.FINGER_TIPS['middle']]
            
            # Calcular distancia entre las puntas
            distance = math.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
            return distance > 0.03  # Umbral para dedos separados
        return False

    def _is_fist(self, landmarks) -> bool:
        
        extended = self._get_extended_fingers(landmarks)
        return len(extended) == 0

    def _is_rocker_sign(self, landmarks) -> bool:
        
        # Verificar dedos extendidos de manera más flexible
        index_extended = self._is_finger_extended(landmarks, 'index')
        pinky_extended = self._is_finger_extended(landmarks, 'pinky')
        middle_extended = self._is_finger_extended(landmarks, 'middle')
        ring_extended = self._is_finger_extended(landmarks, 'ring')
        
        # Índice y meñique deben estar extendidos
        if not (index_extended and pinky_extended):
            return False
        
        # Medio y anular deben estar doblados (más flexibilidad)
        if middle_extended or ring_extended:
            return False
        
        # Verificación adicional: las puntas del índice y meñique 
        # deben estar más altas que sus articulaciones MCP
        index_tip = landmarks.landmark[self.FINGER_TIPS['index']]
        pinky_tip = landmarks.landmark[self.FINGER_TIPS['pinky']]
        index_mcp = landmarks.landmark[self.FINGER_MCPS['index']]
        pinky_mcp = landmarks.landmark[self.FINGER_MCPS['pinky']]
        
        index_up = index_tip.y < index_mcp.y - 0.02
        pinky_up = pinky_tip.y < pinky_mcp.y - 0.02
        
        # Verificar que los dedos estén separados
        distance = math.hypot(index_tip.x - pinky_tip.x, index_tip.y - pinky_tip.y)
        separated = distance > 0.08
        
        return index_up and pinky_up and separated

    def _recognize_gestures(self, landmarks) -> Optional[str]:
        """
        Reconoce gestos basados en la configuración de los dedos.
        """
        # Verificar gestos específicos en orden de prioridad
        if self._is_thumb_up(landmarks):
            return "Me gusta"
        
        if self._is_thumb_down(landmarks):
            return "NO me gusta"
        
        if self._is_middle_finger(landmarks):
            return "Fuck you"
        
        if self._is_peace_sign(landmarks):
            return "Amor y Paz"
        
        if self._is_rocker_sign(landmarks):
            return "Nu Metal"
        
        if self._is_fist(landmarks):
            return "Punio"
        
        # Gestos adicionales
        extended = self._get_extended_fingers(landmarks)
        
        if len(extended) == 5:
            return "Mano Abierta"
        
        if len(extended) == 1 and 'index' in extended:
            return "Senialar"

        return None

    def _draw_gesture_info(self, frame, gesture, x, y):
        
        if gesture:
            # Fondo semi-transparente para el texto
            overlay = frame.copy()
            cv2.rectangle(overlay, (x-10, y-40), (x+200, y+10), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Texto del gesto
            cv2.putText(frame, gesture, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    def _draw_gesture_corner(self, frame, gesture):
        
        if gesture:
            # Fondo para el texto
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (300, 60), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            # Texto principal
            cv2.putText(frame, "Gesto Detectado:", (20, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, gesture, (20, 55), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
 

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        output_frame = frame.copy()
        hands_data = []
        detected_gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibuja las conexiones y puntos clave de la mano
                self.mp_drawing.draw_landmarks(
                    output_frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )

                # Reconoce el gesto actual
                gesture = self._recognize_gestures(hand_landmarks)
                if gesture:
                    detected_gesture = gesture
                
                # Obtiene las coordenadas de la muñeca para posicionar el texto
                wrist_landmark = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                h, w, _ = frame.shape
                wrist_x = int(wrist_landmark.x * w)
                wrist_y = int(wrist_landmark.y * h)

                # Dibuja el gesto cerca de la mano
                self._draw_gesture_info(output_frame, gesture, wrist_x, wrist_y)

                hands_data.append({
                    'gesture': gesture,
                    'is_present': True
                })

        # Dibuja el gesto en la esquina superior
        if detected_gesture:
            self._draw_gesture_corner(output_frame, detected_gesture)

        return output_frame, {'hands_data': hands_data, 'main_gesture': detected_gesture}

def main():
    """Función principal para ejecutar el reconocedor de gestos en la cámara."""
    logging.info("Inicializando Reconocedor de Gestos de Mano...")
    try:
        recognizer = HandGestureRecognizer()
        logging.info("Reconocedor inicializado correctamente.")
    except Exception as e:
        logging.error(f"Error al inicializar el reconocedor: {e}")
        return

    logging.info("Intentando conectar a la cámara...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Error: No se pudo acceder a la cámara. Asegúrate de que no esté en uso.")
        return

    logging.info("Cámara conectada.")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    logging.info("--- Reconocimiento de Gestos Iniciado ---")
    logging.info("Gestos detectables:")
    logging.info("  Amor y Paz (indice y medio)")
    logging.info("  Fuck you (solo medio)")
    logging.info("  Punio (todos los dedos cerrados)")
    logging.info("  Me gusta (pulgar arriba)")
    logging.info("  No me gusta (pulgar abajo)")
    logging.info("  Nu Metal (indice y meñique)")
    logging.info("Presiona 'q' para salir.")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                logging.warning("Ignorando frame vacío. ¿La cámara está funcionando?")
                continue

            frame = cv2.flip(frame, 1)  # Efecto espejo
            processed_frame, results = recognizer.process_frame(frame)
            
            # Log del gesto detectado
            if results.get('main_gesture'):
                logging.info(f"Gesto reconocido: {results['main_gesture']}")
            
            cv2.imshow('Detector de Gestos - Amor y Paz, Fuck you, Punio, Me gusta, No me gusta, Nu metal', processed_frame)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    except Exception as e:
        logging.error(f"Error inesperado: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Reconocedor finalizado.")

if __name__ == "__main__":
    main()