#instalador

import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QLabel, QVBoxLayout, QPushButton, QCheckBox, QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class PyToExeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de .py para .exe")
        self.setFixedSize(500, 400)
        
        # Estilo translúcido e bordas arredondadas
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)

        # Layout e widgets
        layout = QVBoxLayout(self)

        label = QLabel("Converta arquivos .py para .exe:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.select_py_btn = QPushButton("Selecionar Arquivo .py")
        self.select_py_btn.clicked.connect(self.select_py_file)
        layout.addWidget(self.select_py_btn)

        self.py_file_label = QLabel("")
        self.py_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.py_file_label)

        self.icon_checkbox = QCheckBox("Deseja adicionar um ícone?")
        self.icon_checkbox.stateChanged.connect(self.toggle_icon_selection)
        layout.addWidget(self.icon_checkbox)

        self.select_icon_btn = QPushButton("Selecionar Ícone (.ico)")
        self.select_icon_btn.clicked.connect(self.select_icon_file)
        self.select_icon_btn.setEnabled(False)
        layout.addWidget(self.select_icon_btn)

        self.icon_file_label = QLabel("")
        self.icon_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_file_label)

        self.select_output_btn = QPushButton("Selecionar Pasta de Destino")
        self.select_output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.select_output_btn)

        self.output_folder_label = QLabel("")
        self.output_folder_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output_folder_label)

        self.convert_btn = QPushButton("Converter para .exe")
        self.convert_btn.clicked.connect(self.convert_to_exe)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)

        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close_program)
        layout.addWidget(close_btn)

        # Variáveis para os caminhos
        self.py_file = ""
        self.icon_file = ""
        self.output_folder = ""

    def select_py_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo .py", "", "Python Files (*.py)")
        if file:
            self.py_file = file
            self.py_file_label.setText(f"Arquivo selecionado: {file}")
            self.check_ready_to_convert()

    def toggle_icon_selection(self):
        self.select_icon_btn.setEnabled(self.icon_checkbox.isChecked())

    def select_icon_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo .ico", "", "Icon Files (*.ico)")
        if file:
            self.icon_file = file
            self.icon_file_label.setText(f"Ícone selecionado: {file}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta de destino")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Pasta de destino: {folder}")
            self.check_ready_to_convert()

    def check_ready_to_convert(self):
        if self.py_file and self.output_folder:
            self.convert_btn.setEnabled(True)

    def convert_to_exe(self):
        if not self.py_file or not self.output_folder:
            QMessageBox.critical(self, "Erro", "Por favor, selecione o arquivo .py e a pasta de destino.")
            return

        try:
            # Monta o comando para PyInstaller
            command = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                f"--distpath={self.output_folder}",
                self.py_file
            ]

            if self.icon_checkbox.isChecked() and self.icon_file:
                command.append(f"--icon={self.icon_file}")

            # Executa o comando
            subprocess.run(command, check=True)

            QMessageBox.information(self, "Sucesso", "Arquivo .exe criado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao converter: {str(e)}")

    def close_program(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication([])

    # Personalização global
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255, 180))
    app.setPalette(palette)

    window = PyToExeApp()
    window.show()

    app.exec()
