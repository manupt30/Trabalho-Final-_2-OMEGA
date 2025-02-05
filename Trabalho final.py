from abc import ABC, abstractmethod

# Códigos ANSI para cores e formatação
AZUL = "\033[94m"    # Texto azul
NEGRITO = "\033[1m"  # Texto em negrito
RESET = "\033[0m"    # Efetuar reset a formatação

# Função para exibir o título do programa
def exibir_titulo():
    titulo = "Sistema de Gestão de Assistencia Tecnica - SisAT"
    borda = "=" * len(titulo)
    print(f"{AZUL}{NEGRITO}{borda}{RESET}")
    print(f"{AZUL}{NEGRITO}{titulo}{RESET}")
    print(f"{AZUL}{NEGRITO}{borda}{RESET}\n")

# Classe abstrata que define os métodos que devem ser implementados pelas classes derivadas
class Intervencao(ABC):
    @abstractmethod
    def avaliar_problema(self):
        pass

    @abstractmethod
    def calcular_custo(self):
        pass

# Classe Cliente que herda da classe abstrata Intervencao
class Cliente(Intervencao):
    def __init__(self, nome, equipamento, problema, dicionario_orcamentos):
        self.nome = nome  # Nome do cliente
        self.equipamento = equipamento  # Nome do equipamento
        self.problema = problema  # Descrição do problema
        self.custo_reparacao = 0  # Custo inicial da reparação
        self.dicionario_orcamentos = dicionario_orcamentos  # Dicionário de orçamentos e custos

    # Método para avaliar o problema e calcular o custo
    def avaliar_problema(self):
        # Divide o problema numa lista de orçamentos e remove espaços extras
        problemas = [p.strip().lower() for p in self.problema.split(",")]
        self.custo_reparacao = 0  # Reinicia o custo da reparação

        print(f"Avaliação do problema para {self.equipamento}: {self.problema}")
        for p in problemas:
            # Verifica se o orçamento está no dicionário de orçamentos
            if p in self.dicionario_orcamentos:
                # Soma o custo do orçamento ao custo total
                self.custo_reparacao += self.dicionario_orcamentos[p]
            else:
                # Se o orçamento não for encontrado, exibe uma mensagem de erro
                print(f"Orçamento '{p}' não encontrado na lista de orçamentos.")

        # Se nenhum custo foi calculado, exibe uma mensagem de problema desconhecido
        if self.custo_reparacao == 0:
            print("Problema desconhecido. Nenhum custo de reparação encontrado.")
        else:
            # Exibe o custo total da reparação
            print(f"Custo estimado de reparação: {self.custo_reparacao}€")

    # Método para devolver o custo da reparação
    def calcular_custo(self):
        return self.custo_reparacao

# Função para criar um ficheiro e escrever o conteúdo
def criar_ficheiro(nome_ficheiro, conteudo):
    try:
        # Abre o ficheiro em modo escrita ("w") e escreve o conteúdo
        with open(nome_ficheiro, "w", encoding="utf-8") as ficheiro:
            ficheiro.write(conteudo)
        print("Ficheiro criado com sucesso!")
    except IOError as e:
        # Em caso de erro, exibe uma mensagem de erro
        print(f"Erro ao criar o ficheiro: {e}")

# Função para visualizar o conteúdo de um ficheiro
def ver_ficheiro(nome_ficheiro):
    try:
        # Abre o ficheiro em modo de leitura ("r") e exibe o conteúdo
        with open(nome_ficheiro, "r", encoding="utf-8") as ficheiro:
            print(ficheiro.read())
    except FileNotFoundError:
        # Se o ficheiro não for encontrado, exibe uma mensagem de erro
        print("Ficheiro não encontrado!")

# Função para editar um ficheiro, adicionando conteúdo ao final
def editar_ficheiro(nome_ficheiro, conteudo):
    try:
        # Abre o ficheiro em modo de adição ("a") e adiciona o conteúdo
        with open(nome_ficheiro, "a", encoding="utf-8") as ficheiro:
            ficheiro.write(conteudo)
        print("Ficheiro editado com sucesso!")
    except IOError as e:
        # Em caso de erro, exibe uma mensagem de erro
        print(f"Erro ao editar o ficheiro: {e}")

# Função para exibir a lista de orçamentos e seus custos
def mostrar_lista_orcamentos(dicionario_orcamentos):
    print("\n--- Lista de Serviços ---")
    print("{:<30} {:<10}".format("Serviço", "Custo (€)"))  # Formata o cabeçalho
    print("-" * 40)  # Linha divisória com 40 -
    for i, (orcamento, custo) in enumerate(dicionario_orcamentos.items(), start=1):
        # Exibe cada orçamento com seu número, cor azul e negrito, e custo em negrito
        print(f"{i}. {AZUL}{NEGRITO}{orcamento}{RESET}: {NEGRITO}{custo}€{RESET}")
    print()

# Função para permitir que o usuário escolha os orçamentos por números
def escolher_orcamentos(dicionario_orcamentos):
    mostrar_lista_orcamentos(dicionario_orcamentos)  # Exibe a lista de orçamentos
    while True:
        escolhas = input("Escolha os números dos orçamentos (separados por vírgula): ").strip()
        problemas = []  # Lista para armazenar os orçamentos escolhidos
        try:
            for escolha in escolhas.split(","):
                indice = int(escolha.strip()) - 1  # Converte o número para índice (começa em 0)
                if 0 <= indice < len(dicionario_orcamentos):
                    # Adiciona o orçamento correspondente ao índice
                    problemas.append(list(dicionario_orcamentos.keys())[indice])
                else:
                    # Se o número for inválido, exibe uma mensagem de erro
                    print(f"Número inválido: {escolha.strip()}. Tente novamente.")
                    break
            else:
                # Devolve os orçamentos escolhidos como uma string separada por vírgulas
                return ", ".join(problemas)
        except ValueError:
            # Se a entrada não for um número, exibe uma mensagem de erro
            print(f"Entrada inválida: '{escolhas}'. Por favor, insira números separados por vírgula.")

# Função para formatar o conteúdo de uma intervenção para o ficheiro
def formatar_conteudo(cliente, problema_formatado):
    # Cria uma string formatada com várias linhas
    conteudo = (
        f"--- Intervenção ---\n"
        f"Nome: {cliente.nome}\n"
        f"Equipamento: {cliente.equipamento}\n"
        f"Problema: {AZUL}{NEGRITO}{problema_formatado}{RESET}\n"
        f"Custo: {NEGRITO}{cliente.calcular_custo()}€{RESET}\n"
        f"-------------------\n\n"
    )
    return conteudo

# Função principal do programa
def main():
    # Dicionário de orçamentos normalizado (chaves em minúsculas e sem espaços extras)
    dicionario_orcamentos = {
        "trocar disco": 50,
        "trocar placa grafica": 120,
        "trocar fonte alimentacao": 30,
        "remover virus do sistema operativo": 50,
        "limpeza interna": 20
    }
    
    # Dicionário para exibição (com capitalização correta)
    dicionario_exibicao = {
        "Trocar Disco": 50,
        "Trocar Placa Grafica": 120,
        "Trocar Fonte Alimentacao": 30,
        "Remover Virus do Sistema Operativo": 50,
        "Limpeza Interna": 20
    }
    
    nome_ficheiro = "equipamentos.txt"  # Nome do ficheiro para armazenar as intervenções

    # Exibe o título do programa
    exibir_titulo()

    while True:
        try:
            # Exibe o menu de opções com as opções em negrito
            opcao = int(input(f"{NEGRITO}Escolha uma opção:{RESET} {NEGRITO}1{RESET} - Criar Ficheiro, {NEGRITO}2{RESET} - Ver Ficheiro, {NEGRITO}3{RESET} - Editar Ficheiro, {NEGRITO}4{RESET} - Ver Lista de Orçamentos, {NEGRITO}5{RESET} - Sair: "))
            if opcao == 1:
                # Opção para criar um ficheiro
                nome = input("Digite o nome do cliente: ").strip().title()
                equipamento = input("Digite o nome do equipamento: ").strip().title()
                problema = escolher_orcamentos(dicionario_exibicao)  # Escolhe os orçamentos
                problema_normalizado = problema.lower()  # Normaliza o problema para minúsculas
                cliente = Cliente(nome, equipamento, problema_normalizado, dicionario_orcamentos)
                cliente.avaliar_problema()  # Avalia o problema e calcula o custo
                conteudo = formatar_conteudo(cliente, problema)  # Formata o conteúdo
                criar_ficheiro(nome_ficheiro, conteudo)  # Cria o ficheiro
            elif opcao == 2:
                # Opção para visualizar o ficheiro
                ver_ficheiro(nome_ficheiro)
            elif opcao == 3:
                # Opção para editar o ficheiro
                nome = input("Digite o nome do cliente: ").strip().title()
                equipamento = input("Digite o nome do equipamento: ").strip().title()
                problema = escolher_orcamentos(dicionario_exibicao)  # Escolhe os orçamentos
                problema_normalizado = problema.lower()  # Normaliza o problema para minúsculas
                cliente = Cliente(nome, equipamento, problema_normalizado, dicionario_orcamentos)
                cliente.avaliar_problema()  # Avalia o problema e calcula o custo
                conteudo = formatar_conteudo(cliente, problema)  # Formata o conteúdo
                editar_ficheiro(nome_ficheiro, conteudo)  # Edita o ficheiro
            elif opcao == 4:
                # Opção para exibir a lista de orçamentos
                mostrar_lista_orcamentos(dicionario_exibicao)
            elif opcao == 5:
                # Opção para sair do programa
                confirmacao = input("Tem certeza que deseja sair? (s/n): ").strip().lower()
                if confirmacao == "s":
                    print("Sair...")
                    break
            else:
                # Se a opção for inválida, exibe uma mensagem de erro
                print("Opção inválida. Tente novamente.")
        except ValueError:
            # Se a entrada não for um número, exibe uma mensagem de erro
            print("Entrada inválida. Por favor, insira um número.")

# Executa o programa se este arquivo for o principal
if __name__ == "__main__":
    main()
