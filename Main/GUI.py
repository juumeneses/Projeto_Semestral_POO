import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton

class SelecionaMao(QWidget):
    def __init__(self, ):
        super().__init__()
        self.mao_usada = None  # Variável para armazenar a seleção
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Adicionar a mensagem de boas-vindas no topo centralizado
        welcome_label = QLabel("Bem-vindo ao Hand Tracker")
        #welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(welcome_label)

        label = QLabel("Selecione a mão:")
        layout.addWidget(label)

        self.radio_left = QRadioButton("Esquerda")
        self.radio_left.toggled.connect(self.select_left)
        layout.addWidget(self.radio_left)

        self.radio_right = QRadioButton("Direita")
        self.radio_right.toggled.connect(self.select_right)
        layout.addWidget(self.radio_right)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.save_selection)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def select_left(self):
        if self.radio_left.isChecked():
            self.mao_usada  = "esquerda"

    def select_right(self):
        if self.radio_right.isChecked():
            self.mao_usada = "direita"

    def save_selection(self):
        if self.mao_usada:
            print(f"Seleção: {self.mao_usada}")
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SelecionaMao()
    window.setWindowTitle("Seleção de Mão")
    window.show()
    sys.exit(app.exec_())
