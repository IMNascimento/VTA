import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class LinguisticVariable:
    def __init__(self, name, universe, terms):
        self.name = name
        self.universe = universe
        self.terms = terms
        self.variable = ctrl.Antecedent(universe, name) if name != 'iniciar_ultrapassagem' else ctrl.Consequent(universe, name)
        self._define_terms()
    
    def _define_terms(self):
        for term_name, mf in self.terms.items():
            self.variable[term_name] = mf

    def plot(self, input_value=None, output_value=None, medians=[]):
        # Criação do gráfico utilizando matplotlib
        plt.figure(figsize=(8, 6))
        for label in self.terms:
            plt.plot(self.universe, self.variable[label].mf, label=label)

        # Configurações do gráfico
        plt.title(f'Função de Pertinência - {self.name}')
        plt.xlabel(self.name)
        plt.ylabel('Pertinência')
        plt.legend(loc='upper right')

        # Adicionar valor de entrada
        if input_value is not None:
            plt.axvline(x=input_value, color='red', linestyle='--', label=f'Input: {input_value}')

        # Adicionar valor de saída
        if output_value is not None:
            plt.axvline(x=output_value, color='blue', linestyle='-.', label=f'Output: {output_value}')

        # Salvando o gráfico como PNG
        plt.savefig(f'{self.name}_fuzzy_plot.png')
        plt.close()