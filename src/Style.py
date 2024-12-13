def apply_styles(self):
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QProgressBar {
            text-align: center;
            color: white;
            background: #ccc;
            border: 1px solid #999;
            height: 20px;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            width: 20px;
        }
        QComboBox {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        """
        self.setStyleSheet(style)