import cv2
import mediapipe as mp
import numpy as np
import sys
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton

# Importe a classe SelecionaMao do arquivo GUI
from GUI import SelecionaMao

class Automacao:
    def __init__(self):
        self.selected_direction = None  # Variável para armazenar a seleção da mão

    def mover_cursor(self, gesto):
        if gesto == "Up":
            pyautogui.keyDown('up')
        elif gesto == "Down":
            pyautogui.keyDown('down')
        elif gesto == "Left":
            pyautogui.keyDown('left')
        elif gesto == "Right":
            pyautogui.keyDown('right')

class Detector:
    def __init__(self, 
                 modo: bool = False, 
                 numero_maos: int = 2, 
                 complexidade_modelo: int = 1, 
                 confianca_detect: float = 0.5, 
                 confianca_rastreamento: float = 0.5):
        # Configurações do detector de mãos
        self.modo = modo
        self.numero_maos = numero_maos
        self.complexidade_modelo = complexidade_modelo
        self.confianca_detect = confianca_detect
        self.confianca_rastreamento = confianca_rastreamento
        self.mao_usada = None  # Inicialmente não há mão escolhida

        # Inicializa o mediapipe Hands
        self.mp_maos = mp.solutions.hands
        self.Maos = self.mp_maos.Hands(self.modo, self.numero_maos, self.complexidade_modelo, self.confianca_detect, self.confianca_rastreamento)
        self.pontos = []  # Armazena as coordenadas dos pontos das mãos
        self.mpDesenho = mp.solutions.drawing_utils

    def encontrar_maos(self, img):
        # Converte o frame para RGB, pois o modelo do mediapipe espera cores RGB
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processa o frame em busca de mãos
        resultados = self.Maos.process(img_RGB)
        pontos_mao = resultados.multi_hand_landmarks
        altura, largura, _ = img.shape
        self.pontos = []  # Limpa a lista de pontos em cada frame

        # Chama o método para detecção de gestos
        gesto = self.detectar_gesto(pontos_mao, altura, largura)

        if pontos_mao:
            for pontos in pontos_mao:
                # Desenha os landmarks das mãos no frame
                self.mpDesenho.draw_landmarks(img, pontos, self.mp_maos.HAND_CONNECTIONS)

        # Exibe o gesto detectado no frame
        cv2.putText(img, gesto, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 5)

        return img

    def detectar_gesto(self, pontos_mao, altura, largura):
        gesto = ""

        if pontos_mao:
            for pontos in pontos_mao:
                for id, cord in enumerate(pontos.landmark):
                    cx, cy = int(cord.x * largura), int(cord.y * altura)
                    self.pontos.append((cx, cy))  # Armazena as coordenadas dos pontos

                if self.mao_usada:
                    if self.mao_usada == "esquerda":
                        # Lógica para detecção de gestos da mão esquerda
                        if self.pontos[20][1] < self.pontos[18][1] and self.pontos[4][0] > self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1]: # so o mindinho
                            gesto = "Left" #mindinho
                        if self.pontos[4][0] < self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #dedao
                            gesto = "Right" #dedao
                        if self.pontos[8][1] < self.pontos[6][1] and self.pontos[4][0] > self.pontos[3][0] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #indicador
                            gesto = "Up" #indicador
                        if self.pontos[20][1] < self.pontos[18][1] and self.pontos[4][0] < self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1]: #dedao e mindinho
                            gesto = "Down"
                        if self.pontos[4][0] > self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #mao fechada
                            gesto = "Fechada"
                        if self.pontos[4][0] < self.pontos[3][0] and self.pontos[8][1] < self.pontos[6][1] and self.pontos[12][1] < self.pontos[10][1] and self.pontos[16][1] < self.pontos[14][1] and self.pontos[20][1] < self.pontos[18][1]: #mao aberta
                            gesto = "Esquerda"
                    else:
                        # Lógica para detecção de gestos da mão direita
                        if self.pontos[20][1] < self.pontos[18][1] and self.pontos[4][0] < self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1]: # so o mindinho
                            gesto = "Right" #mindinho
                        if self.pontos[4][0] > self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #dedao
                            gesto = "Left" #dedao
                        if self.pontos[8][1] < self.pontos[6][1] and self.pontos[4][0] < self.pontos[3][0] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #indicador
                            gesto = "Up" #indicador
                        if self.pontos[20][1] < self.pontos[18][1] and self.pontos[4][0] > self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1]: #dedao e mindinho
                            gesto = "Down"
                        if self.pontos[4][0] < self.pontos[3][0] and self.pontos[8][1] > self.pontos[6][1] and self.pontos[12][1] > self.pontos[10][1] and self.pontos[16][1] > self.pontos[14][1] and self.pontos[20][1] > self.pontos[18][1]: #mao fechada
                            gesto = "Fechada"
                        if self.pontos[4][0] > self.pontos[0][0] and self.pontos[8][1] < self.pontos[6][1] and self.pontos[12][1] < self.pontos[10][1] and self.pontos[16][1] < self.pontos[14][1] and self.pontos[20][1] < self.pontos[18][1]: #mao aberta
                            gesto = "Direita"

        return gesto

def main():
    captura = cv2.VideoCapture(0)
    Detector_maos = Detector()
    #Automacao_pyautogui = Automacao()

    # Solicita ao usuário que escolha a mão usando a interface gráfica
    app = QApplication(sys.argv)
    window = SelecionaMao()
    window.setWindowTitle("Seleção da Mão")
    window.show()
    app.exec_()

    # Atribui o valor de mao_usada da instância de SelecionaMao para o Detector
    Detector_maos.mao_usada = window.mao_usada

    print(f"Mão escolhida: {Detector_maos.mao_usada}")

    while True:
        _, img = captura.read()

        if not _:
            break

        gestos = Detector_maos.encontrar_maos(img)
        #Automacao_pyautogui.mover_cursor(gestos)  # Chama a função para mover o cursor

        cv2.imshow('Imagem', gestos)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    captura.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()