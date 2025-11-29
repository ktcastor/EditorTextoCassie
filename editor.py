#Importamos el módulo para trabajar con ventanas Qt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QListWidget, QMenuBar, QMenu, QTextEdit, QScrollArea, QColorDialog, QFontDialog,QFileDialog,QInputDialog
from PyQt6.QtGui import QFont, QAction,QTextImageFormat
from PyQt6.QtCore import Qt

#Clase para trabajar con imágenes
class Imagen:
    def __init__(self, ruta, ancho=300, alto=300):
        self.ruta = ruta
        self.ancho = ancho
        self.alto = alto

    def insertar(self, editor: QTextEdit):
        cursor = editor.textCursor()
        formato = QTextImageFormat()
        formato.setName(self.ruta)
        formato.setWidth(self.ancho)   # ancho fijo
        formato.setHeight(self.alto)   # alto fijo
        cursor.insertImage(formato)

class EditorPersonalizado(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Escribe aquí...")

    def insertarImagen(self, ruta, ancho=300, alto=300):
        """Inserta una imagen con tamaño fijo"""
        cursor = self.textCursor()
        formato = QTextImageFormat()
        formato.setName(ruta)
        formato.setWidth(ancho)
        formato.setHeight(alto)
        cursor.insertImage(formato)

    def contextMenuEvent(self, event):
        # Menú estándar de QTextEdit
        menu = self.createStandardContextMenu()

        # Acción personalizada
        resize_action = menu.addAction("Redimensionar imagen...")
        action = menu.exec(event.globalPos())

        if action == resize_action:
            cursor = self.textCursor()
            if cursor.charFormat().isImageFormat():
                formato = cursor.charFormat().toImageFormat()

                # Pedimos nuevo tamaño al usuario
                ancho, ok = QInputDialog.getInt(
                    self, "Nuevo ancho", "Ancho:", int(formato.width()), 50, 1000
                )
                if ok:
                    alto, ok = QInputDialog.getInt(
                        self, "Nuevo alto", "Alto:", int(formato.height()), 50, 1000
                    )
                    if ok:
                        formato.setWidth(ancho)
                        formato.setHeight(alto)
                        cursor.insertImage(formato)

class Pagina(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600,800)
        self.setStyleSheet("background-color: white; border: 2px solid #f8bbd0; border-radius: 10px;")
        self.components()

    def components(self):
        layout = QVBoxLayout(self)
        self.editor = EditorPersonalizado()
        self.editor.setPlaceholderText("Escribe aquí...")

        font_metrics = self.editor.fontMetrics()
        espacio = font_metrics.horizontalAdvance(" ")
        self.editor.setTabStopDistance(4 * espacio)

        layout.addWidget(self.editor)


#clase principal de la aplicación
class Writer:
    
    #Constructor de la clase
    def __init__(self):
        #variable que controla la aplicación
        app = QApplication([])

        self.currentFile = None 
    
        #Creamos la ventana principal
        self.window = QWidget()
        self.window.setStyleSheet("background-color: #fff0f5;font-family: 'Lucida Handwriting';ont-size: 20px;color: #4a148c;")

        #Definimos su personalización
        self.window.setWindowTitle("La libreta de Cassie")
        self.window.showMaximized()

        #Creamos una lista que almacenara que páginas tengo
        self.paginasCargadas = []

        #Carga los widgets a la aplicación
        self.components()
        
        #mostramos la ventana
        self.window.show()

        #ejecutamos la app
        app.exec()

    def components(self):
    
        #Creamos el layout
        layout = QVBoxLayout(self.window)
    
        #Creamos el menu
        menu = QMenuBar()
        menu.setStyleSheet("""
            QMenuBar {
                background-color: #f8bbd0;   /* rosa pastel */
                border: 1px solid #f48fb1;
                padding: 5px;

            QMenuBar::item {
                background-color: transparent;
                padding: 5px 15px;
                margin: 2px;

            QMenuBar::item:selected {
                background-color: #f48fb1;
                color: white;
                border-radius: 5px;

        """)
    
        #Opción del menú referente a funciones de archivo
        archivo = QMenu("Archivo",self.window)

        #Acciones del menú archivo
        archivo_nuevo = QAction("Nuevo", self.window)
        archivo_nuevo.triggered.connect(self.nuevoArchivo)
        archivo.addAction(archivo_nuevo)

        archivo_abrir = QAction("Abrir...", self.window)
        archivo_abrir.triggered.connect(self.abrirArchivo)
        archivo.addAction(archivo_abrir)

        archivo_guardar = QAction("Guardar", self.window)
        archivo_guardar.triggered.connect(self.guardarArchivo)
        archivo.addAction(archivo_guardar)

        archivo_guardar_como = QAction("Guardar como...", self.window)
        archivo_guardar_como.triggered.connect(self.guardarArchivoComo)
        archivo.addAction(archivo_guardar_como)


        #Opción del menú referente a funciones de las páginas
        paginas = QMenu("Páginas",self.window)

        #Acciones del menú archivo
        pagina_nueva = QAction("Nueva página",self.window)
        pagina_nueva.triggered.connect(lambda: self.agregarPagina())
        paginas.addAction(pagina_nueva)

        #Menú de edición
        edicion = QMenu("Edición",self.window)
        
        #Sub menú de edición de texto
        edicion_texto = QMenu("Texto",self.window)
        color_texto = QAction("Cambiar color del texto",self.window)
        color_texto.triggered.connect(lambda: self.cambiarColorTexto())
        edicion_texto.addAction(color_texto)

        fuente_texto = QAction("Cambiar fuente y tamaño", self.window)
        fuente_texto.triggered.connect(self.cambiarFuenteTexto)
        edicion_texto.addAction(fuente_texto)

        buscar_reemplazar = QAction("Buscar y reemplazar", self.window)
        buscar_reemplazar.triggered.connect(self.buscarYReemplazar)
        edicion_texto.addAction(buscar_reemplazar)
        
        
        edicion.addMenu(edicion_texto)

        #Sub menú de edición de imágenes
        edicion_imagen = QMenu("Imágenes",self.window)
        agregar_imagen = QAction("Agregar imágen",self.window)
        agregar_imagen.triggered.connect(lambda: self.agregarImagen())
        edicion_imagen.addAction(agregar_imagen)

        redimensionar_imagen = QAction("Redimensionar imagen", self.window)
        redimensionar_imagen.triggered.connect(lambda: self.redimensionarImagen())
        edicion_imagen.addAction(redimensionar_imagen)


        #fuente_texto = QAction("Cambiar fuente y tamaño", self.window)
        #fuente_texto.triggered.connect(self.cambiarFuenteTexto)
        #edicion_texto.addAction(fuente_texto)        
        
        edicion.addMenu(edicion_texto)
        edicion.addMenu(edicion_imagen)
            

        #Agregamos la opción de archivo al menú
        menu.addMenu(archivo)
        menu.addMenu(paginas)
        menu.addMenu(edicion)

        #Agregamos el menú al layout
        layout.setMenuBar(menu)

        #Creamos el scroll
        self.scroll  = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)
        
        
        #Contenedor de páginas
        self.contenedor = QWidget()
        self.layout_paginas = QVBoxLayout(self.contenedor)
        self.scroll.setWidget(self.contenedor)

        self.agregarPagina()
        
        
        #Agregamos el layout a la ventana
        self.window.setLayout(layout)


    def nuevoArchivo(self):
        # Limpia todas las páginas y resetea la ruta
        for pagina in self.paginasCargadas:
            pagina.setParent(None)
        self.paginasCargadas.clear()
        self.currentFile = None
        # Crear una nueva página vacía
        self.agregarPagina()


    def guardarArchivo(self):
        if hasattr(self, "currentFile") and self.currentFile:
            contenido = ""
            # Guardamos todas las páginas con marcadores
            for i, pagina in enumerate(self.paginasCargadas, start=1):
                contenido += f"<!--PAGINA {i}-->\n"
                contenido += pagina.editor.toHtml()
                contenido += "\n<!--FINPAGINA-->\n"
            with open(self.currentFile, "w", encoding="utf-8") as f:
                f.write(contenido)
        else:
            self.guardarArchivoComo()


    def guardarArchivoComo(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self.window,
            "Guardar archivo como",
            "",
            "Archivos HTML (*.html);;Todos los archivos (*)"
        )
        if ruta:
            contenido = ""
            for i, pagina in enumerate(self.paginasCargadas, start=1):
                contenido += f"<!--PAGINA {i}-->\n"
                contenido += pagina.editor.toHtml()
                contenido += "\n<!--FINPAGINA-->\n"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.currentFile = ruta


    def abrirArchivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.window,
            "Abrir archivo",
            "",
            "Archivos HTML (*.html);;Todos los archivos (*)"
        )
        if ruta:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Dividir por marcador de fin de página
            paginas_html = contenido.split("<!--FINPAGINA-->")

            # Limpiar páginas actuales
            for pagina in self.paginasCargadas:
                pagina.setParent(None)
            self.paginasCargadas.clear()

            # Crear nuevas páginas con el contenido
            for html in paginas_html:
                if html.strip():
                    pagina = Pagina()
                    pagina.editor.setHtml(html)
                    self.layout_paginas.addWidget(pagina, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.paginasCargadas.append(pagina)

            self.currentFile = ruta



    

    #función para agregar una nueva página
    def agregarPagina(self):
        pagina = Pagina()
        pagina.setStyleSheet("background-color: white;border: 2px solid #f8bbd0;border-radius: 10px;")
        self.layout_paginas.addWidget(pagina, alignment=Qt.AlignmentFlag.AlignCenter)
        self.paginasCargadas.append(pagina)

    #función para cambiar el color del texto
    def cambiarColorTexto(self):
        for pagina in self.paginasCargadas:
            if pagina.editor.hasFocus():
                color = QColorDialog.getColor()
                if color.isValid():
                    cursor = pagina.editor.textCursor()
                    fmt = cursor.charFormat()
                    fmt.setForeground(color)
                    cursor.mergeCharFormat(fmt)

                break



    #función para cambiar la fuente del texto
    def cambiarFuenteTexto(self):
        for pagina in self.paginasCargadas:
            if pagina.editor.hasFocus():
                font, ok = QFontDialog.getFont()
                if ok:
                    cursor = pagina.editor.textCursor()
                    fmt = cursor.charFormat()
                    fmt.setFont(font)
                    cursor.mergeCharFormat(fmt)

                break

    #Función para remplazar texto
    def buscarYReemplazar(self):
        # Pedimos el texto a buscar
        texto_buscar, ok = QInputDialog.getText(
            self.window, "Buscar texto", "Texto a buscar:"
        )
        if ok and texto_buscar:
            # Pedimos el texto nuevo
            texto_nuevo, ok2 = QInputDialog.getText(
                self.window, "Reemplazar por", "Texto nuevo:"
            )
            if ok2:
                # Recorremos todas las páginas y reemplazamos
                for pagina in self.paginasCargadas:
                    contenido = pagina.editor.toPlainText()
                    contenido = contenido.replace(texto_buscar, texto_nuevo)
                    pagina.editor.setPlainText(contenido)



    #Función para agregar imagenes a la página
    def agregarImagen(self):
        for pagina in self.paginasCargadas:
            if pagina.editor.hasFocus():
                ruta, _ = QFileDialog.getOpenFileName(
                    self.window,
                    "Seleccionar imagen",
                    "",
                    "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
                )
                if ruta:
                    pagina.editor.insertarImagen(ruta, ancho=300, alto=300)  # 👈 tamaño fijo
                break

    #Función para redimencionar imagen
    def redimensionarImagen(self):
        for pagina in self.paginasCargadas:
            if pagina.editor.hasFocus():
                cursor = pagina.editor.textCursor()
                if cursor.charFormat().isImageFormat():
                    formato = cursor.charFormat().toImageFormat()

                    # Pedimos nuevo tamaño
                    ancho, ok = QInputDialog.getInt(
                        self.window, "Nuevo ancho", "Ancho:", int(formato.width()), 50, 1000
                    )
                    if ok:
                        alto, ok = QInputDialog.getInt(
                            self.window, "Nuevo alto", "Alto:", int(formato.height()), 50, 1000
                        )
                        if ok:
                            formato.setWidth(ancho)
                            formato.setHeight(alto)
                            cursor.insertImage(formato)
                break




Writer()
