#
# Programación Sensor de Distancia usando Ultrasonido
# JBF - 06-06-2019
#

# Incluir funciones de tiempo
import time 
# Manejo de la interrupcion de teclado
from subprocess import call
import RPi.GPIO as GPIO
# Constantes a utilizar
import ConstUltrasonic01 

# Se utilizar la numeracion de los pines de la placa
GPIO.setmode(GPIO.BOARD)
 
#Hay que configurar ambos pines del HC-SR04
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
# Función que calcula la distancia
def detectarObstaculo():
 
	# Se dispara un sonido.
	sendSound()
	# Se inicia el conteo del tiempo cuando el pin ECHO se encienda
   while GPIO.input(ECHO) == 0:
      start = time.time()
 
   while GPIO.input(ECHO) == 1:
      end = time.time()
 
   #La duracion del pulso del pin ECHO sera la diferencia entre
   #el tiempo de inicio y el final
   duracion = end-start
 
   #Este tiempo viene dado en segundos. Si lo pasamos
   #a microsegundos, podemos aplicar directamente las formulas
   #de la documentacion
   duracion = duracion*10**6
   medida = duracion/58 #hay que dividir por la constante que pone en la documentacion, nos dara la distancia en cm
 
   print "%.2f" %medida #por ultimo, vamos a mostrar el resultado por pantalla

# Esta función se encarga de disparar un sonido
def sendSound():
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
 
#Bucle principal del programa, lee el sensor. Se sale con CTRL+C
while True:
   try:
      detectarObstaculo()
   except KeyboardInterrupt:
      break
 
#por ultimo hay que restablecer los pines GPIO
print "Limpiando..."
GPIO.cleanup()
print "Acabado."