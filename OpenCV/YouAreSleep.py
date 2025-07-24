import os
import cv2
import numpy as np
import mediapipe as mp
import pygame
import threading
import time
from collections import deque

#Hola aqui encontraras un detector de somnolencia que utiliza la libreria mediapipe para detectar los ojos y calcular el EAR (Eye Aspect Ratio) y asi determinar si estas somnoliento o no, ademas de reproducir un sonido de alerta si es necesario.

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pygame.mixer.init()


EAR_THRESHOLD_DEFAULT = 0.25
FRAMES_CONSECUTIVOS = 20
CALIBRATION_FRAMES = 30
ALERT_COOLDOWN = 3


SOUND_PATHS = [
    "alarm-clock.mp3", 
    "gg.wav",  
    "Python/Proyect/OpenCV/alarm-clock.mp3",  
    "Python\\Proyect\\OpenCV\\alarm-clock.mp3",  
    "Python/Proyect/OpenCV/gg.wav",  
    "Python\\Proyect\\OpenCV\\gg.wav",  
    os.path.join("Python", "Proyect", "OpenCV", "alarm-clock.mp3"), 
    os.path.join("Python", "Proyect", "OpenCV", "gg.wav"),  
    os.path.join(os.path.expanduser("~"), "Python", "Proyect", "OpenCV", "alarm-clock.mp3"),  
    os.path.join(os.path.expanduser("~"), "Python", "Proyect", "OpenCV", "gg.wav"),  #
]

FONT = cv2.FONT_HERSHEY_SIMPLEX

class DrowsinessDetector:
    def __init__(self):
        # MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Índices de ojos (MediaPipe)
        self.LEFT_EYE_IDX = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]

        # Parámetros
        self.EAR_THRESHOLD = EAR_THRESHOLD_DEFAULT
        self.ear_history = deque(maxlen=CALIBRATION_FRAMES)
        self.contador_frames = 0
        self.is_calibrated = False
        self.calibration_frames = 0

        # Alertas
        self.last_alert_time = 0
        self.alert_cooldown = ALERT_COOLDOWN
        self.sound_playing = False
        self.alert_sound_path = self.find_sound_file()
        self.alert_sound = self.load_sound()
        self.sound_object = None  

    def find_sound_file(self):
        """Busca el archivo de audio en múltiples ubicaciones posibles."""
        print("🔊 Buscando archivo de audio...")
        
        for path in SOUND_PATHS:
            full_path = os.path.abspath(path)
            print(f"   Verificando: {full_path}")
            
            if os.path.exists(path):
                print(f"✅ Archivo encontrado: {full_path}")
                return path
        
        print("❌ Archivo de audio no encontrado en ninguna ubicación.")
        print("\n📁 Ubicaciones verificadas:")
        for path in SOUND_PATHS:
            print(f"   - {os.path.abspath(path)}")
        
        print(f"\n💡 Directorio actual del script: {os.getcwd()}")
        print("💡 Asegúrate de que el archivo 'gg.wav' esté en una de estas ubicaciones.")
        
        return None

    def load_sound(self):
        """Carga el sonido de alerta si existe."""
        if not self.alert_sound_path:
            return False
            
        
        file_ext = os.path.splitext(self.alert_sound_path)[1].lower()
        
       
        if file_ext == '.mp3':
            try:
                pygame.mixer.music.load(self.alert_sound_path)
                print(f"✅ Sonido MP3 cargado exitosamente: {self.alert_sound_path}")
                return "music"
            except Exception as e:
                print(f"❌ Error al cargar MP3: {e}")
                return False
        
        
        elif file_ext == '.wav':
            
            try:
                self.sound_object = pygame.mixer.Sound(self.alert_sound_path)
                print(f"✅ Sonido WAV cargado como Sound object: {self.alert_sound_path}")
                return "sound_object"
            except Exception as e:
                print(f"❌ Error al cargar WAV con Sound: {e}")
                
                
                try:
                    pygame.mixer.music.load(self.alert_sound_path)
                    print(f"✅ Sonido WAV cargado como música: {self.alert_sound_path}")
                    return "music"
                except Exception as e2:
                    print(f"❌ Error al cargar WAV con music: {e2}")
                    print("💡 El archivo WAV puede tener un formato incompatible.")
                    return False
        
        
        else:
            try:
                pygame.mixer.music.load(self.alert_sound_path)
                print(f"✅ Sonido cargado exitosamente: {self.alert_sound_path}")
                return "music"
            except Exception as e:
                print(f"❌ Error al cargar sonido: {e}")
                return False

    def play_alert(self):
        """Reproduce la alerta en un hilo separado."""
        current_time = time.time()
        if (current_time - self.last_alert_time < self.alert_cooldown or 
            self.sound_playing or not self.alert_sound):
            return

        def play():
            self.sound_playing = True
            try:
                if self.alert_sound == "sound_object" and self.sound_object:
                   
                    self.sound_object.play()
                    print("🔊 Reproduciendo alerta con Sound object...")
                    
                    time.sleep(1)
                else:
                    
                    pygame.mixer.music.play()
                    print("🔊 Reproduciendo alerta de sonido...")
                    
                    wait_time = 0
                    while pygame.mixer.music.get_busy() and wait_time < 5:
                        time.sleep(0.1)
                        wait_time += 0.1
            except Exception as e:
                print(f"❌ Error reproduciendo sonido: {e}")
            finally:
                self.sound_playing = False

        threading.Thread(target=play, daemon=True).start()
        self.last_alert_time = current_time

    def eye_aspect_ratio(self, landmarks, indices, frame_shape):
        """Calcula el EAR (Eye Aspect Ratio) dado los landmarks y los índices."""
        h, w = frame_shape
        eye = np.array([
            (int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices
        ], dtype=np.int32)

        A = np.linalg.norm(eye[1] - eye[5])  
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])  

        return (A + B) / (2.0 * C) if C > 0 else 0, eye

    def calibrate(self, ear):
        """Calibración automática del umbral EAR."""
        if self.is_calibrated:
            return True

        self.ear_history.append(ear)
        self.calibration_frames += 1

        if self.calibration_frames >= CALIBRATION_FRAMES:
            avg_ear = np.mean(self.ear_history)
            self.EAR_THRESHOLD = max(0.2, avg_ear * 0.75)
            self.is_calibrated = True
            print(f"🎯 Calibración completada. Umbral EAR: {self.EAR_THRESHOLD:.3f}")

        return self.is_calibrated

    def draw_eye_contours(self, frame, left_eye, right_eye):
        """Dibuja los contornos de los ojos."""
        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

    def show_alert(self, frame):
        """Muestra alerta visual y reproduce sonido."""
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, 0), (w, 100), (0, 0, 255), -1)
        cv2.putText(frame, "¡ALERTA DE SOMNOLENCIA!", (10, 40),
                    FONT, 1.2, (255, 255, 255), 3)
        cv2.putText(frame, "¡MANTENTE DESPIERTO!", (10, 80),
                    FONT, 1.0, (255, 255, 255), 2)
        
        # Mostrar estado del audio
        if not self.alert_sound:
            cv2.putText(frame, "Audio no disponible", (w-200, h-20),
                        FONT, 0.5, (255, 255, 0), 1)
        
        self.play_alert()

    def detect_drowsiness(self, frame):
        """Procesa un frame y detecta somnolencia."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        h, w = frame.shape[:2]

        drowsy = False
        ear_value = 0

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                left_ear, left_eye_coords = self.eye_aspect_ratio(
                    face_landmarks.landmark, self.LEFT_EYE_IDX, (h, w))
                right_ear, right_eye_coords = self.eye_aspect_ratio(
                    face_landmarks.landmark, self.RIGHT_EYE_IDX, (h, w))
                ear_value = (left_ear + right_ear) / 2.0

                
                if not self.calibrate(ear_value):
                    cv2.putText(frame, f"Calibrando... {self.calibration_frames}/{CALIBRATION_FRAMES}",
                                (10, 30), FONT, 0.7, (255, 255, 0), 2)
                    ear_value = 0  # Ocultar EAR durante calibración
                else:
                    # Dibujar ojos
                    self.draw_eye_contours(frame, left_eye_coords, right_eye_coords)

                    # Detección de somnolencia
                    if ear_value < self.EAR_THRESHOLD:
                        self.contador_frames += 1
                        if self.contador_frames >= FRAMES_CONSECUTIVOS:
                            drowsy = True
                            self.show_alert(frame)
                    else:
                        self.contador_frames = 0

        return frame, drowsy, ear_value

    def run(self):
        """Ejecuta el detector en tiempo real."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: No se pudo abrir la cámara.")
            return

        print("🚗 Detector de somnolencia iniciado.")
        print("Presiona 'q' para salir, 'r' para recalibrar.")
        
        if self.alert_sound:
            print("🔊 Audio de alerta listo.")
        else:
            print("⚠️  Funcionando sin audio de alerta.")

        fps = 0
        fps_counter = 0
        fps_start = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: No se pudo leer el frame.")
                break

            
            frame, is_drowsy, ear = self.detect_drowsiness(frame)

            # Actualizar FPS cada 10 frames
            fps_counter += 1
            if fps_counter >= 10:
                fps = fps_counter / (time.time() - fps_start)
                fps_counter = 0
                fps_start = time.time()

           
            h = frame.shape[0]
            if self.is_calibrated and ear > 0:
                color = (0, 0, 255) if is_drowsy else (0, 255, 0)
                cv2.putText(frame, f"EAR: {ear:.3f}", (10, h - 80), FONT, 0.7, color, 2)
                cv2.putText(frame, f"Umbral: {self.EAR_THRESHOLD:.3f}", (10, h - 50), FONT, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, h - 20), FONT, 0.7, (255, 255, 255), 2)

            cv2.imshow("Detector de Somnolencia", frame)

            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                print("🔄 Recalibrando...")
                self.is_calibrated = False
                self.calibration_frames = 0
                self.ear_history.clear()
                self.contador_frames = 0

       
        cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        pygame.mixer.quit()
        print("👋 Detector finalizado.")


if __name__ == "__main__":
    detector = DrowsinessDetector()
    detector.run()