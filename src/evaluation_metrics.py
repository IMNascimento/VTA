import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

class EvaluationMetrics:
    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

    def evaluate(self):
        # Limpeza e transformação dos dados
        # Convertendo as predições contínuas para valores binários (0 ou 1) com base em um threshold de 0.5
        y_pred_binario = [1 if pred >= 0.5 else 0 for pred in self.y_pred]
        y_true_binario = [int(val) for val in self.y_true]  # Garantir que o y_true esteja em formato binário
        
        # Calcula a matriz de confusão
        cm = confusion_matrix(y_true_binario, y_pred_binario)
        
        # Calcula as métricas de avaliação
        accuracy = accuracy_score(y_true_binario, y_pred_binario)
        precision = precision_score(y_true_binario, y_pred_binario, average='binary')
        recall = recall_score(y_true_binario, y_pred_binario, average='binary')
        f1 = f1_score(y_true_binario, y_pred_binario, average='binary')
        
        # Exibe os resultados
        print("Matriz de Confusão:")
        print(cm)
        print(f"Acurácia: {accuracy:.2f}")
        print(f"Precisão: {precision:.2f}")
        print(f"Sensibilidade (Recall): {recall:.2f}")
        print(f"F1-Score: {f1:.2f}")
        
        # Gerar o gráfico da matriz de confusão
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Não', 'Sim'], yticklabels=['Não', 'Sim'])
        plt.title('Matriz de Confusão')
        plt.xlabel('Predito')
        plt.ylabel('Real')
        plt.show()

        return cm, accuracy, precision, recall, f1