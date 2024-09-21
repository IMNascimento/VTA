# Sistema de Controle de Ultrapassagem: Teste e Visualização
Este repositório contém o código-fonte para simular um sistema de controle de ultrapassagem em veículos autônomos utilizando um Sistema de Inferência Nebulosa (SIN). O foco deste projeto está na geração de dados de teste, balanceamento dos dados, simulação e avaliação das decisões de ultrapassagem com base nas variáveis de entrada.

## Estrutura do Repositório
src/data_generator.py: Script para gerar dados de teste para o sistema de inferência nebulosa.
src/vehicle_over_system.py: Script que implementa o sistema de controle de ultrapassagem usando lógica nebulosa.
src/evaluation_metrics.py: Script que avalia os resultados da simulação, calculando métricas de desempenho.
requirements.txt: Arquivo listando todas as dependências necessárias para executar os scripts.

## Pré-requisitos
Para reproduzir os experimentos, você precisará ter o Python 3.8+ instalado em seu ambiente. Recomenda-se utilizar um ambiente virtual para gerenciar as dependências.

## Instalação
Clone este repositório em sua máquina local:

```bash
git clone https://github.com/seuusuario/sistema-ultrapassagem.git
cd sistema-ultrapassagem
```

Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate  # Para Windows
```

Instale as dependências listadas no requirements.txt:

```bash
pip install -r requirements.txt
```

## Executando a Simulação
### Gerando Dados de Teste e Balanceando-os

```python
from src.data_generator import TestDataGenerator

# Criar o gerador de dados
gerador = TestDataGenerator(quantidade=10000)

# Gerar os dados de teste
dados_teste = gerador.gerar_dados_para_sin()

# Balancear os dados usando undersampling
dados_balanceados = gerador.balancear_dados(metodo="undersample")
dados_balanceados.to_csv('dados_de_teste_balanceados.csv', index=False)

# Carregar e processar os dados balanceados
gerador = TestDataGenerator(caminho_csv='dados_de_teste_balanceados.csv')
dados_balanceados = gerador.carregar_dados_e_processar()
```

### Executando o Sistema de Ultrapassagem e Avaliação

```python
from src.vehicle_over_system import VehicleOvertakeSystem
from src.evaluation_metrics import EvaluationMetrics

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
```

### Plotando os Gráficos das Funções de Pertinência

```python
# Plotando as variáveis de entrada e as funções de pertinência

# Simulando uma entrada de exemplo
inputs = {
    'distancia': 50,
    'velocidade_relativa': 56,
    'permissao': 1,
    'pista': 1,
    'visibilidade': 1
}

# Plotando as funções de pertinência das variáveis
sistema_ultrapassagem.distancia.plot(input_value=inputs['distancia'])
sistema_ultrapassagem.velocidade_relativa.plot(input_value=inputs['velocidade_relativa'])
sistema_ultrapassagem.permissao.plot(input_value=inputs['permissao'])
sistema_ultrapassagem.pista.plot(input_value=inputs['pista'])
sistema_ultrapassagem.visibilidade.plot(input_value=inputs['visibilidade'])
```

### Contribuições
Contribuições são bem-vindas! Se você tiver sugestões de melhorias ou encontrar problemas, fique à vontade para abrir uma issue ou enviar um pull request.

### Contato
Para mais informações ou para acesso ao artigo, entre em contato através de igor.muniz@estudante.ufjf.br.