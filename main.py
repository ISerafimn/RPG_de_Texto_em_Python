from random import randint
from time import sleep

def dados(): #gira o dado
    return randint(0, 20)


def titulo(msg):
    linha()
    print(f'\033[35m{msg}\033[m'.center(48))
    linha()


def ganhar_item(): #gera um item dentro da lista de itens
    itens = [{'Banana': 'Restaura 20 de Vida'}, {'Maça': 'Restaura 40 de Vida'}, {'Espinafre': 'Aumenta 1 de Força'}]
    bolsa.append(itens[randint(0, 2)])
    return bolsa[-1]


def linha(): #gera uma linha
    print('-' * 40)


def exibir_ficha_jogador(): #exibe a ficha do jogador
    titulo('Janela de Status')
    for keys in ficha_base.keys():
        print(f'\033[34m{keys}:\033[m {ficha_base[keys]}')
    linha()


def exibir_ficha_mob(mob_atual): #exibe a ficha do mob
    linha()
    print('\033[31mCombate\033[m - Mob Status'.center(48))
    linha()
    for keys in mob_atual.keys():
        print(f'\033[34m{keys}:\033[m {mob_atual[keys]}')
    linha()
    sleep(2)


def gerar_mob(lv_base=3, lv_max=10): #gera um mob
    lv_mob = randint(lv_base, lv_max)
    return {'nome': 'monstro', 'lv': 1 * lv_mob, 'hp': 10 * lv_mob, 'hpm': 10 * lv_mob, 'dmg': 1 * lv_mob,
            'spd': 0.75 * lv_mob, 'exp': 8 * lv_mob}


def ganhar_exp(ficha_mob):
    ficha_base['exp'] += ficha_mob['exp']
    print(f'\033[34m{ficha_mob["exp"]} de Experiência ganha!\033[m'.center(48))
    if ficha_base['exp'] > ficha_base['expm']:
        ficha_base['exp'] = ficha_base['exp'] - ficha_base['exp']
        linha()
        ficha_base['lv'] += 1
        upar()
        print(f'\033[1;33mVocê passou de Nível {ficha_base["lv"] - 1} -> {ficha_base["lv"]}\033[m'.center(48))
        ficha_base['expm'] += (ficha_base['expm'] / 2 )
        exibir_ficha_jogador()

def upar():
    ficha_base['dmg'] += 1
    ficha_base['hpm'] += 10
    ficha_base['hp'] = ficha_base['hpm']
    ficha_base['spd'] += 1

def acampar(): #acampa, restaura metade da vida
    titulo('Acampar')
    vida_curada = ficha_base['hpm'] / 2
    ficha_base['hp'] += vida_curada
    if ficha_base['hp'] > ficha_base['hpm']:
        ficha_base['hp'] = ficha_base['hpm']
    print(f'\033[32mVocê recuperou {vida_curada} de vida\033[m')
    sleep(2)
    exibir_ficha_jogador()
    sleep(2)


def explorar(): #explora, através de dado randomiza a chance de entrar em combate, achar um item ou encontrar um npc
    titulo('Explorar')
    if dados() >= 15:
        ganhar_item()
        print(f'Você encontrou um item')
        sleep(1.5)
    else:
        combate()


def turno_jogador(ficha_mob): #executa o ataque do jogador
    linha()
    print(f'{ficha_base["nome"]} atacou o monstro')
    print(f'\033[33m{ficha_base["dmg"]} de dano causado\033[m')
    ficha_mob.update({'hp': int(ficha_mob['hp']) - ficha_base['dmg']})
    print(f'{ficha_mob["hp"]} de Vida Restante do Mob')
    sleep(1.5)


def turno_mob(ficha_mob): #executa o ataque do mob
    linha()
    print(f'{ficha_mob["nome"]} atacou o jogador')
    print(f'\033[31m{ficha_mob["dmg"]} de dano causado\033[m')
    ficha_base.update({'hp': int(ficha_base['hp']) - ficha_mob['dmg']})
    print(f'{ficha_base["hp"]} de vida restante do jogador')
    sleep(1.5)
    

def iniciativa(ficha_mob): #com base na veolcidade, define quem começa atacando
    if ficha_base['spd'] >= ficha_mob['spd']:
        return 'jogador'
    else:
        return 'mob'


def lutando(ficha_mob): #combate
    iniciativa(ficha_mob)
    while True:
        if iniciativa(ficha_mob) == 'jogador':
            turno_jogador(ficha_mob)
            if ficha_mob['hp'] <= 0:
                titulo('Fim da Luta, o jogador venceu')
                ganhar_exp(ficha_mob)
                break
            turno_mob(ficha_mob)
            if ficha_base['hp'] <= 0:
                titulo('Fim da Luta, o monstro venceu')
                break
        else:
            turno_mob(ficha_mob)
            if ficha_base['hp'] <= 0:
                titulo('Fim da Luta, o monstro venceu')
                break
            turno_jogador(ficha_mob)
            if ficha_mob['hp'] <= 0:
                titulo('Fim da Luta, o jogador venceu')
                ganhar_exp(ficha_mob)
                break


def abrir_bolsa():
    titulo('Inventário')
    if len(bolsa) == 0:
        print('Inventário Vazio'.center(40))
    else:
        for i in range(0, len(bolsa)):
            for key in bolsa[i].keys():
                for value in bolsa[i].values():
                    print(f'{i + 1} - {key} : {value}')
    linha()


def fugir(mob_atual):
    if dados() >= 14:
        return True


def combate(): #turno do jogador
    mob_atual = gerar_mob((ficha_base['lv'] + 3), (ficha_base['lv'] + 10))
    exibir_ficha_mob(mob_atual)
    while True:
        try:
            alternativas = ['lutar', 'usar item', 'fugir']
            num_alternativas = alternativas[int(input("""Alternativas Dispopniveis:\033[33m
                                                      
        1) Lutar
        2) Usar Item
        3) Fugir\033[m

Escolha uma das Alternativas: """)) - 1]
            if num_alternativas == 'lutar':
                lutando(mob_atual)
                break
            elif num_alternativas == 'usar item':
                abrir_bolsa()
            elif num_alternativas == 'fugir':
                if fugir(mob_atual):
                    linha()
                    print('\033[32mVocê conseguiu fugir do monstro!\033[m'.center(40))
                    break
                else:
                    linha()
                    print('\033[31mVocê não conseguiu fugir do monstro!\033[m'.center(40))
                    lutando(mob_atual)
                    break
            
        except ValueError:
            print('\033[31mEscolha Inválida!\033[m')


bolsa = list()
ficha_base = {'nome': '', 'raça': '', 'lv': 1, 'hp': 100, 'hpm': 100, 'dmg': 10, 'spd': 5, 'exp': 0, 'expm': 100}

raca_nomes = ['humano', 'orc', 'elfo']
raca_atributos = {'humano': {'hpm': 20, 'dmg': 0, 'spd': 0},
                  'orc': {'hpm': 0, 'dmg': 5, 'spd': 0},
                  'elfo': {'hpm': 0, 'dmg': 0, 'spd': 2}}


titulo('Criação de Personagem')

ficha_base['nome'] = str(input('Digite o Seu Nome: '))

while True:
    try:
        num_raca = raca_nomes[int(input("""Raças Disponiveis:\033[33m
                                        
    1) humano
    2) orc
    3) elfo\033[m
                                        
Escolha uma das raças: """)) - 1]
        break
    except:
        print(f'\033[31mEscolha Inválida!\033[m')

ficha_base['raça'] = num_raca

ficha_base['raça'] = num_raca
ficha_base['hpm'] += raca_atributos[ficha_base['raça']]['hpm']
ficha_base['hp'] += raca_atributos[ficha_base['raça']]['hpm']
ficha_base['dmg'] += raca_atributos[ficha_base['raça']]['dmg']
ficha_base['spd'] += raca_atributos[ficha_base['raça']]['spd']

exibir_ficha_jogador()

while not ficha_base['hp'] <= 0:
    rotas = ['acampar', 'explorar']
    while True:
        try:
            linha()
            num_rotas = rotas[int(input("""Rotas Disponiveis:\033[33m
                                        
    1) acampar
    2) explorar\033[m

Escolha uma das Alternativas: """)) - 1]
        
            break
        except:
            print('\033[31mEscolha Inválida!\033[m')

    for rodada in range(0, 3):
        if num_rotas == 'acampar' and rodada == 0: 
            acampar()
            explorar()
            if ficha_base['hp'] == 0:
                break
        else:
            explorar()
            if ficha_base['hp'] <= 0:
                rodada = 2
                break
    rodada += 1


titulo('\033[33mFim de Jogo\033[m')
