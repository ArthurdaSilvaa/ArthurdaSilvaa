import random
import time


def executar_com_retry(func, tentativas=3, delay=1):
    for tentativa in range(tentativas):
        try:
            print(f"🔄 Tentativa {tentativa + 1}...")
            resultado = func()
            return resultado
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            if tentativa < tentativas - 1:
                print(f"⏳ Tentando novamente em {delay}s...\n")
                time.sleep(delay)
            else:
                print("❌ Falha após várias tentativas.")
                return None


class HashTable:
    def __init__(self, tamanho=100):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho

    def _hash(self, chave):
        return hash(chave) % self.tamanho

    def inserir(self, chave, valor):
        indice = self._hash(chave)
        while self.tabela[indice] is not None:
            if self.tabela[indice][0] == chave:
                self.tabela[indice][1].append(valor)
                return
            indice = (indice + 1) % self.tamanho
        self.tabela[indice] = (chave, [valor])

    def remover_ingresso(self, chave, valor):
        indice = self._hash(chave)
        while self.tabela[indice] is not None:
            if self.tabela[indice][0] == chave:
                if valor in self.tabela[indice][1]:
                    self.tabela[indice][1].remove(valor)

                    if not self.tabela[indice][1]:
                        self.tabela[indice] = None
                    return True
            indice = (indice + 1) % self.tamanho
        return False

    def consultar(self, chave):
        indice = self._hash(chave)
        while self.tabela[indice] is not None:
            if self.tabela[indice][0] == chave:
                return self.tabela[indice][1]
            indice = (indice + 1) % self.tamanho
        return []

    def mostrar(self):
        for item in self.tabela:
            if item:
                print(f"{item[0]} -> {item[1]}")

    def total_usuarios(self):
        contador = 0
        for item in self.tabela:
            if item is not None:
                contador += 1
        return contador


class Estadio:
    def __init__(self, fileiras=5, colunas=5):
        self.fileiras = fileiras
        self.colunas = colunas
        self.mapa = {}

        for f in range(1, fileiras + 1):
            for c in range(1, colunas + 1):
                self.mapa[f"{f}-{c}"] = None

    def mostrar_cadeiras(self):
        print("\nMapa de Cadeiras (Fileira-Coluna):")
        for f in range(1, self.fileiras + 1):
            linha = ""
            for c in range(1, self.colunas + 1):
                pos = f"{f}-{c}"
                if self.mapa[pos] is None:
                    linha += f"[{pos}] "
                else:
                    linha += "[X] "
            print(linha)

    def reservar_cadeira(self, posicao, usuario):
        if random.random() < 0.3:
            raise Exception("Falha no sistema de reservas!")

        if posicao not in self.mapa:
            print(" Cadeira inexistente.")
            return False
        if self.mapa[posicao] is not None:
            print(" Cadeira já ocupada.")
            return False

        self.mapa[posicao] = usuario
        return True

    def cancelar_reserva(self, posicao, usuario):
        if self.mapa.get(posicao) == usuario:
            self.mapa[posicao] = None
            return True
        return False


usuarios = HashTable()
estadio = Estadio(5, 5)


def ler_opcao_valida():
    opcao = input("Escolha uma opção: ")

    if opcao not in ['1', '2', '3', '4', '5', '6']:
        raise ValueError("Opção inválida!")

    return opcao


def menu():
    while True:
        print("\n Sistema de Compra de Ingressos")
        print("1. Ver cadeiras disponíveis")
        print("2. Comprar ingresso")
        print("3. Cancelar ingresso")
        print("4. Ver ingressos comprados")
        print("5. Mostrar todos os usuários")
        print("6. Sair")

        opcao = executar_com_retry(ler_opcao_valida)

        if opcao is None:
            print("❌ Encerrando sistema por erro de entrada.")
            break

        if opcao == '1':
            estadio.mostrar_cadeiras()

        elif opcao == '2':
            nome = input("Seu nome: ")
            pos = input("Escolha a cadeira (ex: 2-3): ")

            total = usuarios.total_usuarios()

            # 🔥 Limite com RANGE + ENCERRAMENTO
            if total not in range(0, 4):
                print("🚨 Sistema travou!")
                print("🔒 Encerrando sistema...")
                break # This break is now correctly placed within the while True loop

            def tentativa_reserva():
                return estadio.reservar_cadeira(pos, nome)

            resultado = executar_com_retry(tentativa_reserva)

            if resultado:
                usuarios.inserir(nome, pos)
                print(f" Ingresso reservado para {nome} na cadeira {pos}.")

        elif opcao == '3':
            try:
                nome = input("Seu nome: ")
                pos = input("Cadeira a cancelar (ex: 2-3): ")

                if estadio.cancelar_reserva(pos, nome):
                    usuarios.remover_ingresso(nome, pos)
                    print(" Reserva cancelada.")
                else:
                    print(" Você não tem essa reserva.")

            except Exception as e:
                print(f"❌ Erro ao cancelar: {e}")

        elif opcao == '4':
            nome = input("Seu nome: ")
            ingressos = usuarios.consultar(nome)

            if ingressos:
                print(f" Ingressos de {nome}: {ingressos}")
            else:
                print(" Nenhum ingresso encontrado.")

        elif opcao == '5':
            print("\n Lista de usuários:")
            usuarios.mostrar()

        elif opcao == '6':
            print(" Obrigado por usar o sistema!")
            break


menu()