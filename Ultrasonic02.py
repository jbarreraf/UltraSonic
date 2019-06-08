#-----------------------------------------------------------------------------------------------
# Programación Sensor de Distancia usando Ultrasonido
# JBF - 06-06-2019: Primera versión, sin conectar aún a RaspBerry
# JBF - 07-06-2019: Conectado a RaspBerry, se agregó una ventana gráfica para mostrar distancia.
#
#-----------------------------------------------------------------------------------------------

# Biblioteca de funciones de tiempo
import time 
# Manejo de la interrupcion de teclado
from subprocess import call
import RPi.GPIO as GPIO
# Biblioteca gráfica.
import tkinter as tk
# Constantes a utilizar
from ConstUltrasonic01 import *

# Constantes a utilizar en el programa
#TRIGGER = 11
#ECHO = 13

#MICRO_SECONDS_2 = 0.00002
#MICRO_SECONDS_10 = 0.000010

ventana = tk.Tk()
ventana.focus()
ventana.title("Sensor de Distancia")
ventana.geometry("500x100")

lblDistancia = tk.Label(ventana, font=('verdana', 30, 'bold'), bg='green', fg='white', bd=2)
lblDistancia.pack(fill=tk.BOTH, expand=1)

#------------------------------------------------------------------------------------
# Funcion: iniciarGPIO
# Descripción: Inicializar la conexión GPIO de la RaspBerry
#------------------------------------------------------------------------------------
def iniciarGPIO():
    # Se utilizar la numeracion de los pines de la placa
    GPIO.setmode(GPIO.BOARD)
    # Se apagan las alertas
    GPIO.setwarnings(False)
    #Hay que configurar ambos pines del HC-SR04
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
#------------------------------------------------------------------------------------
# Funcion: detectarObjeto
# Descripción: Usando el sensor de ultrasonido, detecta si hay un objeto en frente y
# a que distancia se encuentra
#------------------------------------------------------------------------------------
def detectarObjeto():
 
    # Se dispara un sonido.
   enviarSonido()
    # Se inicia el conteo del tiempo cuando el pin ECHO se encienda
   while GPIO.input(ECHO) == 0:
      start = time.time()
 
   while GPIO.input(ECHO) == 1:
      end = time.time()
 
   # La duración del pulso del pin ECHO sera la diferencia entre
   # el tiempo de inicio y el final
   # Este tiempo está en microsegundos
   duracion = end-start
 
   # La distancia corresponde a lo que tarda la recepción del pulso de ultrasonido, dividido
   # por la velocidad del sonido, que es un valor constante. Se divide por 2 ya que el tiempo
   # considera la ida y vuelta del pulso.
   medida = (duracion * VELOCIDAD_SONIDO) / 2

   if medida < DISTANCIA_MINIMA:
       lblDistancia.configure(bg='red', fg='yellow')
       print('\a')
   elif medida < DISTANCIA_MEDIA:
       lblDistancia.configure(bg='gold', fg='medium blue')
   else:
       lblDistancia.configure(bg='lime green', fg='white')

   # Se muestra la distancia en la ventana
   lblDistancia.configure(text='Distancia: %.0f cm' % medida)
   
   ventana.after(200, detectarObjeto)

#------------------------------------------------------------------------------------
# Funcion: enviarSonido
# Descripción: Disparar un pulso de ultrasonido
#------------------------------------------------------------------------------------
def enviarSonido():
    # Primero se apaga el pin TRIGGER
    GPIO.output(TRIGGER, False)
    # Se genera una pausa de 2 microsegundos
    time.sleep(MICRO_SECONDS_2)
    # Se vuelve a activar el pin TRIGGER
    GPIO.output(TRIGGER, True)
    # Se genera una espera de diez microsegundos
    time.sleep(MICRO_SECONDS_10)
    # Finalmente se vuelve a desactivar el pin TRIGGER
    GPIO.output(TRIGGER, False)
 
iniciarGPIO()
detectarObjeto()
ventana.mainloop()

#por ultimo hay que restablecer los pines GPIO
GPIO.cleanup()
