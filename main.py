from src.data_generator import TestDataGenerator
from src.vehicle_over_system import VehicleOvertakeSystem
from src.evaluation_metrics import EvaluationMetrics


# Criando o sistema de controle de ultrapassagem
#sistema_ultrapassagem = VehicleOvertakeSystem()

# Simulando uma entrada
#inputs = {
#    'distancia': 130,
#    'velocidade_relativa': 80,
#    'permissao': 1,
#    'pista': 1,
#    'visibilidade': 1
#}

# Realizando a simulação
#resultado = sistema_ultrapassagem.simulate(inputs)
#print(f"Decisão de ultrapassagem: {resultado:.2f}")

# Gerando e salvando gráficos das variáveis como PNG
#sistema_ultrapassagem.distancia.plot(input_value=inputs['distancia'])
#istema_ultrapassagem.velocidade_relativa.plot(input_value=inputs['velocidade_relativa'])
#sistema_ultrapassagem.permissao.plot(input_value=inputs['permissao'])
#sistema_ultrapassagem.pista.plot(input_value=inputs['pista'])
#sistema_ultrapassagem.visibilidade.plot(input_value=inputs['visibilidade'])


# Criar o gerador de dados
gerador = TestDataGenerator(quantidade=800)

# Gerar os dados de teste
dados_teste = gerador.gerar_dados_de_teste()

# Salvar os dados de teste não balanceados
dados_teste.to_csv('dados_de_teste_nao_balanceados.csv', index=False)

# Balancear os dados usando undersampling
dados_balanceados = gerador.balancear_dados(metodo="undersample")
dados_balanceados.to_csv('dados_de_teste_balanceados.csv', index=False)

gerador = TestDataGenerator(caminho_csv='dados_de_teste_balanceados.csv')
dados_balanceados= gerador.carregar_dados_csv()

# Criando o sistema de controle de ultrapassagem
sistema_ultrapassagem = VehicleOvertakeSystem()

# Realizando a simulação para os dados balanceados
resultados = []
for _, row in dados_balanceados.iterrows():
    inputs = {
        'distancia': row['distancia'],
        'velocidade_relativa': row['velocidade_relativa'],
        'permissao': row['permissao'],
        'pista': row['pista'],
        'visibilidade': row['visibilidade']
    }
    
    # Realiza a simulação
    resultado = sistema_ultrapassagem.simulate(inputs)
    resultados.append(resultado)

# Avaliação dos resultados usando os dados balanceados
validacao = EvaluationMetrics(dados_balanceados['target'], resultados)
validacao.evaluate()