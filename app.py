import itertools
import random
from time import sleep
import os

class Player:
    # Classe que representa o jogador, com um saldo inicial.
    def __init__(self, balance = 100):
        self.balance = balance

class CassaNiquel:
    # Classe que representa a máquina caça-níquel
    def __init__(self, level = 1, balance = 0):
        # Dicionário com os símbolos (emojis) e seus códigos Unicode.
        self.SYMBOLS = {
            'money_mouth_face': '1F911',
            'cold_face': '1F976',
            'alien': '1F47D',
            'heart_on_fire': '2764',
            'collision': '1F4A5'
        }
        self.level = level  # Nível da máquina (dificuldade, potencialmente)
        self.permutations = self._gen_permutation()  # Todas as combinações possíveis de símbolos
        self.balance = 0  # Saldo da máquina, inicia em 0
        self.initial_balance = self.balance  # Armazena o saldo inicial

    def _gen_permutation(self):
        # Gera todas as combinações possíveis de símbolos em trios.
        permutations = list(itertools.product(self.SYMBOLS.keys(), repeat=3))
        # Adiciona mais combinações de trios iguais, aumentando a chance de repetições
        for j in range(self.level):
            for i in self.SYMBOLS.keys():
                permutations.append((i, i, i,))
        return permutations
    
    def _get_end_result(self):
        # Seleciona aleatoriamente um trio de símbolos como o resultado final
        result = list(random.choice(self.permutations))

        # Se os três símbolos forem diferentes, há uma chance de alterar o resultado
        if len(set(result)) == 3 and random.randint(0, 5) >= 2:
            result[1] = result[0]  # Torna o segundo símbolo igual ao primeiro
        return result
    
    def _display(self, amount_bet, result, time=0.4):
        # Exibe a rotação aleatória de símbolos e o resultado final.
        seconds = 4  # Define a duração da exibição
        for i in range(0, int(seconds/time)):
            print(self._emojize(random.choice(self.permutations)))  # Mostra uma combinação aleatória
            sleep(time)
            # Limpa a tela de forma multiplataforma
            if os.name == 'posix':  # Para Unix/Linux/Mac
                os.system('clear')
            elif os.name == 'nt':  # Para Windows
                 os.system('cls')
            #os.system('cls')  # Limpa a tela (funciona no Windows com 'cls')
        
        # Exibe o resultado final da rotação
        print(self._emojize(result))

        # Verifica se o jogador venceu ou perdeu
        if self._check_result_user(result):
            print(f"Você venceu e recebeu: {amount_bet * 3}")
        else:
            print(f"Foi quase, tente novamente!")

    def _emojize(self, emojis):
        # Converte os códigos Unicode em emojis visuais
        return ''.join(tuple(chr(int(self.SYMBOLS[code], 16)) for code in emojis))

    def _check_result_user(self, result):
        # Verifica se todos os símbolos no resultado são iguais (vitória do jogador)
        emoji = [result[0] == emoji for emoji in result]
        return True if all(emoji) else False
    
    def _update_balance(self, amount_bet, result, player: Player):
        # Atualiza os saldos do jogador e da máquina com base no resultado.
        if self._check_result_user(result):
            # Se o jogador venceu, ele recebe o triplo da aposta
            self.balance -= (amount_bet * 3)
            player.balance += (amount_bet * 3)
        else:
            # Se o jogador perdeu, a máquina ganha a aposta
            self.balance += amount_bet
            player.balance -= amount_bet

    def play(self, amount_bet, player: Player):
        # Executa uma rodada de jogo.
        result = self._get_end_result()  # Gera o resultado final da rotação
        self._display(amount_bet, result)  # Exibe o resultado e a animação
        self._update_balance(amount_bet, result, player)  # Atualiza os saldos

# Inicializa uma máquina caça-níquel com nível 1
# AJUSTADO PRA QUANDO O LEVEL DE "INFLUENCIA" do usuário for alto,
# mais chances ele tem de ganhar
maquina1 = CassaNiquel(level=100)
# Inicializa um jogador com saldo padrão
player1 = Player()

# maquina1.play(10)
# maquina1.play(10)
# maquina1.play(10)
# maquina1.play(10)
# maquina1.play(10)

# Executa 10 rodadas de jogo, apostando 10 em cada rodada
for i in range(0, 5):
    maquina1.play(10, player1)

# maquina1._gen_permutation()
# maquina1._get_end_result()
# maquina1._display(1, maquina1._get_end_result())

# Exibe os saldos finais da máquina e do jogador
print("Saldo final da máquina:", maquina1.balance)
print("Saldo final do jogador:", player1.balance)