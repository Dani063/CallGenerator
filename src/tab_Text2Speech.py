from PyQt5.QtWidgets import (
    QHBoxLayout, QProgressBar, QLineEdit, QComboBox, QTextEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

def setup_text_to_speech_tab(self):
        # Cuadro de texto para escribir el contenido
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Agente: Buenas tardes, le habla Laura de Recordia. ¿Cómo puedo ayudarle? \n Cliente: Hola, soy Luis Fernández. Pues desde esta mañana...")
        self.text_input.setFixedHeight(150)

        # Configuración de voz
        self.voice_config_dropdown = QComboBox(self)
        self.voice_config_dropdown.addItems(["Hombre-Hombre", "Hombre-Mujer", "Mujer-Hombre", "Mujer-Mujer"])

        # Carpeta de salida
        self.output_textbox2 = QLineEdit(self)
        self.output_textbox2.setPlaceholderText("Carpeta de salida...")
        self.output_textbox2.setReadOnly(True)

        self.select_output_btn = QPushButton(QIcon("C:/Users/molqueda/OneDrive - Comunycarse, S.L/Documentos/banca/scripts/icons/folder.png"), "")
        self.select_output_btn.setToolTip("Seleccionar Carpeta de Salida")
        self.select_output_btn.setIconSize(QSize(48,48))
        self.select_output_btn.setMinimumSize(60,60)

        # Botón para convertir el texto en audio
        self.convert_btn = QPushButton("Convertir a Audio", self)
        self.convert_btn.clicked.connect(self.convert_text_to_audio)

        # Barra de progreso para el audio
        self.progress_bar = QProgressBar(self)

        # Layout de la pestaña de texto a voz
        layout = QVBoxLayout()

        input_output_layout = QHBoxLayout()
        input_output_layout.addWidget(self.select_output_btn, alignment=Qt.AlignLeft)
        input_output_layout.addWidget(self.output_textbox2, stretch=1)

        layout.addLayout(input_output_layout)
        layout.addWidget(self.text_input)
        layout.addWidget(self.voice_config_dropdown)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.progress_bar)

        # Contenedor principal de la pestaña
        self.tab_text_to_speech.setLayout(layout)

        # Conectar el botón para seleccionar la carpeta de salida
        self.select_output_btn.clicked.connect(self.select_output_folder)