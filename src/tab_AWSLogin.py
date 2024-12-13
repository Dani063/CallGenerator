from PyQt5.QtWidgets import (
    QTextEdit, QPushButton, QLabel, QVBoxLayout
)
from PyQt5.QtCore import Qt

def setup_aws_login_tab(self):
        # Crear un layout vertical para la pestaña de AWS Login
        layout = QVBoxLayout()

        # Crear un QLabel para instrucciones
        instructions_label = QLabel("""
        <h2>Iniciar Sesión en AWS</h2>
        <p>Para utilizar Amazon Polly es necesario loguearse en AWS</p>
        <p>Haz clic en el botón a continuación para iniciar sesión automaticmente en AWS utilizando el perfil <b>recordia</b>.</p>
        <p>Asegúrate de que tienes AWS CLI configurado en tu sistema.</p>
        """)
        instructions_label.setWordWrap(True)
        instructions_label.setTextFormat(Qt.RichText)
        layout.addWidget(instructions_label)

        # Botón para ejecutar el comando
        login_button = QPushButton("Iniciar Sesión con AWS SSO")
        layout.addWidget(login_button)

        # Área de log para mostrar resultados
        self.aws_log_output = QTextEdit()
        self.aws_log_output.setReadOnly(True)
        layout.addWidget(self.aws_log_output)

        # Conectar el botón a la función de inicio de sesión
        login_button.clicked.connect(self.run_aws_login)

        # Asignar el layout a la pestaña de AWS Login
        self.tab_aws_login.setLayout(layout)