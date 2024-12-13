from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout
)
from PyQt5.QtCore import Qt

def setup_help_tab(self):
        # Crear un layout vertical para la pestaña de Ayuda
        layout = QVBoxLayout()

        # Crear un QLabel con las instrucciones de uso
        help_text = QLabel("""
        <h2>Cómo usar la aplicación</h2>
        <p>Esta aplicación permite procesar archivos de audio y convertir texto en audio usando Amazon Polly generando asi conversaciones.</p>
        
        <h3>Procesar Archivos</h3>
        <ol>
            <li>En la pestaña <b>Procesar Archivos</b>, selecciona una carpeta de salida donde guardar los archivos procesados.</li>
            <li>Selecciona los archivos de audio que deseas procesar y haz clic en "Procesar".</li>
            <li>Consulta el log para verificar el progreso y los resultados.</li>
        </ol>

        <h3>Texto a Voz</h3>
        <ol>
            <li>En la pestaña <b>Texto a Voz</b>, escribe el texto que deseas convertir en audio.</li>
            <li>Selecciona una carpeta de salida y una configuración de voz.</li>
            <li>Haz clic en "Convertir" para generar el archivo de audio.</li>
        </ol>

        <h3>Atajos y Consejos</h3>
        <ul>
            <li>Usa la función de selección de generos para definir rápidamente el genero de agente y cliente.</li>
            <li>Si no se definen Cliente y Agente puedes obtener un audio simple del texto introducido</li>
            <li>Consulta el log en tiempo real para asegurarte de que todo funciona correctamente.</li>
        </ul>

        <p><b>Nota:</b> Asegúrate de tener permisos de escritura en la carpeta seleccionada y de que los archivos de entrada tengan el formato adecuado (.txt).</p>
        """)
        
        # Hacer que el texto del QLabel sea ajustable y permita scroll si es muy largo
        help_text.setWordWrap(True)
        help_text.setTextFormat(Qt.RichText)
        help_text.setAlignment(Qt.AlignTop)

        # Agregar el QLabel al layout
        layout.addWidget(help_text)

        # Asignar el layout a la pestaña de ayuda
        self.tab_help.setLayout(layout)