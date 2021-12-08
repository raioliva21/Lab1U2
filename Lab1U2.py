#!/usr/bin/env python
import json
# Se importa la librería Gobject Instrospection (gi)
import gi
# Selecciona que la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa Gtk
from gi.repository import Gtk

# importing libraries
import numpy as np
import pandas as pd

"""
La carga de los datos en una ventana con el widget correcto para la visualizacion de datos (grid)
"""

archivocsv = "drug200.csv"

def open_file(nombre_archivo = None):

    try:
        with open(nombre_archivo) as archivo:
            print("se abre archivo")
            datos_archivo = archivo.readlines()
            return datos_archivo
    except FileNotFoundError:
        print("Error, el archivo no fue encontrado")
        quit()



class Main():

    def __init__(self):
        # Creamos un objecto que hara la instrospection
        builder = Gtk.Builder()
        # Llamamos al archivo creado
        builder.add_from_file("/home/raimundoosf/Escritorio/laboratorio1U2.glade")
        # Asociamos a atributos cada uno de los elementos del glade (ID)
        self.ventana_principal = builder.get_object("ventana")
        # Seteamos un valor para el tamaño de la ventana
        self.ventana_principal.set_default_size(800, 600)
        self.ventana_principal.set_title("Visualizacion de datos")
        # Activamos
        self.ventana_principal.connect("destroy", Gtk.main_quit)

        self.boton_data_total = builder.get_object("visualizacion de data completa")
        self.boton_data_total.set_label("Visualizacion de data completa")
        self.boton_data_total.connect("clicked", self.click_cargar_data_total)

        self.boton_obtener_resumen = builder.get_object("obtener resumen")
        self.boton_obtener_resumen.set_label("Visualizacion de resumen de data")
        self.boton_obtener_resumen.connect("clicked", self.click_obtener_resumen)

        self.ventana_principal.show_all()
    
    def click_cargar_data_total(self, ntn=None):
        Dialogo_muestra_data()
    
    def click_obtener_resumen(self, ntn=None):
        Obtener_resumen()
        
    #def calcular_promedio_variables(self):

class Obtener_resumen():

    def __init__(self):

        print("ventana obtener resumen")
        # Creamos un objecto que hara la instrospection
        builder = Gtk.Builder()
        # Llamamos al archivo creado
        builder.add_from_file("/home/raimundoosf/Escritorio/laboratorio1U2.glade")
        # Asociamos a atributos cada uno de los elementos del glade (ID)
        self.ventana_resumen = builder.get_object("ventana_resumen_data")
        self.ventana_resumen.set_title("Resumen de data")
        data = open_file(archivocsv)
        datos = data[1:len(data)]

        almacen = []
        for item in datos:
            item = item.strip().split(",")
            almacen.append(item)

        NaN = np.nan
        dataframe = pd.DataFrame(almacen)
        dataframe = pd.DataFrame(almacen, columns = ["Edad", "Sexo", "Presion Arterial", "Colesterol", "Proporcion Na\K", "Droga"])

        print(dataframe)
        # obtiene edad promedio 
        edad_proemdio = int(np.asarray(dataframe['Edad'], dtype=np.int).mean())
        # Imprimimos la media de la columna 'Edad'
        print(edad_proemdio)

        #obtiene cantidad de pacientes de sexo femenino y masculino, respectivamente
        sexo_F = len(dataframe[dataframe["Sexo"] == 'F'])
        sexo_M = len(dataframe[dataframe["Sexo"] == 'M'])
        print(sexo_F)
        print(sexo_M)

        colesterol_elevado = len(dataframe[dataframe["Colesterol"] == 'HIGH'])
        print(colesterol_elevado)

        #obtiene cantidad de pacientes con BP Alto y BP Baja, respectivamente
        BP_HIGH = len(dataframe[dataframe["Presion Arterial"] == 'HIGH'])
        BP_LOW = len(dataframe[dataframe["Presion Arterial"] == 'LOW'])
        #Imprimimos cantidad de pacientes con BP Alto
        print(BP_HIGH)
        print(BP_LOW)

        nombre_drogas = ["drugA", "drugB", "drugC", "drugX", "DrugY", ]
        Droga = ['DrogA', 'DrogB', 'DrogC', 'DrogX', 'DrogY']

        for indice in range (0, len(nombre_drogas)):
            Droga[indice] = len(dataframe[dataframe["Droga"] == nombre_drogas[indice]])
        
        print(Droga)

        promedio_edad = builder.get_object("Promedio edad  pacientes")
        promedio_edad.set_label(f"Promedio de edad en pacientes: {edad_proemdio} anios.")
        sexo_pacientes = builder.get_object("cantidad pacientes masculinos/femeninos")
        sexo_pacientes.set_label(f"{sexo_F} pacientes de sexo femenino. {sexo_M} pacientes de sexo masculino.")
        colesterol_alto = builder.get_object("cantidad pacientes colesterol alt")
        colesterol_alto.set_label(f"{colesterol_elevado} pacientes con indice de colesterol elevado.")
        presion_Alta_Baja = builder.get_object("pacientes presion alta/baja")
        presion_Alta_Baja.set_label(f"{BP_HIGH} pacientes con presion alta. {BP_LOW} pacientes con presion baja.")
        cantidad_tipo_droga = builder.get_object("cantidad tipo droga")
        cantidad_tipo_droga.set_label(f"Droga Y es la de mayor consumo, suministrada a {Droga[4]} pacientes.")



        self.ventana_resumen.show_all()
        

class Dialogo_muestra_data():

    def __init__(self):

        print("ventana muestra data completa")
        # Creamos un objecto que hara la instrospection
        builder = Gtk.Builder()
        # Llamamos al archivo creado
        builder.add_from_file("/home/raimundoosf/Escritorio/laboratorio1U2.glade")
        # Asociamos a atributos cada uno de los elementos del glade (ID)
        self.ventana_dialogo = builder.get_object("Dialogo_muestra_data")
        self.ventana_dialogo.set_title("visualizacion de data completa")


        self.tree = builder.get_object("tree")
        self.modelo = Gtk.ListStore(str, str, str, str, str, str)
        self.tree.set_model(model=self.modelo)

        self.nombre_columnas = ("Edad", "Sexo", "Presion Arterial", "Coleserol", "Proporcion Na\K", "Droga")
        cell = Gtk.CellRendererText()
        for item in range(len(self.nombre_columnas)):
            #item = 2
            column = Gtk.TreeViewColumn(self.nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)

        self.load_data_from_json()

        self.ventana_dialogo.show_all()

    def load_data_from_json(self):
        # llamamos al metodo de abrir el archivo
        data = open_file(archivocsv)
        datos = data[1:len(data)]
            
        for item in datos:
            item = item.strip().split(",")
            self.modelo.append(item)
        
        """
        
        for item in datos:
            item = item.strip().split(",")
            diccionario = {"Edad": item[0],
                        "Sexo": item[1],
                        "Presion Artrial": item[2],
                        "Colesterol": item[3],
                        }
        
        """

        data = datos



if __name__ == "__main__":
    # Llama
    Main()
    Gtk.main()


