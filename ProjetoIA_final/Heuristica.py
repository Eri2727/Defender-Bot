from Configs import *

 
def verQualInfOuTanComMaisVida(slots : list):

    maiorVida = 0

    infOuTanComMaisVida = None
    
    for i in range (len(slots)):

        atacante = slots[i]

        if (atacante == None): continue

        if (isinstance(atacante, Artilharia)): continue

        else: 

            if atacante.pontos_vida > maiorVida: 

                infOuTanComMaisVida = atacante

                maiorVida = atacante.pontos_vida

    return infOuTanComMaisVida

def realizarAtaques(slots : list, defenderBot : DefBot):

    if (defenderBot.energia > 0):

        numeroAtacantesSlots = sum(x is not None for x in slots)

        numeroArtilhariasSlots = sum(x is Artilharia for x in slots)
        numeroInfantariasSlots = sum(x is Infantaria for x in slots)
        numeroTanquesSlots = sum(x is Tanque for x in slots)

        for i in range (len(slots)):

            atacante = slots[i]

            if (atacante == None): continue

            if (numeroArtilhariasSlots > 0): 
                
                defenderBot.atacar(atacante, i, 1, slots)
                continue

            if (numeroAtacantesSlots > 0 and numeroAtacantesSlots >= 4):

                if (defenderBot.energia <= 350):

                    if (numeroInfantariasSlots > 0 and numeroTanquesSlots > 0): 

                        at = verQualInfOuTanComMaisVida(slots)

                        if (at == atacante): 
                            
                            defenderBot.atacar(atacante, i, 1, slots)
                            continue

                    else: 
                        
                        defenderBot.atacar(atacante, i, 2, slots)
                        continue

                else: 
                    
                    defenderBot.atacar(atacante, i, 2, slots)
                    continue

            else:

                if (defenderBot.energia <= 350):

                    if (numeroInfantariasSlots > 0 and numeroTanquesSlots > 0): 

                        at = verQualInfOuTanComMaisVida(slots)

                        if (at == atacante): 
                            
                            defenderBot.atacar(atacante, i, 1, slots)
                            continue

                    else: 
                        
                        defenderBot.atacar(atacante, i, 2, slots)
                        continue

                else: 
                    
                    defenderBot.atacar(atacante, i, 2, slots)
                    continue

#NOVA HEURÍSTICA

def inimigosTemImpactoSuficiente(vidaMinima : int, slots : list, defenderBot : DefBot):

    vidaAtualDefBot = defenderBot.pontos_vida

    for i in range (len(slots)):

        atacante = slots[i]

        if (isinstance(atacante, Inimigo)): 
            
            if (atacante.n_ataques > 0): vidaAtualDefBot = vidaAtualDefBot - atacante.impacto()

    if (vidaAtualDefBot <= vidaMinima): return True

    else: return False

def aguentarMaximoTempoPossivel(slots : list, defenderBot : DefBot, ronda : int):

    inimigoSobrante = None
    impactoInimigoSobrante = 0
    numeroAtaquesInimSobrante = 0
    numeroRondasAFaltar = 7 - ronda

    for i in range (len(slots)):

        atacante = slots[i]

        if (isinstance(atacante, Inimigo)): 
            
            inimigoSobrante = atacante
            impactoInimigoSobrante = atacante.impacto()
            numeroAtaquesInimSobrante = atacante.n_ataques

            break

    if (inimigoSobrante != None):

        vezesQueVaiAtacar = numeroAtaquesInimSobrante if numeroRondasAFaltar >= numeroAtaquesInimSobrante else numeroRondasAFaltar

        danoTotalQueAguenta = vezesQueVaiAtacar * impactoInimigoSobrante

        vidaResultante = defenderBot.pontos_vida - danoTotalQueAguenta

        if(vidaResultante < 0):
            defenderBot.atacar(inimigoSobrante, escolherTipoAtaque(inimigoSobrante), slots)

        #codigo da primeira heuristica que já não é utilizado 
        # numeroRondasQueAguenta = (defenderBot.pontos_vida / impactoInimigoSobrante) 
        
        # if (numeroAtaquesInimSobrante >= numeroRondasQueAguenta or numeroRondasAFaltar > numeroRondasQueAguenta): 

        #     defenderBot.atacar(inimigoSobrante, escolherTipoAtaque(inimigoSobrante), slots)

def sortSecond(val):
        return val[1] 

def escolherTipoAtaque(atacante : Inimigo):
        if (atacante.pontos_vida) > 50: return 2

        else: return 1

def atacarInimigosComMaisImpacto(slots: list, defenderBot : DefBot, minimoEnergiaASobrar : float):

    atacantesESeuImpacto = []

    for i in range (len(slots)):

        atacante = slots[i]

        if (isinstance(atacante, Inimigo)): atacantesESeuImpacto.append([atacante, atacante.impacto(), atacante.n_ataques])

    if (len(atacantesESeuImpacto) > 0):

        atacantesESeuImpacto.sort(key = lambda x: (-x[1], -x[2]))#, reverse = True)

        indiceInimigoAAtacar = 0

        while (defenderBot.energia >= minimoEnergiaASobrar and indiceInimigoAAtacar != len(atacantesESeuImpacto)):

            inimigoAAtacar = atacantesESeuImpacto[indiceInimigoAAtacar][0]

            #print(minimoEnergiaASobrar, "é menor ou igual que ", defenderBot.energia-150,"?")

            if (inimigoAAtacar.pontos_vida > 50 and inimigoAAtacar.n_ataques > 0 and minimoEnergiaASobrar <= defenderBot.energia-150): 
                defenderBot.atacar(inimigoAAtacar, 2, slots)

            elif (minimoEnergiaASobrar <= defenderBot.energia-50 and inimigoAAtacar.n_ataques > 0): 
                defenderBot.atacar(inimigoAAtacar, 1, slots)

            indiceInimigoAAtacar += 1
            
            #codigo da primeira heuristica que já não é utilizado 
            """tipoAtaque = escolherTipoAtaque(inimigoAAtacar)

            if (tipoAtaque == 1): #Ataque com som

                if (defenderBot.energia < minimoEnergiaASobrar+50): parar = True
            
            elif (tipoAtaque == 2): #Ataque com toque

                if (defenderBot.energia < minimoEnergiaASobrar+100): parar = True

            defenderBot.atacar(inimigoAAtacar, escolherTipoAtaque(inimigoAAtacar), slots)
            
            if (inimigoAAtacar.pontos_vida <= 0): indiceInimigoAAtacar += 1

            if (indiceInimigoAAtacar == len(atacantesESeuImpacto)): parar = True"""


def atacarDeModoANaoMorrer(slots : list, defenderBot : DefBot):

    atacantesESeuImpacto = []

    somaImpactos = 0

    for i in range (len(slots)):

        atacante = slots[i]

        if (isinstance(atacante, Inimigo)): 
            
            atacantesESeuImpacto.append([atacante, 0 if atacante.n_ataques == 0 else atacante.impacto()])
            
            somaImpactos += 0 if atacante.n_ataques == 0 else atacante.impacto()

    vidaAtualDefBot = defenderBot.pontos_vida

    impactoTotalAtual = sum([x[1] for x in atacantesESeuImpacto])

    impactoARemover = impactoTotalAtual - vidaAtualDefBot

    #se for mesmo morrer
    if(impactoARemover >= 0):

        if(impactoARemover > 75 * len(atacantesESeuImpacto)):
            # Coloca os atacantes por ordem crescente do seu impacto
            atacantesESeuImpacto.sort(key = sortSecond, reverse = True)
        else:
            atacantesESeuImpacto.sort(key = sortSecond, reverse = False)

        for i in range (len(atacantesESeuImpacto)):

            inimigoAAtacar = atacantesESeuImpacto[i][0]
            
            antigoImpacto = int(inimigoAAtacar.impacto())

            # Ataca inimigo se este ainda tiver ataques
            if (isinstance(inimigoAAtacar, Inimigo) and inimigoAAtacar.n_ataques > 0): 
                if(inimigoAAtacar.pontos_vida >= 200 and defenderBot.energia >= 300):
                    defenderBot.atacar(inimigoAAtacar, 0, slots) # ataque grua se o de toque nao for suficiente
                else:
                    defenderBot.atacar(inimigoAAtacar, escolherTipoAtaque(inimigoAAtacar), slots)

            # Ve se o ataque foi suficiente para nao morrer na proxima (ultima) ronda
            if (vidaAtualDefBot - (somaImpactos - antigoImpacto + inimigoAAtacar.impacto()) <= 0): continue
            
            else: break



def realizarAtaquesNovaHeuristica(slots : list, defenderBot : DefBot, ronda : int, nrInimigosQueApareceram : int):
    
    numeroAtacantesSlots = sum([1 for x in slots if isinstance(x, Inimigo)])

    numeroArtilhariasSlots = sum([1 for x in slots if isinstance(x, Artilharia)])
    
    if (ronda == 6 or nrInimigosQueApareceram == 5 and numeroAtacantesSlots < 2): 
        
        # Retorna True se os inimigos tem Impacto suficiente para matar o Defender Bot
        if (inimigosTemImpactoSuficiente(0, slots, defenderBot)): 
            atacarDeModoANaoMorrer(slots, defenderBot)
        
        else: pass
    
    else:
    
        if (numeroArtilhariasSlots >= 1): 
        
            for i in range (len(slots)):

                atacante = slots[i]

                if (isinstance(atacante, Artilharia)): 
                    defenderBot.atacar(atacante, 1, slots) #ataque 1 = ataque com som

        numeroAtacantesSlots = sum([1 for x in slots if isinstance(x, Inimigo)])

        if (numeroAtacantesSlots == 1): 

            #se for o ultimo atacante recebe o maximo de dano sem morrer
            if (nrInimigosQueApareceram == 5): 
                aguentarMaximoTempoPossivel(slots, defenderBot, ronda)

            else: 
            
                if (defenderBot.energia >= 300): 
                    
                    for i in range (len(slots)):

                            atacante = slots[i]
                            
                            if (isinstance(atacante, Inimigo)): 
                                
                                defenderBot.atacar(atacante, 2, slots) #Ataque 2 = Ataque com toque

                                break #Porque este inimigo é o único no tabuleiro logo não faz sentido continuar a percorrer a lista do tabuleiro
                else: pass
        else:

            if (numeroAtacantesSlots >= 4): 

                if (defenderBot.energia >= 300): 
                    if (nrInimigosQueApareceram >= 4):
                        vida_minima = 50
                        energia_minima = 100
                    else:
                        vida_minima = 100
                        energia_minima = 50
                    if (inimigosTemImpactoSuficiente(vida_minima, slots, defenderBot)): 
                        atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima)
                    else:
                        if (nrInimigosQueApareceram >= 4):
                            energia_minima = 200
                        else: 
                            energia_minima = 250
                        atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima)

                else:

                    if (nrInimigosQueApareceram >= 4):
                        vida_minima = 50
                        energia_minima = 50
                    else:
                        vida_minima = 100
                        energia_minima = 100

                    if (inimigosTemImpactoSuficiente(vida_minima, slots, defenderBot)): 
                        atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima)

                    else: 
                        if (nrInimigosQueApareceram >= 4):
                            energia_minima = 200
                        else:
                            energia_minima = 100
                        atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima) 

            else:
                
                if (numeroAtacantesSlots > 0): #quando faltam 2 fica 200 em vez de 300

                    if (defenderBot.energia >= 300): 
                        if (nrInimigosQueApareceram >= 4):
                            energia_minima = 200
                        else:
                            energia_minima = 250
                        atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima) 

                    else:
                        if (nrInimigosQueApareceram >= 4):
                            energia_minima = 50
                        else:
                            energia_minima = 100
                        if (inimigosTemImpactoSuficiente(100, slots, defenderBot)): 
                            atacarInimigosComMaisImpacto(slots, defenderBot, energia_minima)

                        else: pass