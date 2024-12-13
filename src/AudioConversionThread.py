import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from CreadorDeConversacionV3 import procesar_transcripcion

class AudioConversionThread(QThread):
    # Se definen señales para actualizar la barra de progreso y el log
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)

    def __init__(self, text, output_folder, voice_config):
        super().__init__()
        self.text = text
        self.output_folder = output_folder
        self.voice_config = voice_config

    def run(self):
        try:
            self.log_updated.emit("Convirtiendo texto a audio...")

            # Generar el archivo de texto
            txt_filename = os.path.join(self.output_folder, "texto_a_convertir.txt")
            with open(txt_filename, 'w', encoding='utf-8') as file:
                file.write(self.text)

            if not os.path.exists(txt_filename):
                self.log_updated.emit(f"Error: No se pudo crear el archivo {txt_filename}.")
                return

            self.log_updated.emit(f"Procesando el archivo de texto: {txt_filename}")
            
            procesar_transcripcion(txt_filename, self.output_folder, self.voice_config)
            audio_file = os.path.join(self.output_folder, "audio_output.mp3")
            self.log_updated.emit(f"Audio guardado en: {audio_file}")
            self.progress_updated.emit(100)

            # Eliminar el archivo de texto tras la conversión
            os.remove(txt_filename)
            self.log_updated.emit(f"Archivo de texto {txt_filename} eliminado.")

        except Exception as e:
            self.log_updated.emit(f"Error durante la conversión: {str(e)}")
            self.progress_updated.emit(0)