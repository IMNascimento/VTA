import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from src.linguistic_variable import LinguisticVariable

class VehicleOvertakeSystem:
    def __init__(self):
        # Ajustando o intervalo de distância para até 50 metros
        self.distance = LinguisticVariable('distance', np.arange(0, 51, 1), {
            'pequena': fuzz.trapmf(np.arange(0, 51, 1), [0, 0, 10, 20]),
            'media': fuzz.trimf(np.arange(0, 51, 1), [15, 25, 35]),
            'grande': fuzz.trapmf(np.arange(0, 51, 1), [30, 40, 50, 50])
        })

        # Ajustando o intervalo de velocidade relativa para até 56 m/s
        self.relative_speed = LinguisticVariable('relative_speed', np.arange(0, 57, 1), {
            'baixa': fuzz.trapmf(np.arange(0, 57, 1), [0, 0, 10, 20]),
            'media': fuzz.trimf(np.arange(0, 57, 1), [15, 30, 45]),
            'alta': fuzz.trapmf(np.arange(0, 57, 1), [40, 50, 56, 56])
        })

            
        # Visibilidade: função de pertinência com transição suave
        self.visibility = LinguisticVariable('visibility', np.arange(0, 1.1, 0.1), {
            'ruim': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0, 0, 0.3, 0.5]),  # Transição suave de ruim para boa
            'boa': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0.4, 0.6, 1, 1])    # Sobreposição entre 0.4 e 0.6
        })

        # Permissão: função de pertinência com transição suave
        self.permission = LinguisticVariable('permission', np.arange(0, 1.1, 0.1), {
            'nao_permitido': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0, 0, 0.3, 0.5]),  # Transição suave de não permitido para permitido
            'permitido': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0.4, 0.6, 1, 1])      # Sobreposição entre 0.4 e 0.6
        })
        self.road = LinguisticVariable('road', np.arange(0, 1.1, 0.1), {
            'obstruida': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0, 0, 0.3, 0.5]),  # Transição suave de obstruída para livre
            'livre': fuzz.trapmf(np.arange(0, 1.1, 0.1), [0.4, 0.6, 1, 1])      # Sobreposição entre 0.4 e 0.6
        })


        # Mantendo o mesmo intervalo para a variável de saída (decisão de ultrapassagem)
        self.overtake_decision = LinguisticVariable('overtake_decision', np.arange(0, 1.1, 0.1), {
            'nao': fuzz.trimf(np.arange(0, 1.1, 0.1), [0, 0, 0.5]),
            'sim': fuzz.trimf(np.arange(0, 1.1, 0.1), [0.51, 1, 1])
        })

    def create_rules(self):
         # 1. Se a distância é pequena e a velocidade relativa é alta, e a permissão, pista e visibilidade são favoráveis, então deve ultrapassar
        rule1 = ctrl.Rule(
            self.distance.variable['pequena'] & self.relative_speed.variable['alta'] &
            self.permission.variable['permitido'] & self.road.variable['livre'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 2. Se a distância é pequena e a velocidade relativa é média, e a permissão, pista e visibilidade são favoráveis, então deve ultrapassar
        rule2 = ctrl.Rule(
            self.distance.variable['pequena'] & self.relative_speed.variable['media'] &
            self.permission.variable['permitido'] & self.road.variable['livre'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 3. Se a distância é média e a velocidade relativa é alta, e a permissão, pista e visibilidade são favoráveis, então deve ultrapassar
        rule3 = ctrl.Rule(
            self.distance.variable['media'] & self.relative_speed.variable['alta'] &
            self.permission.variable['permitido'] & self.road.variable['livre'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 4. Se a distância é média e a velocidade relativa é média, e a permissão, pista e visibilidade são favoráveis, então deve ultrapassar
        rule4 = ctrl.Rule(
            self.distance.variable['media'] & self.relative_speed.variable['media'] &
            self.permission.variable['permitido'] & self.road.variable['livre'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 5. Se a distância é grande ou a velocidade relativa é baixa ou a pista está obstruída, não deve ultrapassar
        rule5 = ctrl.Rule(
            self.distance.variable['grande'] | self.relative_speed.variable['baixa'] |
            self.road.variable['obstruida'], self.overtake_decision.variable['nao']
        )

        # 6. Se a visibilidade é ruim, não deve ultrapassar, independentemente das outras condições
        rule6 = ctrl.Rule(
            self.visibility.variable['ruim'], self.overtake_decision.variable['nao']
        )

        # 7. Se a permissão para ultrapassar é negada, não deve ultrapassar
        rule7 = ctrl.Rule(
            self.permission.variable['nao_permitido'], self.overtake_decision.variable['nao']
        )

        # 8. Se a pista está obstruída, não deve ultrapassar
        rule8 = ctrl.Rule(
            self.road.variable['obstruida'], self.overtake_decision.variable['nao']
        )

        # 9. Se a distância é pequena e a velocidade relativa é baixa, e a permissão é dada, deve ultrapassar
        rule9 = ctrl.Rule(
            self.distance.variable['pequena'] & self.relative_speed.variable['baixa'] &
            self.permission.variable['permitido'] & self.road.variable['livre'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 10. Se a distância é grande e a velocidade relativa é alta, não deve ultrapassar
        rule10 = ctrl.Rule(
            self.distance.variable['grande'] & self.relative_speed.variable['alta'],
            self.overtake_decision.variable['nao']
        )

        # 11. Se a distância é média e a velocidade relativa é alta, e a pista e visibilidade são favoráveis, deve ultrapassar
        rule11 = ctrl.Rule(
            self.distance.variable['media'] & self.relative_speed.variable['alta'] &
            self.road.variable['livre'] & self.visibility.variable['boa'],
            self.overtake_decision.variable['sim']
        )

        # 12. Se a distância é grande e a velocidade relativa é média, e a pista está livre, não deve ultrapassar
        rule12 = ctrl.Rule(
            self.distance.variable['grande'] & self.relative_speed.variable['media'] &
            self.road.variable['livre'], self.overtake_decision.variable['nao']
        )

        # 13. Se a velocidade é muito alta, mas a permissão é dada e a visibilidade é boa, deve ultrapassar
        rule13 = ctrl.Rule(
            self.relative_speed.variable['alta'] & self.permission.variable['permitido'] &
            self.visibility.variable['boa'], self.overtake_decision.variable['sim']
        )

        # 14. Se a velocidade é baixa e a visibilidade é ruim, não deve ultrapassar
        rule14 = ctrl.Rule(
            self.relative_speed.variable['baixa'] & self.visibility.variable['ruim'],
            self.overtake_decision.variable['nao']
        )

        # 15. Se a pista está obstruída ou a permissão para ultrapassar é negada, não deve ultrapassar
        rule15 = ctrl.Rule(
            self.road.variable['obstruida'] | self.permission.variable['nao_permitido'],
            self.overtake_decision.variable['nao']
        )

        # Retorna todas as regras criadas
        return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15]

    def simulate(self, inputs):
        try:
            # Cria o sistema de controle e a simulação
            rules = self.create_rules()
            overtake_ctrl = ctrl.ControlSystem(rules)
            overtake_sim = ctrl.ControlSystemSimulation(overtake_ctrl)
            # Passa as entradas
            overtake_sim.input['distance'] = inputs['distance']
            overtake_sim.input['relative_speed'] = inputs['relative_speed']
            overtake_sim.input['permission'] = inputs['permission']
            overtake_sim.input['road'] = inputs['road']
            overtake_sim.input['visibility'] = inputs['visibility']

            # Realiza a computação
            overtake_sim.compute()
            return overtake_sim.output['overtake_decision']
        except ValueError as e:
            print(f"Erro na simulação: {e}")
            print(inputs)
            return 10