from PyQt5.QtWidgets import QFrame, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QMessageBox, QWidget, QTextEdit, QApplication,QScrollArea,QCheckBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from clases.AnalisisExploratorio import AnalisisExploratorio
# from clases.Prediccion import prediccion

import pandas as pd

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('./vistas/index.ui', self)
        
        self.variables = {'predictora': None, 'independiente': []}
        self.df=[]
        self.llaveCheck=0
        
         # Crear un layout vertical para el frame frSeleccionar
        self.layoutSeleccionarCheckboxes = QVBoxLayout()
        
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
        
        
        self.btnCargarArchivo = self.findChild(QPushButton, 'btnCargarArchivo') 
        self.btnCargarArchivo.setVisible(False) 
        
        #Barra Lateral
        self.btnFilasColumnas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageFilasColumnas))
        self.btnSeleccionar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageSeleccionar))
        self.btnResultado.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageResultado))
        self.btnTablero.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageTablero))
    
        self.btnPrediccion.clicked.connect(self.prediccion)   
        
        self.btnSeleccionarIndependientes = self.findChild(QPushButton, 'btnSeleccionarIndependientes') 
        self.btnSeleccionarPredictora = self.findChild(QPushButton, 'btnSeleccionarPredictora') 
        self.btnSeleccionarIndependientes.setVisible(True)
        self.btnSeleccionarPredictora.setVisible(True)
        
        self.btnSeleccionarChecks = self.findChild(QPushButton, 'btnSeleccionarChecks') 
        self.btnSeleccionarChecks.setVisible(False)
        
        self.frCheckboxes = self.findChild(QFrame, 'frCheckboxes') 
        self.frCheckboxes.setVisible(False)
        
        self.frSeleccionar = self.findChild(QFrame, 'frSeleccionar') 
        self.frSeleccionar.setVisible(False)
        
        self.lblCuatroFilas = self.findChild(QLabel, 'lblCuatroFilas')  
        self.lblCuatroFilas.setVisible(True) 
        
        self.lblResumenEstadistico = self.findChild(QLabel, 'lblResumenEstadistico')  
        self.lblResumenEstadistico.setVisible(True) 
        
        self.lblCamposNulos = self.findChild(QLabel, 'lblCamposNulos')  
        self.lblCamposNulos.setVisible(True) 
        
        self.lblPrediccion = self.findChild(QLabel, 'lblPrediccion')  
        self.lblPrediccion.setVisible(True) 
              
        
        
         

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
                self.df = pd.read_csv(archivo)
                
                # Crear un contenedor QVBoxLayout para las etiquetas
                etiquetasTiposDatos = QVBoxLayout()
                
                #  # Crear un layout vertical para el frame frSeleccionar
                # layoutSeleccionarCheckboxes = QVBoxLayout()

                 # Mostrar cantidad de filas y columnas
                self.lblNFilas.setText(f"Filas: {len(self.df)}")
                self.lblNColumnas.setText(f"Columnas: {len(self.df.columns)}")

                tipos_datos =[]
            # Mostrar nombre y tipo de datos de cada campo
                
                for columna, tipo in self.df.dtypes.items():
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
                
                self.mostrarBotonesSeleccionarVariables(df=self.df, layout=self.layoutSeleccionarCheckboxes)
              
                 
                
               
  
                # Ocultar el QLabel lblCargando y cerrar el QProgressDialog
                self.lblCargando.setVisible(False)
       

        # Habilitar toda la ventana
        self.setEnabled(True)

    def prediccion(self):
       self.stackedWidget.setCurrentWidget(self.pagePrediccion)    
    #    self.lblPrediccion.setText(prediccion.to_string())
    
    def enviaSeleccion(self,tipoVariable):      
        # Obtener los nombres de las columnas seleccionadas
        columnas_seleccionadas = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        
         # Verificar si se seleccionó exactamente una columna
        if tipoVariable=='predictora' and len(columnas_seleccionadas) != 1:
            # Mostrar mensaje de error
            QMessageBox.warning(self, "Error", "Por favor, selecciona solo una columna", QMessageBox.Ok)
            columnas_seleccionadas =[]
            tipoVariable=''
            return  # Salir de la función sin continuar
        # Desseleccionar todos los checkboxes
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

        if tipoVariable == 'predictora':          
            self.variables[tipoVariable]=columnas_seleccionadas[0]
        if tipoVariable == 'independiente':
            self.variables[tipoVariable]=columnas_seleccionadas
    
        
        if self.variables['predictora'] is not None and len(self.variables['independiente']) > 0:
        
            # Obtener los valores del diccionario
            valores = list(self.variables.values())

            # Aplanar la lista de valores si hay listas anidadas
            columnas = []
            for valor in valores:
                if isinstance(valor, list):
                    columnas.extend(valor)
                else:
                    columnas.append(valor)
                
            analisis=AnalisisExploratorio(self.df,columnas)
            
            self.lblCuatroFilas.setText(analisis.mostrar_primeras_filas())
            
            self.lblResumenEstadistico.setText(analisis.resumen_estadistico())
            
            self.lblCamposNulos.setText(analisis.valores_nulos())
           
        
        self.frCheckboxes.setVisible(False)
        self.frSeleccionar.setVisible(True)
        self.btnSeleccionarChecks.setVisible(False)
        
   
        
    def mostrarCheck(self,df,layout,tipoVariable):     
                self.frSeleccionar.setVisible(False)
                self.frCheckboxes.setVisible(True)
                              
                if self.llaveCheck==0:        
                            
                    #selecionar para la prediccion   
                    self.checkboxes = []             
                    for column in df.columns:
                        checkbox = QCheckBox(column)
                        self.checkboxes.append(checkbox)
                        layout.addWidget(checkbox)                 
                    
                    # Crear un widget que contendrá el layout
                    widget_seleccionar = QWidget()
                    widget_seleccionar.setLayout(layout)
                    
                    # Crear un área de desplazamiento y establecer el widget como contenido
                    scroll_area = QScrollArea()
                    scroll_area.setWidgetResizable(True)
                    scroll_area.setWidget(widget_seleccionar)

                    # Agregar el widget al frame frSeleccionar
                    self.frCheckboxes.setLayout(QVBoxLayout())
                    self.frCheckboxes.layout().addWidget(scroll_area)
                    
                    self.llaveCheck=self.llaveCheck+1
                 # Desconectar y conectar la señal del botón de selección de manera segura
                self.desconectar_senal(self.btnSeleccionarChecks)
                # Verifica cuántos checkboxes están seleccionados
                checked_count = sum(1 for checkbox in self.checkboxes if checkbox.isChecked())
                
                self.btnSeleccionarChecks.setVisible(True)
                
                self.btnSeleccionarChecks.clicked.connect(lambda: self.enviaSeleccion(tipoVariable=tipoVariable))   

                
                # Haz visible el botón si más de un checkbox está seleccionado, de lo contrario ocúltalo
                # if checked_count > 1:
                #     self.btnSeleccionarChecks.setVisible(True)
                # else:
                #     self.btnSeleccionarChecks.setVisible(False)
                
    def mostrarBotonesSeleccionarVariables(self,df,layout):
     
        self.frSeleccionar.setVisible(True)       
        
        self.desconectar_senal(self.btnSeleccionarIndependientes)
        
                 
        self.btnSeleccionarIndependientes.clicked.connect(lambda: self.mostrarCheck(df=df, layout=layout,tipoVariable='independiente'))   
        # self.desconectar_senal(self.btnSeleccionarIndependientes)
        
        self.btnSeleccionarPredictora.clicked.connect(lambda: self.mostrarCheck(df=df, layout=layout,tipoVariable='predictora'))  
 # Función para desconectar todas las conexiones del botón
    def desconectar_senal(self, boton):
        try:
            boton.clicked.disconnect()
        except TypeError:
            pass  # Ignorar el error si no había ninguna conexión previa

   