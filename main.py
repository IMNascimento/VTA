from src.data_generator import TestDataGenerator
from src.vehicle_over_system import VehicleOvertakeSystem
from src.evaluation_metrics import EvaluationMetrics


# Carregando e processando os dados de teste balanceados
generator = TestDataGenerator(csv_path='data/dados_de_teste_balanceados_menor.csv')
balanced_data = generator.load_and_process_data()

# Criação do sistema de controle de ultrapassagem de veículos
overtake_system = VehicleOvertakeSystem()

# Executando a simulação para os dados balanceados
results = []
for _, row in balanced_data.iterrows():
    inputs = {
        'distance': row['distance'],
        'relative_speed': row['relative_speed'],
        'permission': row['permission'],
        'road': row['road'],
        'visibility': row['visibility']
    }
    # Executando a simulação
    result = overtake_system.simulate(inputs)
    results.append(result)

# Avaliando os resultados usando dados balanceados
evaluation = EvaluationMetrics(balanced_data['target'], results)
evaluation.evaluate()

