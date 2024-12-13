import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from CreadorDeConversacionV3 import procesar_transcripcion

class ProcessingThread(QThread):
    # Se definen señales para actualizar la barra de progreso y el log
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, config_voz):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.config_voz = config_voz

    def run(self):
        try:
            # Listar archivos de entrada
            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f)) and f.endswith(".txt")
            ]
            total_files = len(files)

            if total_files == 0:
                self.log_updated.emit("No se encontraron archivos .txt en la carpeta seleccionada.")
                return

            self.log_updated.emit(f"Se encontraron {total_files} archivos .txt para procesar.")
            os.makedirs(self.output_dir, exist_ok=True)

            # Procesar archivos uno por uno
            for i, filename in enumerate(files, start=1):
                file_path = os.path.join(self.input_dir, filename)
                self.log_updated.emit(f"Procesando archivo: {filename}")
                procesar_transcripcion(file_path, self.output_dir, self.config_voz)
                progress = int((i / total_files) * 100)
                self.progress_updated.emit(progress)

            self.log_updated.emit("Procesamiento completado con éxito.")
        except Exception as e:
            self.log_updated.emit(f"Error durante el procesamiento: {str(e)}")