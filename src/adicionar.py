import os
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTextEdit, QFormLayout, QSpinBox, QDoubleSpinBox,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "sistema.db")

class ImportarProdutosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Novo Produto")
        self.setGeometry(300, 300, 500, 600)
        self._setup_ui()

    def _setup_ui(self):
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.code_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Alimentos", "Bebidas", "Limpeza"])
        self.description_input = QTextEdit()
        self.sale_price_input = QDoubleSpinBox(maximum=10000)
        self.cost_price_input = QDoubleSpinBox(maximum=10000)
        self.stock_input = QSpinBox(maximum=1000)
        self.unit_input = QComboBox()
        self.unit_input.addItems(["Unidade", "Kg", "Litro"])
        self.sku_input = QLineEdit()
        self.barcode_input = QLineEdit()
        self.tags_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.expiry_date_input = QLineEdit()
        self.location_input = QLineEdit()

        layout.addRow("Nome do Produto:", self.name_input)
        layout.addRow("Código do Produto:", self.code_input)
        layout.addRow("Categoria:", self.category_input)
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Preço de Venda:", self.sale_price_input)
        layout.addRow("Preço de Custo:", self.cost_price_input)
        layout.addRow("Quantidade em Estoque:", self.stock_input)
        layout.addRow("Unidade de Medida:", self.unit_input)
        layout.addRow("SKU:", self.sku_input)
        layout.addRow("Código de Barras:", self.barcode_input)
        layout.addRow("Tags:", self.tags_input)
        layout.addRow("Fornecedor:", self.supplier_input)
        layout.addRow("Data de Validade:", self.expiry_date_input)
        layout.addRow("Localização no Estoque:", self.location_input)

        self.image_button = QPushButton("Selecionar Imagem")
        self.image_button.clicked.connect(self.select_image)
        layout.addRow("Imagens do Produto:", self.image_button)

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_product)
        layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Limpar Campos")
        self.clear_button.clicked.connect(self.clear_fields)
        layout.addWidget(self.clear_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.image_path = None  # A variável para armazenar o caminho da imagem selecionada

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar Imagem", "", "Images (*.png *.xpm *.jpg)")
        if file_path:
            self.image_path = file_path  # Armazena o caminho da imagem
            QMessageBox.information(self, "Imagem Selecionada", f"Imagem '{file_path}' selecionada.")

    def save_product(self):
        product_data = {
            "name": self.name_input.text(),
            "code": self.code_input.text(),
            "category": self.category_input.currentText(),
            "description": self.description_input.toPlainText(),
            "sale_price": self.sale_price_input.value(),
            "cost_price": self.cost_price_input.value(),
            "stock": self.stock_input.value(),
            "unit": self.unit_input.currentText(),
            "sku": self.sku_input.text(),
            "barcode": self.barcode_input.text(),
            "tags": self.tags_input.text(),
            "supplier": self.supplier_input.text(),
            "expiry_date": self.expiry_date_input.text(),
            "location": self.location_input.text()
        }

        if not product_data["name"]:
            QMessageBox.warning(self, "Erro", "O nome do produto é obrigatório.")
            return

        if self.image_path:
            # Converte o caminho da imagem para dados binários
            with open(self.image_path, "rb") as image_file:
                image_data = image_file.read()
        else:
            image_data = None

        self._save_to_database(product_data, image_data)
        QMessageBox.information(self, "Sucesso", "Produto salvo com sucesso!")
        self.clear_fields()

    def _save_to_database(self, product_data, image_data):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Products (name, code, category, description, sale_price, cost_price, stock_quantity, unit, sku, barcode, tags, supplier, expiry_date, location, image_data)
            VALUES (:name, :code, :category, :description, :sale_price, :cost_price, :stock, :unit, :sku, :barcode, :tags, :supplier, :expiry_date, :location, ?)
        ''', (*product_data.values(), image_data))
        connection.commit()
        connection.close()

    def clear_fields(self):
        self.name_input.clear()
        self.code_input.clear()
        self.description_input.clear()
        self.sale_price_input.setValue(0)
        self.cost_price_input.setValue(0)
        self.stock_input.setValue(0)
        self.sku_input.clear()
        self.barcode_input.clear()
        self.tags_input.clear()
        self.supplier_input.clear()
        self.expiry_date_input.clear()
        self.location_input.clear()
        self.image_path = None  # Limpa o caminho da imagem selecionada


class AdicionarPedidoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Pedido")
        self.setGeometry(300, 300, 400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.product_input = QComboBox()
        self.load_products()

        self.quantity_input = QSpinBox(maximum=1000)

        layout.addWidget(QLabel("Produto:"))
        layout.addWidget(self.product_input)
        layout.addWidget(QLabel("Quantidade:"))
        layout.addWidget(self.quantity_input)

        self.add_button = QPushButton("Adicionar Pedido")
        self.add_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

    def load_products(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT product_id, name FROM Products")
        products = cursor.fetchall()
        connection.close()

        for product_id, name in products:
            self.product_input.addItem(name, product_id)

    def add_order(self):
        product_id = self.product_input.currentData()
        quantity = self.quantity_input.value()
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Orders (product_id, quantity, order_date)
            VALUES (?, ?, ?)
        ''', (product_id, quantity, order_date))
        connection.commit()
        connection.close()

        QMessageBox.information(self, "Sucesso", "Pedido adicionado com sucesso!")
        self.close()
