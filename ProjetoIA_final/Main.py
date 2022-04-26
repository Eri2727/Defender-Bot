#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sound import Sound
from Configs import *

from Heuristica import realizarAtaques, realizarAtaquesNovaHeuristica

from lib import definirAtacantesERondas,lerSlots
import iocomponents

sound = Sound()
sound.speak("Play!")

#função usada para correr o simulador (descomentar a def, os atacantes, returns e codigo a partir do numJogosGanhos quando necessário) -> Simulador
# def funcao():
ronda = 0

nrInimigosQueApareceram = 0

slots = [None, None, None, None, None, None]

defenderBot = DefBot()

# jogo = jogo()

# atacantes = definirAtacantesERondas() 
atacantes = [None, None, None, None, None, None]

# atac = Infantaria()
# atac.ronda = 2
# atac.slot = 1
# atacantes.append(atac)

# atac = Tanque()
# atac.ronda = 5
# atac.slot = 2
# atacantes.append(atac)

# atac = Tanque()
# atac.ronda = 4
# atac.slot = 3
# atacantes.append(atac)

# atac = Tanque()
# atac.ronda = 4
# atac.slot = 4
# atacantes.append(atac)

# atac = Infantaria()
# atac.ronda = 3
# atac.slot = 5
# atacantes.append(atac)

# atac = Tanque()
# atac.ronda = 1
# atac.slot = 6
# atacantes.append(atac)

while ronda < 7:

    ronda = ronda + 1
    input("Prima ENTER para iniciar a ronda " + str(ronda) + "\n")
    print(slots)
    atacantes = lerSlots(atacantes, slots, ronda)
    print(atacantes)
    
    inimigoApareceuRonda = False
    
    print("---------------------------------------- RONDA " + str(ronda) + " ----------------------------------------\n")

    if (defenderBot.energia == 0.0): print("O Defender-Bot nao tem qualquer energia pelo que a mesma nao foi restaurada...\n")
    
    elif (defenderBot.energia != defenderBot.energiaMax):

        defenderBot.energia = defenderBot.energia + defenderBot.energia * 0.5

        if (defenderBot.energia > defenderBot.energiaMax): defenderBot.energia = defenderBot.energiaMax
        
        print("A energia do Defender-Bot foi restaurada e agora tem " + str(defenderBot.energia) + "\n")

    for i in range (len(atacantes)):
        if(atacantes[i]!= None):
            atacante = atacantes[i]
            

            if (atacante.ronda == ronda):

                inimigoApareceuRonda = True

                slots[atacante.slot ] = atacante 

                print("Um inimigo do tipo " + type(atacante).__name__ + " foi posicionado no slot " + str(atacante.slot +1))

                nrInimigosQueApareceram = nrInimigosQueApareceram + 1

    if (inimigoApareceuRonda): print("*** Tabuleiro neste momento: ", str(slots).replace("None", "Vazio"), "***\n")

    elif (nrInimigosQueApareceram != 6): print("Nenhum inimigo apareceu nesta ronda... Falta(m) aparecer " + str(6 - nrInimigosQueApareceram) + " inimigo(s)\n")


    for i in range (len(atacantes)):
        if(atacantes[i]!= None):
            atacante = atacantes[i]

            # Se o atacante está nos slots, ainda tem ataques e se o atacante nao se posicionou nesta ronda => ataca o defenderBot
            if (slots.__contains__(atacante) and atacante.n_ataques > 0 and ronda >= atacante.ronda + 1): 
                
                atacante.ataque(defenderBot)

                print("Um inimigo do tipo " + type(atacante).__name__ + " (slot " + str(atacante.slot +1) + ") atacou o Defender-Bot [sobra(m) " + str(atacante.n_ataques) + " ataque(s) de um total de " + str(atacante.max_n_ataques) + "], retirando-lhe um total de " + str(atacante.impacto()) + " pontos de vida\n")
                sound.speak(str(defenderBot.pontos_vida) + "life points")
                if (defenderBot.pontos_vida > 0): 
                    print("O Defender-Bot tem agora " + str(defenderBot.pontos_vida) + " pontos de vida \n")
                else: 
                    
                    print("O Defender-Bot morreu :(\n")
                    sound.speak("oh no, the game, its broken")
                    sound.play_file('./goodbye.wav')
                    print("----------------------------------- O JOGO TERMINOU... -----------------------------------\n")
                    exit() #comentar os exit's quando se corre o servidor
                    # return 0


    #
    
    #É AQUI QUE O DEFENDER-BOT VAI ATACAR
    if (ronda != 7): 

        realizarAtaquesNovaHeuristica(slots, defenderBot, ronda, nrInimigosQueApareceram)
    #

    somaInimigosSemAtaques = 0

    semAtaques = True

    for i in range (len(slots)):

        atacante = slots[i]

        if (isinstance(atacante, Inimigo)):

            if (atacante.n_ataques != 0): semAtaques = False

    motorAndamento = LargeMotor(iocomponents.OAndamento)
    motorAndamento.on_to_position(SpeedPercent(15), 0) #volta à posicao 0

    # Se já apareceram 6 inimigos E todos os slots estão vazios OU Se já apareceram 6 inimigos e nenhum tem ataques 
    if (nrInimigosQueApareceram == 6 and sum([1 for x in slots if not isinstance(x, Inimigo)]) == 6 or nrInimigosQueApareceram == 6 and semAtaques): 
        print("O Defender-Bot terminou com " + str(defenderBot.pontos_vida) + " pontos de vida \n")
        sound.speak("Look at me, i won")
        print("------------------------------------ O JOGO TERMINOU! ------------------------------------\n")
        exit() 
        # return 1

print("O Defender-Bot terminou com " + str(defenderBot.pontos_vida) + " pontos de vida \n")
sound.speak("Look at me, i won")
sound.play_file('./confirm.wav')
print("----------------------------------- O JOGO TERMINOU! -----------------------------------\n")
# return 1


# numJogosGanhos = 0
# numJogos = 500

# for x in range(numJogos):
#   numJogosGanhos = numJogosGanhos + funcao()

# print(100*numJogosGanhos/numJogos)