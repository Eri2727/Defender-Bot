
#from asyncio.windows_events import streams#
import lib

# Variaveis 

energiaBot = 500
vidaBot = 750
danoGrua = 200
danoToque = 100
danoSom = 50
custoGrua = 300
custoToque = 150
custoSom = 50
curaPequena = 100
curaMedia = 200
curaGrande = 400
custoCuraPeq = 200
custoCuraMed = 300
custoCuraGran = 400
vidaTanque = 200
vidaArt = 50
vidaInf = 100
Ftanque = 200
FArt = 500
FInf = 100
AtaquesTanque = 2
AtaquesArt = 1
AtaquesInfant = 3



#implementação das classes 
class jogo:
    def __init__(self):
        self.slots = [None, None, None, None, None, None]

class Unidade: 

    def __init__(self,_max_health_points):
        self.max_vida = _max_health_points
        self.pontos_vida = _max_health_points
        self.posicao = 0
        return

    def __repr__(self):
        return self.__class__.__name__

class Inimigo(Unidade):


    def __init__(self,_max_health_points,_strength,_max_number_of_attacks):
        Unidade.__init__(self,
            _max_health_points)
        self.max_n_ataques = _max_number_of_attacks
        self.n_ataques = _max_number_of_attacks
        self.forca = _strength
        return
    
    def impacto(self):
        percentagem_vida = self.pontos_vida/self.max_vida
        impacto = int(percentagem_vida * self.forca)
        # if(self.n_ataques == 0): impacto = 0
        return impacto
    
    def ataque(self, alvo):
        alvo.pontos_vida = alvo.pontos_vida - self.impacto()
        self.n_ataques = self.n_ataques - 1

class Tanque(Inimigo):
    def __init__(self):
        Inimigo.__init__(self,
            vidaTanque ,
            Ftanque,
            AtaquesTanque)
        return

class Artilharia(Inimigo):
    def __init__(self):
        Inimigo.__init__(self,
            vidaArt,
            FArt,
            AtaquesArt)
        return

class Infantaria(Inimigo):
    def __init__(self):
        Inimigo.__init__(self,
            vidaInf,
            FInf,
            AtaquesInfant)
        return

class DefBot(Unidade):


    def __init__(self,):
        Unidade.__init__(self,
            vidaBot)
            
        self.energiaMax = energiaBot
        self.energia = self.energiaMax

        self.DanoGrua = danoGrua
        self.CustoGrua = custoGrua

        self.DanoSom = danoSom
        self.CustoSom = custoSom

        self.DanoToque = danoToque
        self.CustoToque = custoToque

        self.cura_grande = curaGrande
        self.cura_media = curaMedia
        self.cura_pequena = curaPequena

        self.custo_cura_pequena = custoCuraPeq
        self.custo_cura_media = custoCuraMed
        self.custo_cura_grande = custoCuraGran
        return

    def atacar(self, alvo : Inimigo, tipoAtaque : int, slots : list):

        msgAtaque = "O Defender-Bot atacou um inimigo do tipo " + type(alvo).__name__ + " (slot " + str(alvo.slot +1) + ")"

        ataqueBemSucedido = False

        lib.goToSlot(alvo.slot)

        if (tipoAtaque == 0):
            ataqueBemSucedido = self.ataque_grua(alvo)
            msgAtaque += " com um ataque com grua, retirando-lhe um total de " + str(self.DanoGrua) + " pontos de vida [sobram " + str(alvo.pontos_vida) + " de um total de " + str(alvo.max_vida) + "]"

        elif(tipoAtaque == 1):
            ataqueBemSucedido = self.ataque_som(alvo)
            msgAtaque += " com um ataque com som, retirando-lhe um total de " + str(self.DanoSom) + " pontos de vida [sobram " + str(alvo.pontos_vida) + " de um total de " + str(alvo.max_vida) + "]"

        elif (tipoAtaque == 2):
            ataqueBemSucedido = self.ataque_toque(alvo)
            msgAtaque += " com um ataque com toque, retirando-lhe um total de " + str(self.DanoToque) + " pontos de vida [sobram " + str(alvo.pontos_vida) + " de um total de " + str(alvo.max_vida) + "]"

        if (ataqueBemSucedido):

            print(msgAtaque)

            if (alvo.pontos_vida <= 0): 
                
                print("Um inimigo do tipo " + type(alvo).__name__ + " (slot " + str(alvo.slot +1) + ") morreu :)\n")
                
                slots[alvo.slot] = None

                print("*** Tabuleiro neste momento: ", str(slots).replace("None", "Vazio"), "***\n")

            print("O Defender-Bot ficou com ", self.energia, " de energia a sobrar\n")

    def ataque_grua(self, alvo : Unidade):
        if (self.CustoGrua <= self.energia):
            lib.gruaAnim()
            alvo.pontos_vida = alvo.pontos_vida - self.DanoGrua
            self.energia = self.energia - self.CustoGrua

            return True

        else: return False

    def ataque_som(self, alvo : Unidade):
        if (self.CustoSom <= self.energia):
            lib.somAnim() 
            alvo.pontos_vida = alvo.pontos_vida - self.DanoSom
            self.energia = self.energia - self.CustoSom
            
            return True

        else: return False

    def ataque_toque(self, alvo : Unidade):
        if (self.CustoToque <= self.energia):
            lib.toqueAnim() 
            alvo.pontos_vida = alvo.pontos_vida - self.DanoToque
            self.energia = self.energia - self.CustoToque
            
            return True

        else: return False
