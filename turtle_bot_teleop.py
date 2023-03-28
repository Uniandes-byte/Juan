#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# IMPORTAR LAS LIBRERÍAS
#-------------------------------------------------------------------------------

from argparse import _VersionAction
from glob import glob
from tkinter.tix import TEXT
from turtle import end_fill
import rospy
import sys
import os.path
from pynput import keyboard
from geometry_msgs.msg import Vector3
from std_msgs.msg import String
from tkinter.filedialog import asksaveasfile
from tkinter import BOTTOM, Tk,Frame,Button,Label, mainloop,ttk

#-------------------------------------------------------------------------------
# INICIALIZA LAS VARIABLES
#-------------------------------------------------------------------------------

recorrido = [] # Se inicializa la variable "recorrido" en un vector vacío.

dataFromRos = Vector3() # Se declara el vector con las componentes de velocidad lineal x y velocidad angular y.

#-------------------------------------------------------------------------------
# MÉTODOS
#-------------------------------------------------------------------------------

# Presionado y No presionado.
def poseCallback(pose_message):
    global x
    global y, z, z
    x = pose_message.x
    y = pose_message.y
    z = pose_message.theta

def on_press(key): # Método cuando el usuario presiona una tecla.
        global movimiento
        if key == keyboard.Key.up: # Si se presiona la tecla de la flecha 'Arriba'.
            # Stop listener
            dataFromRos.x = abs(int(speed_lineal)) # Asignar valor de velocidad lineal a la componente x positiva.
            recorrido.append(1) # Se guarda un valor de 1 en el vector de recorrido.

        elif key == keyboard.Key.down: # Si se presiona la tecla de la flecha 'Abajo'.
            recorrido.append(2) # Se guarda un valor de 2 en el vector de recorrido.
            dataFromRos.x  = -abs(int(speed_lineal)) # Asignar valor de velocidad lineal a la componente x negativa.
       
        elif key == keyboard.Key.left: # Si se presiona la tecla de la flecha 'Izquierda'.
            recorrido.append(3) # Se guarda un valor de 3 en el vector de recorrido.
            dataFromRos.y = abs(int(speed_theta)) # Asignar valor de velocidad angular a la componente y positiva.
        
        elif key == keyboard.Key.right: # Si se presiona la tecla de la flecha 'Derecha'.
            recorrido.append(4) # Se guarda un valor de 4 en el vector de recorrido.
            dataFromRos.y = -abs(int(speed_theta)) # Asignar valor de velocidad angular a la componente y negativa.

        elif key == keyboard.Key.esc:  # Si se presiona la tecla ESC.
            print('Listo para guardar...')
            global save_btn
            global ventana
            ventana  = Tk() # Crea la interfaz.
            ventana.geometry('200x100') # Tamaño de la interfaz.
            ventana.wm_title('Guardar ruta')
            save_btn = ttk.Button(ventana, text = 'Click to save file ', command = lambda : SaveFile()) # Crea el botón de guardar archivo.
            save_btn.pack(side = BOTTOM, pady = 20,padx = 50)
            ventana.mainloop()

            sys.exit()

def SaveFile(): # Método para guardar el recorrido.

        data = [("Text files","*.txt")] # Guarda el archivo con el nombre dado por el usuario.

        file1 = asksaveasfile(filetypes =data, defaultextension = '.txt')
        file1.write(speed_lineal+"\n") # Escribe la velocidad lineal.
        file1.write(speed_theta+"\n") # EScribe la velocidad angular.

        for i in recorrido: # Escribe los valores de 1, 2, 3 y 4 en cada posición del recorrido, respectivamente.
                file1.write(str(i)+"\n")
        file1.close()
        ventana.destroy()
        
def move(key):
    global velocity_message
    global dataFromRos
    dataFromRos.x = 0 # Se inicializa el componente de velocidad lineal en 0.
    dataFromRos.y = 0 # Se inicializa el componente de velocidad angular en 0.
               
def main():
    global dataFromRos
    global velocity_message
    print('Corriendo...')
    rospy.init_node('turtle_bot_teleop') # Inicializa el nodo con el nombre turtle_bot_teleop.
    
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press,on_release=move) #Método que establece el método de presionar tecla y soltar tecla.
    listener.start() # Inicializa el hilo.
    loop_rate = rospy.Rate(10) # 10Hz.
    topico_velocidad ='locomotion_arduino' # Variable con el nombre del topico a usar (velocidad).
    velocity_publisher = rospy.Publisher(topico_velocidad,Vector3, queue_size = 10) # Crea un publicador hacia el topico /locomotion_arduino de tipo Vector3.

    while not rospy.is_shutdown():
        velocity_publisher.publish(dataFromRos) # Envía el vector al robot.
        print(dataFromRos) # Prueba de que manda.
        loop_rate.sleep()
        
if __name__ == "__main__":
	speed_lineal =input('Escriba una velocidad lineal en el rango [1, 70] (cm/s):')
	speed_theta = input('Escriba una velocidad angular en el rango [1, 180] (rad/s):')
	main()