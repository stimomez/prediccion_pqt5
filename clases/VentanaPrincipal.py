from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QTabWidget, QWidget, QTextEdit, QApplication,QScrollArea,QCheckBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import pandas as pd

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('./vistas/index.ui', self)
        
        # Deshabilitar la capacidad de maximizar
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
         # Lista para mantener referencias a los QCheckBox
        self.checkboxes = []

        # Deshabilitar la capacidad de cambiar el tamaño de la ventana
        self.setFixedSize(self.size())

        # Crear un botón para cargar archivos CSV
        self.botonCargar = QPushButton("Cargar Archivo CSV", self.frCargar)
        
        self.lblCargando = self.findChild(QLabel, 'lblCargando')  # Encontrar el QLabel lblCargando
        self.lblCargando.setVisible(False)  # Inicialmente ocultar el QLabel

        # Conectar el botón con el método para abrir el diálogo de archivos
        self.botonCargar.clicked.connect(self.abrir_dialogo_archivo)

        # Agregar el botón al layout del frame
        layout = QVBoxLayout(self.frCargar)
        layout.addWidget(self.botonCargar)
        self.frCargar.setLayout(layout)
        
        
        #Barra Lateral
        self.btnCargarArchivo = self.findChild(QPushButton, 'btnCargarArchivo') 
        self.btnCargarArchivo.setVisible(False) 
        
        self.btnFilasColumnas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageFilasColumnas))
        self.btnSeleccionar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageSeleccionar))
        self.btnResultado.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageResultado))
        self.btnTablero.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageTablero))
        self.btnPrediccion.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pagePrediccion))   
        
        

    def abrir_dialogo_archivo(self):          

        # Mostrar el QLabel lblCargando
        self.lblCargando.setVisible(True)
        self.lblCargando.setText("Cargando...")

        # Deshabilitar toda la ventana
        self.setEnabled(False)

         # Abrir el diálogo de archivos
        opciones = QFileDialog.Options()
        filtro = "Archivos CSV (*.csv);;Todos los archivos (*)"
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo CSV", "", filtro, options=opciones)
        
        if archivo:
         # Cargar el archivo CSV usando pandas
                df = pd.read_csv(archivo)
                
                # Crear un contenedor QVBoxLayout para las etiquetas
                etiquetasTiposDatos = QVBoxLayout()
                
                 # Crear un layout vertical para el frame frSeleccionar
                layout_seleccionar = QVBoxLayout()

                 # Mostrar cantidad de filas y columnas
                self.lblNFilas.setText(f"Filas: {len(df)}")
                self.lblNColumnas.setText(f"Columnas: {len(df.columns)}")

                tipos_datos =[]
            # Mostrar nombre y tipo de datos de cada campo
                
                for columna, tipo in df.dtypes.items():
                 tipos_datos.append({'columna': columna, 'tipo': str(tipo)})
                 
                for dato in tipos_datos:
                    etiqueta = QLabel(f"{dato['columna']} : {dato['tipo']}")
                    etiquetasTiposDatos.addWidget(etiqueta)
                
                # Crear un widget que contendrá el layout de las etiquetas
                widget_contenido = QWidget()
                widget_contenido.setLayout(etiquetasTiposDatos)

                # Crear un área de desplazamiento y establecer el widget como contenido
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)  # El área de desplazamiento se ajustará al tamaño del widget contenido
                scroll_area.setWidget(widget_contenido)

                # Establecer el área de desplazamiento como el contenido del frame
                self.frTiposDatos.setLayout(QVBoxLayout())
                self.frTiposDatos.layout().addWidget(scroll_area)
                
                #selecionar para la prediccion   
                self.checkboxes = []             
                for column in df.columns:
                    checkbox = QCheckBox(column)
                    self.checkboxes.append(checkbox)
                    layout_seleccionar.addWidget(checkbox)                 
                
                 # Crear un widget que contendrá el layout
                widget_seleccionar = QWidget()
                widget_seleccionar.setLayout(layout_seleccionar)
                
                # Crear un área de desplazamiento y establecer el widget como contenido
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setWidget(widget_seleccionar)

                # Agregar el widget al frame frSeleccionar
                self.frSeleccionar.setLayout(QVBoxLayout())
                self.frSeleccionar.layout().addWidget(scroll_area)
                
                
  
                # Ocultar el QLabel lblCargando y cerrar el QProgressDialog
                self.lblCargando.setVisible(False)
       

        # Habilitar toda la ventana
        self.setEnabled(True)

       
    def enviar_seleccion(self):
        # Obtener los nombres de las columnas seleccionadas
        columnas_seleccionadas = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        print("Columnas seleccionadas:", columnas_seleccionadas)
        # Aquí puedes realizar las acciones necesarias con las columnas seleccionadas
