import sys
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTabWidget, QWidget
)
import ProcessingThread, AudioConversionThread
import tab_ProcessAudio, tab_Text2Speech, tab_AWSLogin, tab_Help
import Style


class AudioGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Audios con Polly")
        self.setGeometry(100, 100, 600, 450)
        self.setWindowIcon(QIcon("C:/Users/molqueda/OneDrive - Comunycarse, S.L/Documentos/banca/scripts/icons/recordia-logo.png"))

        # Crear el widget principal y las pestañas
        self.tab_widget = QTabWidget()

        # Pestaña de procesamiento de archivos
        self.tab_processing = QWidget()
        tab_ProcessAudio.setup_processing_tab()
        self.tab_widget.addTab(self.tab_processing, "Procesar Archivos")

        # Pestaña de texto a voz
        self.tab_text_to_speech = QWidget()
        tab_Text2Speech.setup_text_to_speech_tab()
        self.tab_widget.addTab(self.tab_text_to_speech, "Texto a Voz")

        self.tab_aws_login = QWidget()
        tab_AWSLogin.setup_aws_login_tab()
        self.tab_widget.addTab(self.tab_aws_login, "AWS Login")

        # Pestaña de Ayuda
        self.tab_help = QWidget()
        tab_Help.setup_help_tab()
        self.tab_widget.addTab(self.tab_help, "Ayuda")

        # Configurar el layout
        self.setCentralWidget(self.tab_widget)

        Style.apply_styles()

    def run_aws_login(self):
        """Ejecuta el comando `aws sso login --profile recordia` y muestra el resultado en el log."""
        self.aws_log_output.append("Iniciando sesión en AWS...")
        try:
            process = subprocess.run(
                ["aws", "sso", "login", "--profile", "recordia"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if process.returncode == 0:
                self.aws_log_output.append(f"Inicio de sesión exitoso:\n{process.stdout}")
            else:
                self.aws_log_output.append(f"Error durante el inicio de sesión:\n{process.stderr}")
        except Exception as e:
            self.aws_log_output.append(f"Error al intentar ejecutar el comando: {str(e)}")

    def convert_text_to_audio(self):
        # Obtener el texto desde el cuadro de texto
        text = self.text_input.toPlainText()
        output_folder = self.output_textbox.text()

        if not text:
            self.log_output.append("Por favor, escribe un texto para convertirlo a audio.")
            return

        if not output_folder:
            self.log_output.append("Por favor, selecciona una carpeta de salida.")
            return

        # Aquí es donde se realiza la conversión del texto a audio (simulado en este ejemplo)
        self.log_output.append("Convirtiendo texto a audio...")

        config_voz = self.voice_config_dropdown.currentText()
        self.log_output.append(f"Configuración de voz seleccionada: {config_voz}")

        self.audio_conversion_thread = AudioConversionThread(text, output_folder, config_voz)
        self.audio_conversion_thread.progress_updated.connect(self.update_progress)
        self.audio_conversion_thread.log_updated.connect(self.update_log)
        self.audio_conversion_thread.start()

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Entrada")
        if folder:
            self.input_dir = folder
            self.input_textbox.setText(folder)
            self.log_output.append(f"Seleccionada carpeta de entrada: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida")
        if folder:
            self.output_dir = folder
            self.output_textbox1.setText(folder)
            self.output_textbox2.setText(folder)
            self.log_output.append(f"Seleccionada carpeta de salida: {folder}")

    def process_files(self):
        if not self.input_dir or not self.output_dir:
            self.log_output.append("Por favor, selecciona ambas carpetas antes de procesar.")
            return

        config_voz = self.voice_config_dropdown.currentText()
        self.log_output.append(f"Configuración de voz seleccionada: {config_voz}")

        self.processing_thread = ProcessingThread(self.input_dir, self.output_dir, config_voz)
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.log_updated.connect(self.update_log)
        self.processing_thread.start()

        self.log_output.append("Iniciando procesamiento...")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_log(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()

def main():
    app = QApplication(sys.argv)
    window = AudioGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
