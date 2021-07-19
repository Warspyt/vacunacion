""" Se importa la libreria datatime para el manejo,
    transformacion y extraccion de las de las fechas"""
from datetime import datetime
from datetime import date

"""Clase para la creacion de objetos dato, para hacerles
    las validaciones pertinentes reutilizando codigo"""
class Dato:
    def __init__(self, Variable):
        self.variable = Variable

    def TipoDatoAlpha(self):
        if self.variable.isalpha():
            alpha = True
        else:
            alpha = False
        return alpha
    
    def TipoDatoNum(self):
        if self.variable.isdigit():
            num = True
        else:
            num = False
        return num
    
    def longitud(self, lenght):
        if len(self.variable) <= lenght:
            long = True
        else:
            long = False
        return long
    
    def rango(self, tope):
        if 1 <= int(self.variable) <= tope:
            dentro = True
        else:
            dentro = False
        return dentro
    
    def dia(self):
        if self.variable.isdigit() and 0 < int(self.variable) < 32:
            dia = True
            self.variable = self.variable.rjust(2, "0")
        else:
            dia = False
        return dia
    
    def mes(self):
        if self.variable.isdigit() and 0 < int(self.variable) < 13:
            mes = True
            self.variable = self.variable.rjust(2, "0")
        else:
            mes = False
        return mes

    def anio(self, inicio, fin):
        if self.variable.isdigit() and len(self.variable) == 4 and inicio < int(self.variable) < fin:
            ano = True
        else:
            ano = False
        return ano
    
    def hora(self):
        if self.variable.isdigit() and 0 < int(self.variable) < 25:
            hora = True
            self.variable = self.variable.rjust(2)
        else:
            hora = False
        return hora

    def minuto(self):
        if self.variable.isdigit() and 0 <= int(self.variable) < 60:
            minuto = True
            self.variable = self.variable.rjust(2)
        else:
            minuto = False
        return minuto

    def fecha(self, indicador): # valdiar con un < (menor que) o un >(mayor que)
        factual = datetime.now().strftime("%Y/%m/%d")
        if indicador == "<":
            if self.variable < factual:
                fecha = True
            else:
                fecha = False
        elif indicador == "<=":
            if self.variable <= factual:
                fecha = True
            else:
                fecha = False
        elif indicador == ">":
            if self.variable > factual:
                fecha = True
            else:
                fecha = False
        elif indicador == ">=":
            if self.variable >= factual:
                fecha = True
            else:
                fecha = False
        return fecha

    def existir(self, contenedor):
        if self.variable in contenedor:
            existe = True
        else:
            existe = False
        return existe


        
