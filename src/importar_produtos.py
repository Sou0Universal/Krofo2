from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFormLayout, QMessageBox, QScrollArea, QGridLayout, QHBoxLayout,
    QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import sqlite3
import os
from .adicionar import ImportarProdutosWidget  # Arquivo onde adiciona os produtos

# Caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "sistema.db")


class DatabaseHandler:
    """Classe para interagir com o banco de dados de produtos."""
    @staticmethod
    def get_all_products():
        """Recupera todos os produtos do banco de dados."""
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("SELECT product_id, name, stock_quantity, code, sale_price, description, image_data FROM Products")
            products = cursor.fetchall()
            connection.close()
            return products
        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")
            return []

    @staticmethod
    def delete_product(product_id):
        """Remove um produto do banco de dados."""
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Erro ao remover produto: {e}")

    @staticmethod
    def update_product(product_id, updated_data):
        """Atualiza um produto no banco de dados."""
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute(''' 
                UPDATE Products
                SET name = ?, stock_quantity = ?, sale_price = ?, description = ?
                WHERE product_id = ?
            ''', (updated_data['name'], updated_data['stock_quantity'], updated_data['sale_price'],
                  updated_data['description'], product_id))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")


class ProdutosWidget(QWidget):
    """Classe para exibir e gerenciar produtos"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestão de Produtos")
        self.setGeometry(200, 200, 1000, 600)
        self._setup_ui()

    def _setup_ui(self):
        """Configura os componentes da interface"""
        main_layout = QVBoxLayout(self)

        # Layout superior (botão para adicionar novos produtos)
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignRight)

        self.add_product_button = QPushButton("Adicionar Produto")
        self.add_product_button.clicked.connect(self.open_add_product_window)
        self.add_product_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        top_layout.addWidget(self.add_product_button)

        # Scroll Area para exibir os produtos em forma de cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container para os produtos em grid
        self.product_container = QWidget()
        self.product_layout = QGridLayout(self.product_container)

        self.scroll_area.setWidget(self.product_container)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.scroll_area)

        # Carrega e exibe os produtos
        products = DatabaseHandler.get_all_products()  # Recupera todos os produtos do banco de dados
        self.load_products(products)  # Passa os produtos como argumento

    def load_products(self, products):
        # Cria um layout horizontal para os cards
        self.product_layout = QHBoxLayout()  # Layout horizontal para os cards
        self.product_layout.setSpacing(3)  # Espaçamento horizontal entre os cards

        # Scroll area para exibir os cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.product_layout)
        scroll_area.setWidget(container)

        # Exibe os produtos em cards, empilhados horizontalmente
        for product in products:
            product_id, name, stock_quantity, code, sale_price, description, image_data = product

            # Cria o card para o produto
            card = self.create_product_card(product_id, name, stock_quantity, sale_price, description, image_data)

            # Adiciona o card ao layout principal
            self.product_layout.addWidget(card)

            # Separação visual entre os cards (linha vertical)
            separator = QFrame()
            separator.setFrameShape(QFrame.VLine)  # Linha vertical
            separator.setFrameShadow(QFrame.Sunken)
            self.product_layout.addWidget(separator)

        # Adiciona a scroll area diretamente no layout do widget
        self.layout().addWidget(scroll_area)

    def create_product_card(self, product_id, name, stock_quantity, sale_price, description, image_data):
        """Cria um card de produto (horizontal)"""
        card = QWidget()
        card_layout = QVBoxLayout(card)  # Layout vertical dentro do card
        self.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 1px solid #ccc;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        """)

        # Adiciona margem ao redor do card
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(5)  # Espaçamento interno entre os widgets do card

        # Imagem do produto (imagem padrão caso não haja imagem)
        pixmap = QPixmap(100, 100)  # Imagem padrão (caso não tenha a coluna de imagem)
        pixmap.fill(Qt.gray)  # Cor de fundo cinza, caso o produto não tenha imagem

        if image_data:  # Verifica se há dados de imagem
            image = QImage()
            image.loadFromData(image_data)  # Converte os dados BLOB para uma imagem
            pixmap = QPixmap(image)  # Cria o QPixmap a partir da imagem

            # Limita o tamanho da imagem para 100x100 pixels
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Adiciona a imagem ao card
        card_layout.addWidget(image_label)

        # Linha de separação entre a imagem e o texto
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        card_layout.addWidget(separator)

        # Nome do produto
        name_label = QLabel(f"Nome: {name}")
        name_label.setStyleSheet("font-weight: bold;")
        card_layout.addWidget(name_label)

        # Preço de venda e estoque
        price_label = QLabel(f"Preço: R${sale_price:.2f}")
        stock_label = QLabel(f"Estoque: {stock_quantity}")

        # Adiciona o preço e o estoque
        price_layout = QHBoxLayout()
        price_layout.addWidget(price_label)
        price_layout.addWidget(stock_label)

        # Adiciona o layout de preço ao card
        card_layout.addLayout(price_layout)

        # Linha de separação entre os preços e a descrição
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        card_layout.addWidget(separator)

        # Descrição do produto
        description_label = QLabel(f"Descrição: {description}")
        description_label.setWordWrap(True)  # Quebra a linha da descrição para não estourar a largura
        card_layout.addWidget(description_label)

        # Botões de editar e excluir
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(lambda: self.edit_product(product_id))
        delete_button = QPushButton("Excluir")
        delete_button.clicked.connect(lambda: self.delete_product(product_id))

        # Adiciona os botões
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        # Adiciona o layout de botões ao card
        card_layout.addLayout(button_layout)

        return card
    
    def edit_product(self, product_id):
        # Recupera os dados do produto do banco de dados
        query = '''
            SELECT 
                name, stock_quantity, sale_price, description, code, category, 
                cost_price, unit, sku, barcode, tags, supplier, expiry_date, location
            FROM Products WHERE product_id = ?
        '''
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        product_data = cursor.fetchone()
        connection.close()

        if product_data:
            # Desempacota os dados retornados
            (name, stock_quantity, sale_price, description, code, category, cost_price, 
            unit, sku, barcode, tags, supplier, expiry_date, location) = product_data

            # Abre a janela de edição com todos os dados
            self.edit_product_window = EditProductWindow(
                product_id, name, stock_quantity, sale_price, description, 
                code, category, cost_price, unit, sku, barcode, tags, supplier, expiry_date, location, self
            )
            self.edit_product_window.show()
        else:
            QMessageBox.warning(self, "Erro", "Produto não encontrado.")

    def delete_product(self, product_id):
        try:
            # Exclui o produto do banco de dados
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))
            connection.commit()
            connection.close()

            # Após deletar, recarrega a lista de produtos
            self.update_product_list()
            
            QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso!")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao excluir o produto: {str(e)}")

    def update_product_list(self):
        # Aqui você obtém os produtos novamente do banco de dados
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        connection.close()

    def get_product_by_id(self, product_id):
        """Recupera os dados de um produto pelo ID"""
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))
            product = cursor.fetchone()
            connection.close()
            return product
        except Exception as e:
            print(f"Erro ao recuperar o produto: {e}")
            return None

    def open_add_product_window(self):
        """Abre a janela para adicionar produtos"""
        self.add_product_window = ImportarProdutosWidget()  # Remover 'self' como argumento
        self.add_product_window.show()

class EditProductWindow(QWidget):
    """Janela para editar um produto"""
    def __init__(self, product_id, name, stock_quantity, sale_price, description, code, category, cost_price, unit, sku, barcode, tags, supplier, expiry_date, location, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Produto")
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setGeometry(300, 300, 400, 250)
        self.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 10px;")
        self.product_id = product_id
        self._setup_ui(name, stock_quantity, sale_price, description, code, category, cost_price, unit, sku, barcode, tags, supplier, expiry_date, location)
        self.setStyleSheet(open(r"C:/krofo/src/styles.css").read())

    def _setup_ui(self, name, stock_quantity, sale_price, description, code, category, cost_price, unit, sku, barcode, tags, supplier, expiry_date, location):
        """Configura os componentes da janela de edição"""
        layout = QVBoxLayout(self)

        # Layout de formulário para organizar os campos
        form_layout = QFormLayout()

        # Campos de edição
        self.name_input = QLineEdit(name)
        self.stock_input = QLineEdit(str(stock_quantity))
        self.stock_input.setValidator(QIntValidator())  # Aceitar apenas números inteiros
        self.sale_price_input = QLineEdit(str(sale_price))
        self.sale_price_input.setValidator(QDoubleValidator(0.0, 999999.99, 2))  # Aceitar apenas números decimais
        self.cost_price_input = QLineEdit(str(cost_price))
        self.cost_price_input.setValidator(QDoubleValidator(0.0, 999999.99, 2))  # Aceitar apenas números decimais
        self.description_input = QLineEdit(description)
        self.code_input = QLineEdit(code)

        # Carregar categorias do banco de dados
        self.category_input = QComboBox()
        self.load_categories()

        # Unidade (apenas unidades disponíveis no banco de dados)
        self.unit_input = QComboBox()
        self.load_units()

        self.sku_input = QLineEdit(sku)
        self.barcode_input = QLineEdit(barcode)
        self.tags_input = QLineEdit(tags)
        self.supplier_input = QLineEdit(supplier)
        self.expiry_date_input = QLineEdit(expiry_date)
        self.location_input = QLineEdit(location)

        # Adicionando os campos ao layout de formulário
        form_layout.addRow(QLabel("Nome do Produto:"), self.name_input)
        form_layout.addRow(QLabel("Quantidade em Estoque:"), self.stock_input)
        form_layout.addRow(QLabel("Preço de Venda:"), self.sale_price_input)
        form_layout.addRow(QLabel("Descrição:"), self.description_input)
        form_layout.addRow(QLabel("Código:"), self.code_input)
        form_layout.addRow(QLabel("Categoria:"), self.category_input)
        form_layout.addRow(QLabel("Preço de Custo:"), self.cost_price_input)
        form_layout.addRow(QLabel("Unidade:"), self.unit_input)
        form_layout.addRow(QLabel("SKU:"), self.sku_input)
        form_layout.addRow(QLabel("Código de Barras:"), self.barcode_input)
        form_layout.addRow(QLabel("Tags:"), self.tags_input)
        form_layout.addRow(QLabel("Fornecedor:"), self.supplier_input)
        form_layout.addRow(QLabel("Data de Validade:"), self.expiry_date_input)
        form_layout.addRow(QLabel("Localização:"), self.location_input)

        # Botão de salvar
        self.save_button = QPushButton("Salvar Alterações")
        self.save_button.clicked.connect(self.save_edited_product)

        # Layout horizontal para o botão
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.save_button)

        # Adicionando o formulário e o botão ao layout principal
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        # Ajustando o layout principal
        self.setLayout(layout)

    def load_categories(self):
        """Carregar categorias disponíveis no banco de dados"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM Products")
        categories = cursor.fetchall()
        connection.close()

        for category in categories:
            self.category_input.addItem(category[0])

    def load_units(self):
        """Carregar unidades de medida disponíveis no banco de dados"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT unit FROM Products")
        units = cursor.fetchall()
        connection.close()

        for unit in units:
            self.unit_input.addItem(unit[0])

    def save_edited_product(self):
        try:
            # Validar os dados inseridos
            stock_quantity_text = self.stock_input.text()
            sale_price_text = self.sale_price_input.text()
            cost_price_text = self.cost_price_input.text()

            if not stock_quantity_text.isdigit():
                raise ValueError("A quantidade de estoque deve ser um número inteiro.")
            if not sale_price_text.replace(".", "").isdigit():
                raise ValueError("O preço de venda deve ser um número válido.")
            if not cost_price_text.replace(".", "").isdigit():
                raise ValueError("O preço de custo deve ser um número válido.")

            stock_quantity = int(stock_quantity_text)
            sale_price = float(sale_price_text)
            cost_price = float(cost_price_text)

            # Coletar os valores atualizados
            updated_data = {
                "name": self.name_input.text(),
                "code": self.code_input.text(),
                "category": self.category_input.currentText(),
                "description": self.description_input.text(),
                "sale_price": sale_price,
                "cost_price": cost_price,
                "stock_quantity": stock_quantity,
                "unit": self.unit_input.currentText(),
                "sku": self.sku_input.text(),
                "barcode": self.barcode_input.text(),
                "tags": self.tags_input.text(),
                "supplier": self.supplier_input.text(),
                "expiry_date": self.expiry_date_input.text(),
                "location": self.location_input.text(),
            }

            # Salvar no banco de dados
            self.save_product_to_db(updated_data)

            QMessageBox.information(self, "Produto Editado", "Produto editado com sucesso!")
            self.close()

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def save_product_to_db(self, data):
        """Atualiza o produto no banco de dados"""
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()

            cursor.execute('''
                UPDATE Products
                SET name = ?, code = ?, category = ?, description = ?, sale_price = ?,
                    cost_price = ?, stock_quantity = ?, unit = ?, sku = ?, barcode = ?,
                    tags = ?, supplier = ?, expiry_date = ?, location = ?
                WHERE product_id = ?
            ''', (
                data["name"], data["code"], data["category"], data["description"], data["sale_price"],
                data["cost_price"], data["stock_quantity"], data["unit"], data["sku"], data["barcode"],
                data["tags"], data["supplier"], data["expiry_date"], data["location"], self.product_id
            ))

            connection.commit()
            connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar no banco de dados: {str(e)}")
