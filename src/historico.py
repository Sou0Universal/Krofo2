import sqlite3
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox, QTextEdit, QFormLayout, QLabel

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sistema.db")

class DetalhesFechamentoDialog(QDialog):
    def __init__(self, row_data):
        super().__init__()
        self.setWindowTitle("Detalhes do Fechamento")
        layout = QVBoxLayout(self)

        date, closing_value, opening_value, total_entries, total_exits, observations = row_data

        # Informações do fechamento com layout melhorado
        info_layout = QFormLayout()
        info_layout.addRow("Data:", QLabel(date))
        info_layout.addRow("Valor de Abertura:", QLabel(f"R${opening_value:.2f}"))
        info_layout.addRow("Saldo Final:", QLabel(f"R${closing_value:.2f}"))
        info_layout.addRow("Total de Entradas:", QLabel(f"R${total_entries:.2f}"))
        info_layout.addRow("Total de Saídas:", QLabel(f"R${total_exits:.2f}"))

        layout.addLayout(info_layout)

        # Detalhes das transações
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)

        self.load_transaction_details(date)

    def load_transaction_details(self, date):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Exibir entradas
        cursor.execute("""
            SELECT date, amount, note
            FROM transactions
            WHERE type = 'entrada' AND date LIKE ?
            ORDER BY date
        """, (f"{date}%",))
        entradas = cursor.fetchall()
        details = []
        if entradas:
            details.append("<b>Entradas:</b>")
            for date_time, amount, note in entradas:
                details.append(f"{date_time} - R${amount:.2f} - Entrada")
                if note:
                    details[-1] += f" - {note}"

        # Exibir saídas
        cursor.execute("""
            SELECT date, amount, note
            FROM transactions
            WHERE type = 'saida' AND date LIKE ?
            ORDER BY date
        """, (f"{date}%",))
        saidas = cursor.fetchall()
        if saidas:
            details.append("<b>Saídas:</b>")
            for date_time, amount, note in saidas:
                details.append(f"{date_time} - R${amount:.2f} - Saída")
                if note:
                    details[-1] += f" - {note}"

        # Exibir detalhes dos pedidos
        cursor.execute("""
            SELECT horario, valor_total, forma_pagamento, cliente
            FROM pagamentos
            WHERE horario LIKE ?
            ORDER BY horario
        """, (f"{date}%",))
        pedidos = cursor.fetchall()
        if pedidos:
            details.append("<b>Pedidos:</b>")
            for horario, valor_total, forma_pagamento, cliente in pedidos:
                descricao = f"Pedido - {forma_pagamento} - {cliente}"
                details.append(f"Hora: {horario} - R${valor_total:.2f} - {descricao}")

        connection.close()

        # Atualiza a área de texto com as transações e pedidos
        self.details_text.setText("\n".join(details))

import sqlite3
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sistema.db")

class HistoricoFechamentosDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histórico de Fechamentos")
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Data", "Valor Final", "Detalhes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.clear_button = QPushButton("Limpar Histórico")
        self.clear_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_button)

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT date, closing_value, opening_value, total_entries, total_exits, observations FROM close_registers WHERE closing_value IS NOT NULL")
        records = cursor.fetchall()
        connection.close()

        self.table.setRowCount(len(records))

        for row_index, row_data in enumerate(records):
            date_item = QTableWidgetItem(row_data[0])
            final_value_item = QTableWidgetItem(f"R${row_data[1]:.2f}")
            details_button = QPushButton("Ver Detalhes")
            details_button.clicked.connect(lambda checked, row=row_data: self.show_details(row))
            self.table.setItem(row_index, 0, date_item)
            self.table.setItem(row_index, 1, final_value_item)
            self.table.setCellWidget(row_index, 2, details_button)

    def show_details(self, row_data):
        detalhes_dialog = DetalhesFechamentoDialog(row_data)
        detalhes_dialog.exec()

    def clear_history(self):
        confirmation = QMessageBox.question(self, "Confirmar Limpeza", "Tem certeza de que deseja limpar o histórico de fechamentos? Esta ação não pode ser desfeita.",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM close_registers")  # Limpa o histórico de fechamentos
            cursor.execute("DELETE FROM transactions")  # Limpa as transações também
            connection.commit()
            connection.close()

            self.load_data()
            QMessageBox.information(self, "Histórico Limpo", "O histórico foi limpo com sucesso.")


