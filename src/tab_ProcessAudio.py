from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QProgressBar, QLineEdit, QComboBox, QTextEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


def setup_processing_tab(self):
        # Componentes de la pestaña de procesamiento
        self.input_textbox = QLineEdit(self)
        self.input_textbox.setPlaceholderText("Carpeta de entrada...")
        self.input_textbox.setReadOnly(True)

        self.output_textbox1 = QLineEdit(self)
        self.output_textbox1.setPlaceholderText("Carpeta de salida...")
        self.output_textbox1.setReadOnly(True)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.progress_bar = QProgressBar(self)

        self.voice_config_dropdown = QComboBox(self)
        self.voice_config_dropdown.addItems(["Hombre-Hombre", "Hombre-Mujer", "Mujer-Hombre", "Mujer-Mujer"])

        # Botones con íconos
        self.select_input_btn = QPushButton(QIcon("C:/Users/molqueda/OneDrive - Comunycarse, S.L/Documentos/banca/scripts/icons/copy-writing.png"), "")
        self.select_input_btn.setToolTip("Seleccionar Carpeta de Entrada")
        self.select_input_btn.setIconSize(QSize(48, 48))
        self.select_input_btn.setMinimumSize(60, 60)

        self.select_output_btn = QPushButton(QIcon("C:/Users/molqueda/OneDrive - Comunycarse, S.L/Documentos/banca/scripts/icons/folder.png"), "")
        self.select_output_btn.setToolTip("Seleccionar Carpeta de Salida")
        self.select_output_btn.setIconSize(QSize(48,48))
        self.select_output_btn.setMinimumSize(60,60)

        self.process_btn = QPushButton(QIcon("C:/Users/molqueda/OneDrive - Comunycarse, S.L/Documentos/banca/scripts/icons/ai.png"), "  Procesar")
        self.process_btn.setToolTip("Procesar Transcripciones")

        # Layout principal
        layout = QVBoxLayout()

        # Layout para los botones de selección
        input_output_layout = QHBoxLayout()
        input_output_layout.addWidget(self.select_input_btn, alignment=Qt.AlignLeft)
        input_output_layout.addWidget(self.input_textbox, stretch=1)
        input_output_layout.addWidget(self.select_output_btn, alignment=Qt.AlignRight)
        input_output_layout.addWidget(self.output_textbox1, stretch=1)

        layout.addLayout(input_output_layout)
        layout.addWidget(self.voice_config_dropdown)
        layout.addWidget(self.process_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_output)

        # Contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.tab_processing.setLayout(layout)

        # Conectar eventos
        self.select_input_btn.clicked.connect(self.select_input_folder)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.process_btn.clicked.connect(self.process_files)

        # Variables para las rutas y configuración
        self.input_dir = None
        self.output_dir = None
        self.processing_thread = None