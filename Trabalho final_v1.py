from abc import ABC, abstractmethod

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
    def __init__(self, nome, equipamento, problema, dicionario_avarias):
        self.nome = nome  # Nome do cliente
        self.equipamento = equipamento  # Nome do equipamento
        self.problema = problema  # Descrição do problema
        self.custo_reparacao = 0  # Custo inicial da reparação
        self.dicionario_avarias = dicionario_avarias  # Dicionário de avarias e custos

    # Método para avaliar o problema e calcular o custo
    def avaliar_problema(self):
        # Divide o problema em uma lista de avarias e remove espaços extras
        problemas = [p.strip().lower() for p in self.problema.split(",")]
        self.custo_reparacao = 0  # Reinicia o custo da reparação

        print(f"Avaliação do problema para {self.equipamento}: {self.problema}")
        for p in problemas:
            # Verifica se a avaria está no dicionário de avarias
            if p in self.dicionario_avarias:
                # Soma o custo da avaria ao custo total
                self.custo_reparacao += self.dicionario_avarias[p]
            else:
                # Se a avaria não for encontrada, exibe uma mensagem de erro
                print(f"Avaria '{p}' não encontrada na lista de avarias.")

        # Se nenhum custo foi calculado, exibe uma mensagem de problema desconhecido
        if self.custo_reparacao == 0:
            print("Problema desconhecido. Nenhum custo de reparação encontrado.")
        else:
            # Exibe o custo total da reparação
            print(f"Custo estimado de reparação: {self.custo_reparacao}€")

    # Método para retornar o custo da reparação
    def calcular_custo(self):
        return self.custo_reparacao