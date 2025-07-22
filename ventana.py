import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
)

class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setFixedSize(300, 400)

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        self.entrada = QLineEdit()
        self.entrada.setReadOnly(True)
        self.entrada.setStyleSheet("font-size: 24px; padding: 10px;")
        self.layout_principal.addWidget(self.entrada)

        self.crear_botones()

    def crear_botones(self):
        botones_layout = QGridLayout()

        # Todos los botones incluyen: texto, fila, columna, rowspan, colspan
        botones = [
            ('7', 0, 0, 1, 1), ('8', 0, 1, 1, 1), ('9', 0, 2, 1, 1), ('/', 0, 3, 1, 1),
            ('4', 1, 0, 1, 1), ('5', 1, 1, 1, 1), ('6', 1, 2, 1, 1), ('*', 1, 3, 1, 1),
            ('1', 2, 0, 1, 1), ('2', 2, 1, 1, 1), ('3', 2, 2, 1, 1), ('-', 2, 3, 1, 1),
            ('0', 3, 0, 1, 1), ('.', 3, 1, 1, 1), ('=', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('C', 4, 0, 1, 4)
        ]

        for texto, fila, col, rowspan, colspan in botones:
            boton = QPushButton(texto)
            boton.setFixedHeight(60)
            boton.setStyleSheet("font-size: 18px;")
            boton.clicked.connect(self.procesar_click)
            botones_layout.addWidget(boton, fila, col, rowspan, colspan)

        self.layout_principal.addLayout(botones_layout)

    def procesar_click(self):
        boton = self.sender()
        texto = boton.text()

        if texto == "C":
            self.entrada.setText("")
        elif texto == "=":
            try:
                resultado = str(eval(self.entrada.text()))
                self.entrada.setText(resultado)
            except:
                self.entrada.setText("Error")
        else:
            self.entrada.setText(self.entrada.text() + texto)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec())
