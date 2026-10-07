import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from processador import calcular_resumo, processar_vendas


class ProcessadorTestCase(unittest.TestCase):
    def test_calcula_faturamento_e_agrupa_produtos(self):
        vendas = [
            {"Produto": "Caixa", "Quantidade": "2", "Preco": "10,50"},
            {"Produto": "Caixa", "Quantidade": "1", "Preco": "10.50"},
            {"Produto": "Fita", "Quantidade": "3", "Preco": "2"},
        ]
        faturamento, resumo = calcular_resumo(vendas)
        self.assertEqual(faturamento, Decimal("34.50"))
        self.assertEqual(resumo, {"Caixa": 3, "Fita": 3})

    def test_processa_csv_com_ponto_e_virgula_e_gera_relatorio(self):
        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            entrada = pasta / "pedidos.csv"
            saida = pasta / "relatorio.txt"
            entrada.write_text(
                "Produto;Quantidade;Preco\nParafuso;4;1,25\n",
                encoding="utf-8",
            )
            processar_vendas(entrada, saida)
            relatorio = saida.read_text(encoding="utf-8")
            self.assertIn("R$ 5.00", relatorio)
            self.assertIn("Parafuso: 4 unidades", relatorio)

    def test_rejeita_coluna_obrigatoria_ausente(self):
        with self.assertRaises(ValueError):
            calcular_resumo([{"Produto": "Caixa", "Quantidade": "2"}])


if __name__ == "__main__":
    unittest.main()
