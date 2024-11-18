import sqlite3
import os

def create_database():
    db_path = os.path.join(os.path.dirname(__file__),"sistema.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS close_registers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            opening_value REAL,
            closing_value REAL,
            total_entries REAL,
            total_exits REAL,
            observations TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT,
            cliente_telefone TEXT,
            data TEXT,
            horario TEXT,
            valor_total REAL,
            status TEXT,
            total REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            produto TEXT,
            quantidade INTEGER,
            preco REAL,
            subtotal REAL,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            amount REAL,
            note TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            saldo_final REAL,
            observacao TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT,
            category TEXT,
            description TEXT,
            sale_price REAL,
            cost_price REAL,
            stock_quantity INTEGER,
            unit TEXT,
            sku TEXT,
            barcode TEXT,
            tags TEXT,
            supplier TEXT,
            expiry_date TEXT,
            location TEXT,
            image_data BLOB
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY(product_id) REFERENCES Products(product_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            data TEXT,
            horario TEXT,
            valor_total REAL,
            forma_pagamento TEXT,
            valor_recebido REAL,
            troco REAL
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
