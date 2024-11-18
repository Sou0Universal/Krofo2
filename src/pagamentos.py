import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "sistema.db")

class Pagamento:
    def __init__(self, valor_total, forma_pagamento, valor_recebido):
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento
        self.valor_recebido = valor_recebido
        self.troco = 0.0

    def calcular_troco(self):
        """Calcula o troco baseado no valor recebido."""
        if self.valor_recebido < self.valor_total:
            raise ValueError("Valor recebido é menor que o valor total.")
        
        self.troco = self.valor_recebido - self.valor_total
        return self.troco

    def registrar_pagamento(self):
        """Registra o pagamento no banco de dados."""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            # Registrar o pagamento realizado
            cursor.execute('''
                INSERT INTO pagamentos (total_value, payment_method, amount_received, change, date)
                VALUES (?, ?, ?, ?, datetime("now"))
            ''', (self.valor_total, self.forma_pagamento, self.valor_recebido, self.troco))

            connection.commit()
            connection.close()
        except Exception as e:
            connection.rollback()
            print(f"Erro ao registrar pagamento: {e}")
            connection.close()

    def gerar_relatorio_pagamento(self):
        """Gera um relatório simples de pagamento."""
        return {
            "valor_total": self.valor_total,
            "forma_pagamento": self.forma_pagamento,
            "valor_recebido": self.valor_recebido,
            "troco": self.troco
        }
