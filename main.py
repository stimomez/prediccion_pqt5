import sys
from PyQt5.QtWidgets import QApplication
from clases.VentanaPrincipal import VentanaPrincipal

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
