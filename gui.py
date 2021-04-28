import tkinter as tk
#importa libreria grafica y se le crea un alias tk
from tkinter import messagebox
#importa cuadro de mensaje emergente

def salir():
    answer=messagebox.askyesno("salir","Desea Salir?")

    #si se confirma que desea salir  se cierra la ventana
    if(answer):
        ventana.destroy()

ventana= tk.Tk()
ventana.title("Vacunacion Amaya")
ventana.geometry("400x300")



main_menu=tk.Menu(ventana)
mi_dropdown_menu=tk.Menu(main_menu,tearoff=0)

main_menu.add_cascade(label="Administrar Afiliados",menu=mi_dropdown_menu)

mi_dropdown_menu.add_command(label="Crear Afiliado")
mi_dropdown_menu.add_command(label="Actualizar Afiliado")
mi_dropdown_menu.add_command(label="Consultar Afiliado")
main_menu.add_command(label="Administrar Vacunas")
main_menu.add_command(label="Plan Vacunacion")
main_menu.add_command(label="Salir",command=salir)
ventana.config(menu=main_menu)
ventana.mainloop()