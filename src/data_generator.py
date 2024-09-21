import random
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler


class TestDataGenerator:
    def __init__(self, quantity=None, csv_path=None):
        self._quantity = quantity
        self._csv_path = csv_path
        self._data = None
    
    def generate_data_for_fis(self):
        """
        Gera dados prontos para passar diretamente ao Sistema de Inferência Nebulosa (SIN).
        
        :return: DataFrame com os dados gerados e o target.
        """
        if not self._quantity:
            raise ValueError("Defina a quantidade de dados a serem gerados.")
        
        data = []
        for _ in range(self._quantity):
            distance = random.uniform(1, 50)  # Distância entre 1 e 50 metros
            relative_speed = random.uniform(1, 56)  # Velocidade relativa entre 1 e 56 m/s
            permission = random.uniform(0, 1)  # Permissão (0 a 1)
            road = random.uniform(0, 1)  # Condições da pista (0 a 1)
            visibility = random.uniform(0, 1)  # Visibilidade (0 a 1)
            
            # Definir uma regra simples para o target
            if (distance < 20 and relative_speed > 30 and permission >= 0.5 and road >= 0.5 and visibility >= 0.5) or \
            (20 <= distance <= 30 and 15 < relative_speed < 40 and permission >= 0.5 and road >= 0.5 and visibility >= 0.5) or \
            (distance > 30 and relative_speed > 40 and permission >= 0.5 and road >= 0.5 and visibility >= 0.5):
                target = 1  # Deve ultrapassar
            else:
                target = 0  # Não deve ultrapassar
            
            data.append({
                'distance': round(distance, 2),
                'relative_speed': round(relative_speed, 2),
                'permission': round(permission, 2),
                'road': round(road, 2),
                'visibility': round(visibility, 2),
                'target': target  # 1 para ultrapassagem, 0 para não
            })
        
        self._data = pd.DataFrame(data)
        return self._data

    def generate_complete_vehicle_data(self):
        """
        Gera dados simulando um veículo com timestamp inicial, distância inicial, e outras variáveis.
        
        :return: DataFrame com os dados gerados.
        """
        if not self._quantity:
            raise ValueError("Defina a quantidade de dados a serem gerados.")
        
        data = []
        for _ in range(self._quantity):
            current_timestamp = random.randint(100000, 200000)
            next_timestamp = current_timestamp + random.randint(1, 5)  # Tempo depois
            initial_distance = random.uniform(1, 50)  # Distância inicial (em metros)
            final_distance = random.uniform(1, 50)  # Distância final (em metros)
            speed = random.uniform(10, 30)  # Velocidade do carro (em m/s)
            road = random.uniform(0, 1)  # Condições da pista (0 a 1)
            visibility = random.uniform(0, 1)  # Visibilidade (0 a 1)
            
            # Calcula a velocidade do carro à frente
            front_speed = (initial_distance - final_distance) / (next_timestamp - current_timestamp)
            relative_speed = speed - front_speed
            
            permission = random.uniform(0, 1)  # Permissão (0 a 1)

            data.append({
                'current_timestamp': current_timestamp,
                'next_timestamp': next_timestamp,
                'initial_distance': round(initial_distance, 2),
                'final_distance': round(final_distance, 2),
                'speed': round(speed, 2),
                'front_speed': round(front_speed, 2),
                'relative_speed': round(relative_speed, 2),
                'permission': round(permission, 2),
                'road': round(road, 2),
                'visibility': round(visibility, 2)
            })

        self._data = pd.DataFrame(data)
        return self._data

    def generate_simple_vehicle_data(self):
        """
        Gera dados simulando o cenário onde só temos distância do carro à frente e velocidade.
        
        :return: DataFrame com os dados gerados.
        """
        if not self._quantity:
            raise ValueError("Defina a quantidade de dados a serem gerados.")
        
        data = []
        for _ in range(self._quantity):
            distance = random.uniform(1, 50)  # Distância do carro da frente (em metros)
            speed = random.uniform(10, 30)  # Velocidade do carro (em m/s)
            road = random.uniform(0, 1)  # Condições da pista (0 a 1)
            visibility = random.uniform(0, 1)  # Visibilidade (0 a 1)
            permission = random.uniform(0, 1)  # Permissão (0 a 1)
            
            data.append({
                'distance': round(distance, 2),
                'speed': round(speed, 2),
                'permission': round(permission, 2),
                'road': round(road, 2),
                'visibility': round(visibility, 2)
            })

        self._data = pd.DataFrame(data)
        return self._data

    def load_and_process_data(self):
        """
        Carrega dados de um arquivo CSV e processa de acordo com o tipo de dados gerados.
        Pode ser do tipo já pronto para SIN ou do tipo que necessita de processamento.
        
        :return: DataFrame processado, pronto para o SIN.
        """
        if not self._csv_path:
            raise ValueError("Caminho do CSV não fornecido.")
        
        self._data = pd.read_csv(self._csv_path)

        # Verifica se os dados precisam de processamento (ou seja, são do tipo 2 ou 3)
        if 'current_timestamp' in self._data.columns and 'next_timestamp' in self._data.columns:
            # Tipo 2: Processar para obter a velocidade relativa
            self._data['front_speed'] = (self._data['initial_distance'] - self._data['final_distance']) / (self._data['next_timestamp'] - self._data['current_timestamp'])
            self._data['relative_speed'] = self._data['speed'] - self._data['front_speed']
            # Drop unnecessary columns
            self._data = self._data.drop(columns=['current_timestamp', 'next_timestamp', 'initial_distance', 'final_distance', 'front_speed'])
        elif 'distance' in self._data.columns and 'speed' in self._data.columns:
            # Tipo 3: Processar a velocidade relativa com base na distância segura
            self._data['front_speed'] = self._data.apply(
                lambda row: self._calculate_front_vehicle_speed_from_safe_distance(row['distance'], row['speed'] * 3.6), axis=1)
            self._data['relative_speed'] = self._data['speed'] - (self._data['front_speed'] / 3.6)
        
        # Retorna o DataFrame processado
        return self._data

    def balance_data(self, method="undersample"):
        """
        Aplica o balanceamento dos dados utilizando undersampling ou oversampling.
        
        :param method: Método de balanceamento ("undersample" ou "oversample").
        :return: DataFrame balanceado.
        """
        if self._data is None:
            raise ValueError("Os dados de teste ainda não foram gerados ou carregados. Chame 'generate_data_for_fis()' ou 'load_and_process_data()' antes de balancear.")
        
        X = self._data.drop(columns=['target'], errors='ignore')
        y = self._data['target'] if 'target' in self._data.columns else None
        
        if method == "undersample":
            sampler = RandomUnderSampler()
        elif method == "oversample":
            sampler = RandomOverSampler()
        else:
            raise ValueError("Método inválido. Escolha 'undersample' ou 'oversample'.")
        
        X_resampled, y_resampled = sampler.fit_resample(X, y)
        
        # Combinar os dados balanceados novamente em um DataFrame
        df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='target')], axis=1)
        return df_resampled

    def calculate_relative_speed(self, my_car_speed_kmh, front_car_speed_kmh):
        """
        Calcula a velocidade relativa entre o seu carro e o carro da frente.
        
        :param my_car_speed_kmh: Velocidade do seu carro em km/h.
        :param front_car_speed_kmh: Velocidade do carro da frente em km/h.
        :return: Velocidade relativa em m/s.
        """
        # Converte km/h para m/s
        my_car_speed_ms = my_car_speed_kmh * (1000 / 3600)
        front_car_speed_ms = front_car_speed_kmh * (1000 / 3600)
        
        # Calcula a velocidade relativa
        relative_speed_ms = my_car_speed_ms - front_car_speed_ms
        return round(relative_speed_ms, 2)

    def _calculate_front_vehicle_speed_from_safe_distance(self, distance, my_car_speed_kmh):
        """
        Calcula a velocidade estimada do carro da frente com base na distância segura e na velocidade do seu carro.
        
        :param distance: Distância atual entre o seu carro e o carro da frente (em metros).
        :param my_car_speed_kmh: Velocidade do seu carro em km/h.
        :return: Velocidade estimada do carro da frente em km/h.
        """
        # A distância segura é de 5 metros para cada 16 km/h de velocidade
        safe_distance = 5 * (my_car_speed_kmh / 16)
        
        # Se a distância for menor que a distância segura, assumimos que o carro da frente está mais lento
        if distance < safe_distance:
            # Calcula a velocidade estimada do carro da frente com base na fórmula mencionada
            front_car_speed_kmh = (distance * 16) / 5
        else:
            # Se a distância é maior ou igual à distância segura, supomos que o carro da frente está na mesma velocidade
            front_car_speed_kmh = my_car_speed_kmh
        
        return round(front_car_speed_kmh, 2)