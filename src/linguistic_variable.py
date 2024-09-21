import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class LinguisticVariable:
    def __init__(self, name, universe, terms):
        """
        Inicializa a variável linguística com seu nome, universo de discurso e termos fuzzy.
        
        :param name: Nome da variável linguística.
        :param universe: Universo de discurso da variável.
        :param terms: Dicionário contendo os termos fuzzy e suas funções de pertinência.
        """
        self._name = name
        self._universe = universe
        self._terms = terms
        self._variable = ctrl.Antecedent(universe, name) if name != 'overtake_decision' else ctrl.Consequent(universe, name)
        self._define_terms()
    
    def _define_terms(self):
        """
        Define os termos fuzzy e suas funções de pertinência para a variável linguística.
        """
        for term_name, mf in self._terms.items():
            self._variable[term_name] = mf

    def plot(self, input_value=None, output_value=None, medians=[]):
        """
        Plota a função de pertinência da variável linguística.
        
        :param input_value: Valor de entrada que será mostrado no gráfico (opcional).
        :param output_value: Valor de saída que será mostrado no gráfico (opcional).
        :param medians: Lista de valores medianos (opcional).
        """
        plt.figure(figsize=(8, 6))
        for label in self._terms:
            plt.plot(self._universe, self._variable[label].mf, label=label)

        # Configurações do gráfico
        plt.title(f'Função de Pertinência - {self._name}')
        plt.xlabel(self._name)
        plt.ylabel('Pertinência')
        plt.legend(loc='upper right')

        # Adicionar valor de entrada
        if input_value is not None:
            plt.axvline(x=input_value, color='red', linestyle='--', label=f'Input: {input_value}')

        # Adicionar valor de saída
        if output_value is not None:
            plt.axvline(x=output_value, color='blue', linestyle='-.', label=f'Output: {output_value}')

        # Salvando o gráfico como PNG
        plt.savefig(f'{self._name}_fuzzy_plot.png')
        plt.close()



    @property
    def variable(self):
        return self._variable