import random
import iocomponents
import Configs as C
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, MediumMotor, SpeedPercent
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, ColorSensor
import ev3dev2.fonts as fonts
import ev3dev2.display as display


#configurações do tabuleiro, ataques, tipos de atacante (coisas que usam sensores, motores,..)
distanciaSlots = 360
sound = Sound()

def goToSlot(slot):
    motorAndamento = LargeMotor(iocomponents.OAndamento)
    motorAndamento.on_to_position(SpeedPercent(15), (slot +1)  * distanciaSlots) #volta à posicao 0

#ataque toque
def toqueAnim():

    #vai buscar o sensor e coloca me modo de toque
    sensorToque = TouchSensor(iocomponents.IToque)
    sensorToque.mode = 'TOUCH'
    
    #vai buscar o motor de toque
    motorToque = LargeMotor(iocomponents.OToque)

    #reseta o motor colocando todos os seus valores a 0. desta forma a posicao em que se encontra é 0
    motorToque.reset()
    #roda até à posicao 180 
    motorToque.on_to_position(SpeedPercent(20), 180)

    #enquanto está a rodar
    while(motorToque.is_running):
        #se o sensor de toque for premido
        if sensorToque.is_pressed:
            #para o motor e sai do while com o break
            motorToque.stop()
            break

    #coloca o motor de volta na posicao 0
    motorToque.on_to_position(SpeedPercent(-20), 0)

#ataque grua
def gruaAnim():
    #vai buscar o motor da grua
    motorGrua = MediumMotor(iocomponents.OGrua)
    #reseta o motor colocando todos os seus valores a 0. desta forma a posicao em que se encontra é 0
    motorGrua.reset()

    #vai até à posicao 3000 (corda esticada) e volta para a posicao 0
    motorGrua.on_to_position(SpeedPercent(100), 3000)
    motorGrua.on_to_position(SpeedPercent(-100), 0)

#ataque som, corre o ficheiro de som 'laser.wav'
def somAnim():
    sound.play_file('./laser.wav')

#apenas virtualmente
#devolve onde ficarão cada atacante na forma de list, indice 0 -> slot 0, indice 1 -> slot 1, etc. Cada elemento será um objeto do seu tipo(Tanque, Artilharia ou Infantaria)
def definirAtacantesERondas():

    atacantes = []
    
    while (len(atacantes) != 6): #Enquanto a lista de atacantes não está preenchida por 6 atacantes

        # if(sum([1 for x in atacantes if isinstance(x, Tanque)])== 3): dado1 = random.randint(3,6)
        # else: 
        dado1 = random.randint(1,6) #escolhe atacante

        if (dado1 <= 2): atacante = C.Tanque()
        elif (dado1 <= 4): atacante = C.Artilharia()
        else: atacante = C.Infantaria()
        
        dado2 = random.randint(1,6) #escolhe ronda

        atacante.ronda = int(dado2)

        atacante.slot = int(len(atacantes)+1) 

        atacantes.append(atacante)
        
    return atacantes


def lerSlots(atacantes, slots, ronda):

    motorAndamento = LargeMotor(iocomponents.OAndamento)
    motorAndamento.reset() #reset para o x em que está for 0
    slot = -1
    nova_posicao = motorAndamento.position
    while(slot < 5):
        nova_posicao += distanciaSlots
        slot += 1
        motorAndamento.on_to_position(SpeedPercent(15), nova_posicao)

        #le qual o atacante
        atacante = tipoAtacante()

        #se tem um atacante no slot e ainda nao esta na list slots
        print(slot)
        if(slots[slot] == None):
            atacantes[slot]= None
            if(atacante):
                atacante.ronda = ronda
                atacante.slot = slot 
                atacantes[slot]= atacante
    
    return atacantes


#Verifica que tipo de oponente está no slot através das cores
def tipoAtacante():
    #vai buscar o sensor de cor
    sensorCor = ColorSensor(iocomponents.ICor)
    print(sensorCor.color_name)
    if(sensorCor.color == 5):   #se for a cor vermelha
        tipoAtacante = C.Infantaria()
        sound.speak("Infantry")
    elif(sensorCor.color == 2): #azul
        tipoAtacante = C.Artilharia()
        sound.speak("Artillery")
    elif(sensorCor.color == 3): #verde
        tipoAtacante = C.Tanque()
        sound.speak("Tank")
    else: 
        return #se for qualquer outra cor devolve nulo
    return tipoAtacante     #devolve a classe de atacante
