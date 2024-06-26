from random import randint
from time import sleep

def dados(): #gira o dado
    return randint(0, 20)

def erro_msg():
    linha()
    print(f'\033[31mEscolha Inválida!\033[m'.center(48))
    linha()

def titulo(msg):
    linha()
    print(f'\033[35m{msg}\033[m'.center(48))
    linha()


def ganhar_item(): #gera um item dentro da lista de itens
    itens = [{'Banana': ['Restaura a vida', '20']}, {'Maça': ['Restaura a vida', '40']}, {'Espinafre': ['Restaura a vida', '50']}]
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
    sleep(1.5)


def gerar_mob(lv_base=3, lv_max=10): #gera um mob
    lv_mob = randint(lv_base, lv_max)
    return {'nome': 'monstro', 'lv': 1 * lv_mob, 'hp': 10 * lv_mob, 'hpm': 10 * lv_mob, 'dmg': 1 * lv_mob,
            'spd': 0.75 * lv_mob, 'exp': 8 * lv_mob}


def ganhar_exp(ficha_mob):
    ficha_base['exp'] += ficha_mob['exp']
    print(f'\033[34m{ficha_mob["exp"]} de Experiência ganha!\033[m'.center(48))
    while ficha_base['exp'] > ficha_base['expm']:
        if ficha_base['exp'] > ficha_base['expm']:
            linha()
            ficha_base['lv'] += 1
            upar()
            ficha_base['exp'] = ficha_base['exp'] - ficha_base['expm']
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
    sleep(1.5)
    exibir_ficha_jogador()
    sleep(1.5)


def explorar(): #explora, através de dado randomiza a chance de entrar em combate, achar um item ou encontrar um npc
    titulo('Explorando')
    print('\033[33mgirando dados...\033[m'.center(48))
    sleep(1.5)
    dado = dados()
    titulo(f'dado caiu em {dado}')
    if dado >= 15:
        for keys in ganhar_item().keys():
            print(f'Você encontrou um(a) \033[34m{keys}\033[m'.center(48))
            sleep(1.5)
    else:
        sleep(0.5)
        combate()


def turno_jogador(ficha_mob): #executa o ataque do jogador
    linha()
    print(f'{ficha_base["nome"]} atacou o monstro')
    print(f'\033[33m{ficha_base["dmg"]} de dano causado\033[m')
    ficha_mob.update({'hp': int(ficha_mob['hp']) - ficha_base['dmg']})
    print(f'{ficha_mob["hp"]} de Vida Restante do Mob')
    sleep(0.5)


def turno_mob(ficha_mob): #executa o ataque do mob
    linha()
    print(f'{ficha_mob["nome"]} atacou o jogador')
    print(f'\033[31m{ficha_mob["dmg"]} de dano causado\033[m')
    ficha_base.update({'hp': int(ficha_base['hp']) - ficha_mob['dmg']})
    print(f'{ficha_base["hp"]} de vida restante do jogador')
    sleep(0.5)
    

def iniciativa(ficha_mob): #com base na veolcidade, define quem começa atacando
    if ficha_base['spd'] >= ficha_mob['spd']:
        return 'jogador'
    else:
        return 'mob'


def lutando(ficha_mob, tentativa_fuga=False): #combate
    iniciativa(ficha_mob)
    if tentativa_fuga:
        turno_mob(ficha_mob)
        if ficha_base['hp'] <= 0:
            titulo('Fim da Luta, o monstro venceu')
        else:
            linha()
            escolha_combate(ficha_mob)
    else:
        if iniciativa(ficha_mob) == 'jogador':
            turno_jogador(ficha_mob)
            if ficha_mob['hp'] <= 0:
                titulo('Fim da Luta, o jogador venceu')
                ganhar_exp(ficha_mob)
            else:
                turno_mob(ficha_mob)
            if ficha_base['hp'] <= 0:
                titulo('Fim da Luta, o monstro venceu')
            else:
                linha()
                escolha_combate(ficha_mob)
        else:
            turno_mob(ficha_mob)
            if ficha_base['hp'] <= 0:
                titulo('Fim da Luta, o monstro venceu')
            else:
                turno_jogador(ficha_mob)
            if ficha_mob['hp'] <= 0:
                titulo('Fim da Luta, o jogador venceu')
                ganhar_exp(ficha_mob)
            else:
                linha()
                escolha_combate(ficha_mob)


def abrir_bolsa():
    titulo('Inventário')
    if len(bolsa) == 0:
        print('Inventário Vazio'.center(40))
        linha()
    else:
        while True:
            try:
                for i in range(0, len(bolsa)):
                    for key in bolsa[i].keys():
                        for value in bolsa[i].values():
                            print(f'{i + 1} - \033[34m{key}\033[m : {value[0]} = {value[1]} hp')
                usar_item = bolsa[int(input('\nEscolha o Item que será Utilizado: ')) - 1]
                linha()
                for keys in usar_item.keys():
                    print(f'Você Consumiu um(a) \033[34m{keys}\033[m'.center(48))
                    linha()
                    vida_recuperda = usar_item[key][1]
                    print(f'\033[32mVocê Recuperou {vida_recuperda} de Vida\033[m'.center(48))
                    linha()
                break
            except:
                erro_msg()
    ficha_base['hp'] += int(vida_recuperda)
    if ficha_base['hp'] > ficha_base['hpm']:
        ficha_base['hp'] = ficha_base['hpm']


def fugir(mob_atual):
    if dados() >= 14:
        return True

def escolha_combate(mob_atual):
    while True:
        if mob_atual['hp'] <= 0 or ficha_base['hp'] <= 0:
            break
        try:
            alternativas = ['lutar', 'usar item', 'fugir']
            print('\033[35mTurno do Jogador\033[m'.center(48))
            linha()
            for i in range(0, len(alternativas)):
                print(f'\033[33m{i + 1}) {alternativas[i]}\033[m')
            num_alternativas = alternativas[int(input('\nEscolha uma das Alternativas:')) - 1]
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
                    lutando(mob_atual, True)
                    break
            
        except:
            erro_msg()



def combate(): #turno do jogador
    mob_atual = gerar_mob((ficha_base['lv'] + 3), (ficha_base['lv'] + 10))
    exibir_ficha_mob(mob_atual)
    escolha_combate(mob_atual)


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
        erro_msg()

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
            erro_msg()

    for rodada in range(0, 3):
        if num_rotas == 'acampar' and rodada == 0: 
            acampar()
            explorar()
            if ficha_base['hp'] == 0:
                rodada = 2
                break
        else:
            explorar()
            if ficha_base['hp'] <= 0:
                rodada = 2
                break
    rodada += 1


titulo('\033[33mFim de Jogo\033[m')