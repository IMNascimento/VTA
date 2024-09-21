import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

class EvaluationMetrics:
    def __init__(self, y_true, y_pred):
        self._y_true = y_true
        self._y_pred = y_pred

    def evaluate(self):
        """
        Avalia as predições em relação aos valores verdadeiros utilizando várias métricas.
        Converte as predições contínuas para binárias e exibe a matriz de confusão, acurácia, precisão, recall e F1-score.
        
        :return: Matriz de confusão, acurácia, precisão, recall, e F1-score.
        """
        # Limpeza e transformação dos dados
        # Convertendo as predições contínuas para valores binários (0 ou 1) com base em um threshold de 0.5
        y_pred_binary = [1 if pred >= 0.5 else 0 for pred in self._y_pred]
        y_true_binary = [int(val) for val in self._y_true]  # Garantir que o y_true esteja em formato binário
        
        # Calcula a matriz de confusão
        cm = confusion_matrix(y_true_binary, y_pred_binary)
        
        # Calcula as métricas de avaliação
        accuracy = accuracy_score(y_true_binary, y_pred_binary)
        precision = precision_score(y_true_binary, y_pred_binary, average='binary')
        recall = recall_score(y_true_binary, y_pred_binary, average='binary')
        f1 = f1_score(y_true_binary, y_pred_binary, average='binary')
        
        # Exibe os resultados
        print("Confusion Matrix:")
        print(cm)
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1-Score: {f1:.2f}")
        
        # Gerar o gráfico da matriz de confusão
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Não', 'Sim'], yticklabels=['Não', 'Sim'])
        plt.title('Matriz de Confusão')
        plt.xlabel('Predito')
        plt.ylabel('Real')
        plt.show()

        return cm, accuracy, precision, recall, f1