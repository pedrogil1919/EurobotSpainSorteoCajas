'''
Created on 6 abr 2026

Programa para sortear la posición de los colores de las cajas en las zonas de
carga y refrigeradores para cada partido de Eurobot Spain 2026 "Winter is
coming".

@author: pedro
'''

from enum import Enum
import random
import time
import tkinter

import coordenadas
import imagenes


class Estado(Enum):
    # Estados de la aplicación
    CRONO_INICIO = 1  # Cronometro parado.
    CRONO_AVANCE = 2  # Cronómetro descendiendo
    SORTEO_INICIO = 4  # Cajas en gris
    SORTEO_ANIM = 5   # Animación del sorteo
    SORTEO_RESUL = 6  # Sorteo resuelto


ventana = None
tiempo_aminacion = 100  # mseg
tiempo_crono = 50  # mseg
crono_duracion = 180  # segundos
tiempo_inicio = 0
font = ("Liberation Sans", 300, "bold")


def teclado(evento):
    """ Función de atención a los eventos del teclado.

    """
    global estado
    global sorteo
    global tiempo_inicio
    # Implementación de la máquina de estados.
    if estado == Estado.CRONO_INICIO:
        if evento.char == 't':
            pass
        elif evento.char == ' ':
            estado = Estado.CRONO_AVANCE
        elif evento.char == 'p':
            altarnar_pantallas(True)
            estado = Estado.SORTEO_INICIO
    elif estado == Estado.CRONO_AVANCE:
        if evento.char == 't':
            estado = Estado.CRONO_INICIO
        elif evento.char == ' ':
            return
        elif evento.char == 'p':
            return

    elif estado == Estado.SORTEO_INICIO:
        if evento.char == 't':
            estado = Estado.CRONO_INICIO
            altarnar_pantallas(False)
        elif evento.char == ' ':
            estado = Estado.SORTEO_ANIM
        elif evento.char == 'p':
            pass
    elif estado == Estado.SORTEO_ANIM:
        if evento.char == 't':
            estado = Estado.CRONO_INICIO
            altarnar_pantallas(False)
        elif evento.char == ' ':
            estado = Estado.SORTEO_RESUL
        elif evento.char == 'p':
            estado = Estado.SORTEO_INICIO
    elif estado == Estado.SORTEO_RESUL:
        if evento.char == 't':
            estado = Estado.CRONO_INICIO
            altarnar_pantallas(False)
        elif evento.char == ' ':
            estado = Estado.SORTEO_ANIM
        elif evento.char == 'p':
            estado = Estado.SORTEO_INICIO

    if estado == Estado.SORTEO_INICIO:
        borrar_sorteo(sorteo)
    elif estado == Estado.SORTEO_ANIM:
        realizar_sorteo(sorteo)
        ventana.after(tiempo_aminacion, realizar_sorteo)
    elif estado == Estado.SORTEO_RESUL:
        realizar_sorteo(sorteo)
    elif estado == Estado.CRONO_INICIO:
        inicio_crono()
    elif estado == Estado.CRONO_AVANCE:
        tiempo_inicio = time.time()
        actualizar_crono()
        # print("iniciar crono: ", tiempo_inicio)
    elif estado == Estado.CRONO_FIN:
        pass


def convertir_tiempo(tiempo):
    segundos = tiempo % 60
    minutos = tiempo // 60
    return "%i:%02i" % (minutos, segundos)


def inicio_crono():
    global etiqueta_crono
    global tiempo_inicio
    tiempo = convertir_tiempo(crono_duracion)
    etiqueta_crono.config(text="%s" % tiempo)


def actualizar_crono():
    global etiqueta_crono
    global tiempo_inicio
    if estado != Estado.CRONO_AVANCE:
        return
    tiempo_actual = time.time()
    restante = int(crono_duracion - (tiempo_actual - tiempo_inicio))

    if restante < 0:
        restante = 0
    tiempo = convertir_tiempo(restante)
    etiqueta_crono.config(text="%s" % tiempo)
    ventana.after(tiempo_crono, actualizar_crono)


def iniciar_sorteo(sorteo):
    sorteo["H4"] = {
        0: 6,
        1: 6,
        2: 6,
        3: 6}
    sorteo["V4"] = {
        0: 6,
        1: 6,
        2: 6,
        3: 6}
    sorteo["R2"] = {
        0: 2,
        1: 2,
        2: 2,
        3: 2}


def borrar_sorteo(sorteo):
    global lista_escaladas
    global lista_etiquetas
    iniciar_sorteo(sorteo)
    imagenes.mostrar_imagenes(lista_escaladas, lista_etiquetas, sorteo)


def realizar_sorteo(evento=None):
    global lista_escaladas
    global lista_etiquetas
    global sorteo
    global estado

    if evento is None:
        if estado == Estado.SORTEO_ANIM:
            ventana.after(tiempo_aminacion, realizar_sorteo)
        else:
            return
    # Elegimos un valor entre 1 y 6^8*2*4
    # es decir:
    # 8 zonas de almacenaje, por 6 posibles combinaciones de colores
    # cada 1, por 4 refrigeradores por 2 combinaciones de colores cada una.
    valor = random.randint(1, 26873856)

    for i in range(4):
        sorteo["H4"][i] = valor % 6
        valor = valor // 6
    for i in range(4):
        sorteo["V4"][i] = valor % 6
        valor = valor // 6
    for i in range(4):
        sorteo["R2"][i] = valor % 2
        valor = valor // 2

    # if simetrico:

    imagenes.mostrar_imagenes(lista_escaladas, lista_etiquetas, sorteo)


def redimensionar(event):
    global ventana_ancho
    global ventana_alto
    global lista_imagenes
    global lista_escaladas
    global lista_etiquetas
    global sorteo

    nuevo_ancho = event.width
    nuevo_alto = event.height
    # NOTA: Al redimensionar el evento, en primer lugar salta el evento con
    # alto y ancho igual a 1. Eso no se puede evitar. Por lo tanto, tenemos que
    # ignorar estos eventos.
    if nuevo_ancho <= 1 or nuevo_alto <= 1:
        return

    # Detectamos si se ha cambiado las dimensiones de la ventana.
    if ventana_ancho == nuevo_ancho and ventana_alto == nuevo_alto:
        return

    # Actualizamos el nuevo ancho y alto de la ventana.
    ventana_ancho = nuevo_ancho
    ventana_alto = nuevo_alto

    # Calculamos la escala para las imágenes, teniendo en cuenta que debemos
    # conservar la relación de aspecto.
    escala_x = ventana_ancho / coordenadas.img_ancho
    escala_y = ventana_alto / coordenadas.img_alto
    # Elegimos la menor de las dos, para que no se salga de la ventana en la
    # dimensión menos reducida.
    escala = min((escala_x, escala_y))
    # Configuramos el marco al tamaño máximo para que ocupe toda la ventana sin
    # salirse.
    fondo_ancho = int(coordenadas.img_ancho * escala)
    fondo_alto = int(coordenadas.img_alto * escala)
    fondo_sorteo.config(width=fondo_ancho, height=fondo_alto)
    imagenes.redimensionar_imagenes(
        lista_etiquetas["fondo"], lista_imagenes, lista_escaladas, escala)
    imagenes.mostrar_imagenes(lista_escaladas, lista_etiquetas, sorteo)


def altarnar_pantallas(sorteo):
    if sorteo:
        fondo_sorteo.pack(expand=True)
        fondo_crono.pack_forget()
    else:
        fondo_sorteo.pack_forget()
        fondo_crono.pack(fill=tkinter.BOTH, expand=True)


###############################################################################
# Dimensinoes de la ventana. Lo empleamos para detectar si se han cambiado las
# dimensiones de la ventana principal.
ventana_ancho = 0
ventana_alto = 0
# Escala de las imágenes a imprimir. Nótese que en el módulo de coordanadas
# tenemos las coordenadas originales de todos los elementos.
escala = 1.0

estado = Estado.SORTEO_INICIO
# Listado de valores aleatorios para mostrar los patrones en cada zona.
sorteo = {}
iniciar_sorteo(sorteo)

tiempo_inicio = time.time()

# Ventana principal. Sobre esta ventana añadiremos un marco que será sobre el
# que se imprimirán la imagen del mapa y las etiquetas con los cólores de las
# cajas.
ventana = tkinter.Tk()
ventana.geometry("800x600")

# Creamos el marco sobre el que imprimir las imágenes.
fondo_aux = tkinter.Frame(ventana)
fondo_aux.pack(fill=tkinter.BOTH, expand=True)
fondo_sorteo = tkinter.Frame(fondo_aux, bg="green")
fondo_sorteo.pack(expand=True)
fondo_sorteo.pack_propagate(False)
fondo_crono = tkinter.Frame(fondo_aux)
fondo_crono.pack_propagate(False)
etiqueta_crono = tkinter.Label(fondo_crono, font=font)
etiqueta_crono.pack(expand=True)

###############################################################################

# Abrimos las imágenes en sus tamaños originales.
lista_imagenes = {
    "fondo": None,  # Imagen del fondo.
    "H": {},       # Patrones de zona carga en horizontal.
    "V": {},       # Patrones de zona carga en vertical.
    "R": {}}       # Patrones del refrigerador.
imagenes.abrir_imagenes(lista_imagenes)
# Lista de imágenes escaladas
lista_escaladas = {
    "fondo": None,  # Imagen del fondo.
    "H": {},       # Patrones de zona carga en horizontal.
    "V": {},       # Patrones de zona carga en vertical.
    "R": {}}       # Patrones del refrigerador.

lista_etiquetas = {}
imagenes.añadir_etiquetas(fondo_sorteo, lista_etiquetas)
###############################################################################
# Detectamos el redimensionamiento de la ventana principal, para calcular la
# escala de las imágenes a imprimir
fondo_aux.bind("<Configure>", redimensionar)
ventana.bind("<space>", teclado)
ventana.bind("p", teclado)
ventana.bind("t", teclado)
ventana.bind("<Escape>", exit)

ventana.mainloop()
