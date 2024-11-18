import os

caminho_completo = os.getcwd()
print(caminho_completo)

def get_button_data():
    return {
        "PRINCIPAL": [
            ("Abertura e\nFechamento\nde Caixa",  "C:/krofo/icon/caixa.ico", "handle_caixa", "button-caixa"),
            ("Adicionar Pedido", "C:/krofo/icon/pedido.ico", "open_adicionar_pedido", "button-adicionar-pedido"),
            ("Histórico de\nFechamentos", "C:/krofo/icon/historico.ico", "open_historico", "button-historico"),
            ("Relatórios", "C:/krofo/icon/relatorios.ico", "open_tab", "button-relatorios", "Relatórios"),
            ("Alertas", "C:/krofo/icon/alert_icon.ico", "open_tab", "button-alertas", "Alertas"),
            ("Controle de\nOrçamento", "C:/krofo/icon/orçamento.ico", "open_tab", "button-orcamento", "Controle de Orçamento"),
            ("Importação e\nExportação", "C:/krofo/icon/import.ico", "open_tab", "button-import", "Importação/Exportação"),
            ("Relatórios de\nFechamento", "C:/krofo/icon/relatorio.ico", "open_tab", "button-relatorio-fechamento", "Relatórios de Fechamento"),
            ("Sair", "C:/krofo/icon/sair.ico", "close_app", "button-sair")
        ],
        "PRODUTOS": [
            ("Produtos", "C:/krofo/icon/produtos.ico", "produtos_callback", "produtos_button"),
            ("Complementos", "C:/krofo/icon/complementos.ico", "complementos_callback", "complementos_button"),
            ("Observações", "C:/krofo/icon/observacoes.ico", "observacoes_callback", "observacoes_button"),
            ("Categorias", "C:/krofo/icon/categorias.ico", "categorias_callback", "categorias_button"),
            ("Tipos e Tamanhos", "C:/krofo/icon/tipos.ico", "tipos_tamanhos_callback", "tipos_tamanhos_button"),
            ("Perguntas", "C:/krofo/icon/perguntas.ico", "perguntas_callback", "perguntas_button"),
            ("Insumos", "C:/krofo/icon/insumos.ico", "insumos_callback", "insumos_button"),
            ("Alterar Estoque\nem Lote", "C:/krofo/icon/alterar_estoque.ico", "alterar_estoque_lote_callback", "alterar_estoque_lote_button"),
            ("Alterar Estoque\ncom NFe", "C:/krofo/icon/alterar_estoque_nfe.ico", "alterar_estoque_nfe_callback", "alterar_estoque_nfe_button"),
            ("Histórico de\nEntradas e Saídas", "C:/krofo/icon/historico_entradas.ico", "historico_entradas_saidas_callback", "historico_entradas_saidas_button"),
            ("Posição por Data", "C:/krofo/icon/posicao.ico", "posicao_data_callback", "posicao_data_button"),
            ("Promoções", "C:/krofo/icon/promocoes.ico", "promocoes_callback", "promocoes_button"),
            ("Histórico de\nItens Vendidos", "C:/krofo/icon/historico_itens.ico", "historico_itens_vendidos_callback", "historico_itens_vendidos_button")
        ],
        "FINANCEIRO": [
            ("9", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-9", "9"),
            ("10", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-10", "10"),
            ("11", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-11", "11"),
            ("12", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-12", "12"),
            ("13", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-13", "13"),
            ("14", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-14", "14"),
            ("15", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-15", "15"),
            ("16", "C:/krofo/icon/busca.ico", "open_tab", "button-financeiro-16", "16")
        ],
        "CONFIGURAÇÕES": [
            ("modo dark", "C:/krofo/icon/dark.ico", "toggle_dark_mode", "button-config-dark"),
            ("18", "C:/krofo/icon/busca.ico", "open_tab", "button-config-18", "18"),
            ("19", "C:/krofo/icon/busca.ico", "open_tab", "button-config-19", "19"),
            ("20", "C:/krofo/icon/busca.ico", "open_tab", "button-config-20", "20"),
            ("21", "C:/krofo/icon/busca.ico", "open_tab", "button-config-21", "21"),
            ("22", "C:/krofo/icon/busca.ico", "open_tab", "button-config-22", "22"),
            ("23", "C:/krofo/icon/busca.ico", "open_tab", "button-config-23", "23"),
            ("24", "C:/krofo/icon/busca.ico", "open_tab", "button-config-24", "24")
        ],
        "APPS": [
            ("25", "C:/krofo/icon/busca.ico", "open_tab", "button-app-25", "25"),
            ("26", "C:/krofo/icon/busca.ico", "open_tab", "button-app-26", "26"),
            ("27", "C:/krofo/icon/busca.ico", "open_tab", "button-app-27", "27"),
            ("28", "C:/krofo/icon/busca.ico", "open_tab", "button-app-28", "28"),
            ("29", "C:/krofo/icon/busca.ico", "open_tab", "button-app-29", "29"),
            ("30", "C:/krofo/icon/busca.ico", "open_tab", "button-app-30", "30"),
            ("31", "C:/krofo/icon/busca.ico", "open_tab", "button-app-31", "31"),
            ("32","C:/krofo/icon/busca.ico", "open_tab", "button-app-32", "32")
        ],
    }