import random
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

class TestDataGenerator:
    def __init__(self, quantidade=None, caminho_csv=None):
        self.quantidade = quantidade
        self.caminho_csv = caminho_csv
        self.dados = None

    def gerar_dados_de_teste(self):
        """
        Gera cenários de teste aleatórios com um target para medir o acerto do modelo.
        
        :return: DataFrame com os cenários gerados e o target (1 para ultrapassagem, 0 para não ultrapassagem).
        """
        if not self.quantidade:
            raise ValueError("Defina a quantidade de dados a serem gerados.")
        
        dados = []
        
        for _ in range(self.quantidade):
            # Gerar valores aleatórios dentro dos intervalos especificados
            distancia = random.uniform(1, 500)  # Distância entre 1 e 500 metros
            velocidade_relativa = random.uniform(1, 250)  # Velocidade relativa entre 1 e 250
            permissao = random.uniform(0, 1)  # Permissão (0 a 1)
            pista = random.uniform(0, 1)  # Condições da pista (0 a 1)
            visibilidade = random.uniform(0, 1)  # Visibilidade (0 a 1)
            
            # Definir uma regra simples para o target
            if (200 > distancia > 100 and 140 < velocidade_relativa < 200 and permissao > 0.5 and pista > 0.5 and visibilidade > 0.5) or \
               (distancia > 100 and velocidade_relativa > 80 and permissao > 0.5 and pista > 0.5 and visibilidade > 0.5) or \
               (distancia < 100 and velocidade_relativa > 200 and permissao > 0.5 and pista > 0.5 and visibilidade > 0.6):
                target = 1  # Deve ultrapassar
            else:
                target = 0  # Não deve ultrapassar
            
            # Adicionar os valores ao conjunto de dados
            dados.append({
                'distancia': round(distancia, 2),
                'velocidade_relativa': round(velocidade_relativa, 2),
                'permissao': round(permissao, 2),
                'pista': round(pista, 2),
                'visibilidade': round(visibilidade, 2),
                'target': target  # Target binário (1 para ultrapassagem, 0 para não)
            })
        
        # Converter a lista em um DataFrame para facilitar a manipulação
        self.dados = pd.DataFrame(dados)
        return self.dados

    def carregar_dados_csv(self):
        """
        Carrega dados de um arquivo CSV.
        
        :return: DataFrame com os dados carregados.
        """
        if not self.caminho_csv:
            raise ValueError("Caminho do CSV não fornecido.")
        
        self.dados = pd.read_csv(self.caminho_csv)
        return self.dados

    def balancear_dados(self, metodo="undersample"):
        """
        Aplica o balanceamento dos dados utilizando undersampling ou oversampling.
        
        :param metodo: Método de balanceamento ("undersample" ou "oversample").
        :return: DataFrame balanceado.
        """
        if self.dados is None:
            raise ValueError("Os dados de teste ainda não foram gerados ou carregados. Chame 'gerar_dados_de_teste()' ou 'carregar_dados_csv()' antes de balancear.")
        
        X = self.dados[['distancia', 'velocidade_relativa', 'permissao', 'pista', 'visibilidade']]
        y = self.dados['target']
        
        if metodo == "undersample":
            sampler = RandomUnderSampler()
        elif metodo == "oversample":
            sampler = RandomOverSampler()
        else:
            raise ValueError("Método inválido. Escolha 'undersample' ou 'oversample'.")
        
        X_resampled, y_resampled = sampler.fit_resample(X, y)
        
        # Combinar os dados balanceados novamente em um DataFrame
        df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='target')], axis=1)
        return df_resampled