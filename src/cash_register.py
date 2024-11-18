import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DB_PATH = os.path.join(DB_DIR, "sistema.db")

class CashRegister:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []


    def open_cash_register(self, amount):
        self.balance += amount
        self.transactions.append({"type": "entrada", "amount": amount})
        self.add_transaction("Abertura de Caixa", amount, "entrada")

    def add_transaction(self, description, amount, transaction_type):
        self.transactions.append({"description": description, "amount": amount, "type": transaction_type})
        if transaction_type == 'entrada':
            self.balance += amount
        elif transaction_type == 'saida':
            self.balance -= amount

        # Salvar transação no banco de dados
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transacoes (descricao, tipo, valor)
                VALUES (?, ?, ?)
            ''', (description, transaction_type, amount))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao salvar transação: {e}")

    def close_cash_register(self):
        return self.balance