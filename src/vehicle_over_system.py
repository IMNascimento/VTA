from src.linguistic_variable import LinguisticVariable
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class VehicleOvertakeSystem:
    def __init__(self):
        self.distancia = LinguisticVariable('distancia', np.arange(0, 500, 1), {
            'pequena': fuzz.trapmf(np.arange(0, 500, 1), [0, 0, 100, 200]),
            'media': fuzz.trimf(np.arange(0, 500, 1), [150, 250, 350]),
            'grande': fuzz.trapmf(np.arange(0, 500, 1), [300, 400, 500, 500])
        })

        self.velocidade_relativa = LinguisticVariable('velocidade_relativa', np.arange(0, 250, 1), {
            'baixa': fuzz.trapmf(np.arange(0, 250, 1), [0, 0, 50, 100]),
            'media': fuzz.trimf(np.arange(0, 250, 1), [80, 150, 200]),
            'alta': fuzz.trapmf(np.arange(0, 250, 1), [150, 200, 250, 250])
        })

        self.permissao = LinguisticVariable('permissao', np.arange(0, 1.1, 0.1), {
            'nao_permitido': fuzz.trimf(np.arange(0, 1.1, 0.1), [0, 0, 0.5]),
            'permitido': fuzz.trimf(np.arange(0, 1.1, 0.1), [0.5, 1, 1])
        })

        self.pista = LinguisticVariable('pista', np.arange(0, 1.1, 0.1), {
            'obstruida': fuzz.trimf(np.arange(0, 1.1, 0.1), [0, 0, 0.5]),
            'livre': fuzz.trimf(np.arange(0, 1.1, 0.1), [0.5, 1, 1])
        })

        self.visibilidade = LinguisticVariable('visibilidade', np.arange(0, 1.1, 0.1), {
            'ruim': fuzz.trimf(np.arange(0, 1.1, 0.1), [0, 0, 0.5]),
            'boa': fuzz.trimf(np.arange(0, 1.1, 0.1), [0.5, 1, 1])
        })

        self.iniciar_ultrapassagem = LinguisticVariable('iniciar_ultrapassagem', np.arange(0, 1.1, 0.1), {
            'nao': fuzz.trimf(np.arange(0, 1.1, 0.1), [0, 0, 0.5]),
            'sim': fuzz.trimf(np.arange(0, 1.1, 0.1), [0.5, 1, 1])
        })

    def create_rules(self):
        # Regras existentes
        rule1 = ctrl.Rule(
            self.distancia.variable['pequena'] & self.velocidade_relativa.variable['alta'] &
            self.permissao.variable['permitido'] & self.pista.variable['livre'] &
            self.visibilidade.variable['boa'], self.iniciar_ultrapassagem.variable['sim']
        )

        rule2 = ctrl.Rule(
            self.distancia.variable['pequena'] & self.velocidade_relativa.variable['media'] &
            self.permissao.variable['permitido'] & self.pista.variable['livre'] &
            self.visibilidade.variable['boa'], self.iniciar_ultrapassagem.variable['sim']
        )

        rule3 = ctrl.Rule(
            self.distancia.variable['grande'] | self.velocidade_relativa.variable['baixa'] |
            self.pista.variable['obstruida'], self.iniciar_ultrapassagem.variable['nao']
        )

        rule4 = ctrl.Rule(
            self.distancia.variable['media'] & self.velocidade_relativa.variable['alta'] &
            self.permissao.variable['permitido'] & self.pista.variable['livre'],
            self.iniciar_ultrapassagem.variable['sim']
        )

        # Regras adicionais para cobrir mais cenários:
        
        # Se a visibilidade for ruim, não deve ultrapassar, independentemente das outras variáveis
        rule5 = ctrl.Rule(
            self.visibilidade.variable['ruim'], self.iniciar_ultrapassagem.variable['nao']
        )

        # Se a pista estiver obstruída, não deve ultrapassar
        rule6 = ctrl.Rule(
            self.pista.variable['obstruida'], self.iniciar_ultrapassagem.variable['nao']
        )
        
        # Se a permissão for negada (não_permitido), não deve ultrapassar
        rule7 = ctrl.Rule(
            self.permissao.variable['nao_permitido'], self.iniciar_ultrapassagem.variable['nao']
        )
        
        # Se a distância for grande e a velocidade for alta, não deve ultrapassar
        rule8 = ctrl.Rule(
            self.distancia.variable['grande'] & self.velocidade_relativa.variable['alta'],
            self.iniciar_ultrapassagem.variable['nao']
        )
        
        # Se a distância for pequena, a velocidade for baixa e a permissão for dada, deve ultrapassar
        rule9 = ctrl.Rule(
            self.distancia.variable['pequena'] & self.velocidade_relativa.variable['baixa'] &
            self.permissao.variable['permitido'], self.iniciar_ultrapassagem.variable['sim']
        )

        # Se a distância for média, a velocidade for média e a visibilidade for boa, deve ultrapassar
        rule10 = ctrl.Rule(
            self.distancia.variable['media'] & self.velocidade_relativa.variable['media'] &
            self.visibilidade.variable['boa'], self.iniciar_ultrapassagem.variable['sim']
        )

        # Se a velocidade for muito alta, mas a permissão e visibilidade forem boas, deve ultrapassar
        rule11 = ctrl.Rule(
            self.velocidade_relativa.variable['alta'] & self.permissao.variable['permitido'] &
            self.visibilidade.variable['boa'], self.iniciar_ultrapassagem.variable['sim']
        )

        # Se a velocidade for baixa e a visibilidade for ruim, não deve ultrapassar
        rule12 = ctrl.Rule(
            self.velocidade_relativa.variable['baixa'] & self.visibilidade.variable['ruim'],
            self.iniciar_ultrapassagem.variable['nao']
        )
        rule13 = ctrl.Rule(
            self.distancia.variable['pequena'] & self.velocidade_relativa.variable['alta'],
            self.iniciar_ultrapassagem.variable['nao']
        )
        rule14 = ctrl.Rule(
            self.velocidade_relativa.variable['baixa'] & self.visibilidade.variable['boa'] & 
            self.pista.variable['livre'], self.iniciar_ultrapassagem.variable['sim']
        )
        rule15 = ctrl.Rule(
            self.visibilidade.variable['boa'] & (self.pista.variable['obstruida'] | self.permissao.variable['nao_permitido']),
            self.iniciar_ultrapassagem.variable['nao']
        )
        #Regra de fallback para casos não cobertos (padrão de segurança):
        rule16 = ctrl.Rule(
            ~((self.distancia.variable['pequena'] | self.distancia.variable['media'] | self.distancia.variable['grande']) &
            (self.velocidade_relativa.variable['baixa'] | self.velocidade_relativa.variable['media'] | self.velocidade_relativa.variable['alta']) &
            (self.permissao.variable['permitido'] | self.permissao.variable['nao_permitido']) &
            (self.pista.variable['livre'] | self.pista.variable['obstruida']) &
            (self.visibilidade.variable['boa'] | self.visibilidade.variable['ruim'])),
            self.iniciar_ultrapassagem.variable['nao']
        )

        # Adicionando todas as regras criadas à lista de regras
        return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15]

    def simulate(self, inputs):
        try:
            # Cria o sistema de controle e a simulação
            rules = self.create_rules()
            ultrapassagem_ctrl = ctrl.ControlSystem(rules)
            ultrapassagem_sim = ctrl.ControlSystemSimulation(ultrapassagem_ctrl)

            # Passa as entradas
            ultrapassagem_sim.input['distancia'] = inputs['distancia']
            ultrapassagem_sim.input['velocidade_relativa'] = inputs['velocidade_relativa']
            ultrapassagem_sim.input['permissao'] = inputs['permissao']
            ultrapassagem_sim.input['pista'] = inputs['pista']
            ultrapassagem_sim.input['visibilidade'] = inputs['visibilidade']

            # Realiza a computação
            ultrapassagem_sim.compute()
            return ultrapassagem_sim.output['iniciar_ultrapassagem']
        except ValueError as e:
            print(f"Erro na simulação: {e}")
            return None