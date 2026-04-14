'''
Created on 6 abr 2026

Módulo para el uso de las imágenes a imprimir en la ventana.

@author: pedro
'''

import tkinter
from PIL import Image, ImageTk
import coordenadas

invertir = False

def calcular_relx(x, ancho):
    if invertir:
        return 1 - (x + ancho/2) / coordenadas.img_ancho
    else:
        return (x - ancho/2) / coordenadas.img_ancho

def calcular_rely(y, alto):
    if invertir:
        return 1 - (y + alto/2) / coordenadas.img_alto
    else:
        return (y - alto/2) / coordenadas.img_alto
    
    
def añadir_etiquetas(marco, lista_etiquetas):
    
    ancho = coordenadas.img_ancho
    alto = coordenadas.img_alto
    # Añadimos una etiqueta para la imagen del fondo.
    lista_etiquetas["fondo"] = tkinter.Label(marco, bg = "blue")
    lista_etiquetas["fondo"].place(x=1, y=1, relwidth=1, relheight=1)
    lista_etiquetas["H"] = {}
    for i in range(4):
        lista_etiquetas["H"][i] = tkinter.Label(marco, bg="red")
        lista_etiquetas["H"][i].place(
            relx=calcular_relx(coordenadas.areas_H[i]["x"], coordenadas.alto),
            rely=calcular_rely(coordenadas.areas_H[i]["y"], coordenadas.ancho_4),
            relwidth = coordenadas.alto / ancho,
            relheight = coordenadas.ancho_4 / alto)
    lista_etiquetas["V"] = {}
    for i in range(4):
        lista_etiquetas["V"][i] = tkinter.Label(marco, bg="yellow")
        lista_etiquetas["V"][i].place(
            relx=calcular_relx(coordenadas.areas_V[i]["x"], coordenadas.ancho_4),
            rely=calcular_rely(coordenadas.areas_V[i]["y"], coordenadas.alto),
            relwidth = coordenadas.ancho_4 / ancho,
            relheight = coordenadas.alto / alto)
    lista_etiquetas["R"] = {}
    for i in range(4):
        lista_etiquetas["R"][i] = tkinter.Label(marco, bg="yellow")
        lista_etiquetas["R"][i].place(
            relx=calcular_relx(coordenadas.areas_R[i]["x"], coordenadas.ancho_2),
            rely=calcular_rely(coordenadas.areas_R[i]["y"], coordenadas.alto),
            relwidth = coordenadas.ancho_2 / ancho,
            relheight = coordenadas.alto / alto)

    
def abrir_imagenes(lista_imagenes):
    
    # Abrimos la imagen del fondo.
    if invertir:
        lista_imagenes["fondo"] = Image.open("graficos/mapa1.png")
    else:
        lista_imagenes["fondo"] = Image.open("graficos/mapa0.png")
    # Abrimos los patrones en horizontal.
    lista_imagenes["H"][0] = Image.open("graficos/H0.png")
    lista_imagenes["H"][1] = Image.open("graficos/H1.png")
    lista_imagenes["H"][2] = Image.open("graficos/H2.png")
    lista_imagenes["H"][3] = Image.open("graficos/H3.png")
    lista_imagenes["H"][4] = Image.open("graficos/H4.png")
    lista_imagenes["H"][5] = Image.open("graficos/H5.png")
    lista_imagenes["H"][6] = Image.open("graficos/HN.png")
    
    # Abrimos los patrones en vertical.
    lista_imagenes["V"][0] = Image.open("graficos/V0.png")
    lista_imagenes["V"][1] = Image.open("graficos/V1.png")
    lista_imagenes["V"][2] = Image.open("graficos/V2.png")
    lista_imagenes["V"][3] = Image.open("graficos/V3.png")
    lista_imagenes["V"][4] = Image.open("graficos/V4.png")
    lista_imagenes["V"][5] = Image.open("graficos/V5.png")
    lista_imagenes["V"][6] = Image.open("graficos/VN.png")
    
    # Abrimos los patrones del refrigerador.
    lista_imagenes["R"][0] = Image.open("graficos/R0.png")
    lista_imagenes["R"][1] = Image.open("graficos/R1.png")
    lista_imagenes["R"][2] = Image.open("graficos/RN.png")
    
def escalar_imagen(imagen, escala):
    # Función para escalar una imagen.
    w = imagen.width
    h = imagen.height
    w = int(w * escala)
    h = int(h * escala)
    return imagen.resize((w, h), Image.NEAREST)

def redimensionar_imagenes(fondo, lista_imagenes, lista_escaladas, escala):
    # Redimensionar las imágenes originales para que encagen en la ventana.
    for i in range(7):
        lista_escaladas["H"][i] = ImageTk.PhotoImage(escalar_imagen(lista_imagenes["H"][i], escala))
    for i in range(7):
        lista_escaladas["V"][i] = ImageTk.PhotoImage(escalar_imagen(lista_imagenes["V"][i], escala))
    for i in range(3):
        lista_escaladas["R"][i] = ImageTk.PhotoImage(escalar_imagen(lista_imagenes["R"][i], escala))
    lista_escaladas["fondo"] = ImageTk.PhotoImage(escalar_imagen(lista_imagenes["fondo"], escala))
    fondo.config(image=lista_escaladas["fondo"])
        
def mostrar_imagenes(lista_escaladas, lista_etiquetas, sorteo):
    for i in range(4):
        lista_etiquetas["H"][i].config(image=lista_escaladas["H"][sorteo["H4"][i]])
    for i in range(4):
        lista_etiquetas["V"][i].config(image=lista_escaladas["V"][sorteo["V4"][i]])
    for i in range(4):
        lista_etiquetas["R"][i].config(image=lista_escaladas["R"][sorteo["R2"][i]])
    
