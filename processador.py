"""Processamento de pedidos logísticos e geração de relatório."""

from __future__ import annotations

import argparse
import csv
import logging
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

LOGGER = logging.getLogger(__name__)
COLUNAS_OBRIGATORIAS = {"Produto", "Quantidade", "Preco"}


def detectar_delimitador(primeira_linha: str) -> str:
    """Detecta o delimitador mais provável de um arquivo CSV."""
    return ";" if primeira_linha.count(";") > primeira_linha.count(",") else ","


def converter_decimal(valor: str) -> Decimal:
    """Converte valores monetários brasileiros ou internacionais para Decimal."""
    normalizado = valor.strip().replace("R$", "").replace(" ", "")
    if "," in normalizado and "." in normalizado:
        normalizado = normalizado.replace(".", "").replace(",", ".")
    else:
        normalizado = normalizado.replace(",", ".")
    try:
        return Decimal(normalizado)
    except InvalidOperation as exc:
        raise ValueError(f"Preço inválido: {valor!r}") from exc


def ler_vendas(arquivo_entrada: Path) -> list[dict[str, str]]:
    """Lê as vendas do CSV e valida as colunas obrigatórias."""
    try:
        with arquivo_entrada.open("r", encoding="utf-8-sig", newline="") as arquivo:
            primeira_linha = arquivo.readline()
            if not primeira_linha:
                raise ValueError("O arquivo CSV está vazio.")
            arquivo.seek(0)
            leitor = csv.DictReader(
                arquivo,
                delimiter=detectar_delimitador(primeira_linha),
                skipinitialspace=True,
            )
            colunas = set(leitor.fieldnames or [])
            ausentes = COLUNAS_OBRIGATORIAS - colunas
            if ausentes:
                raise ValueError(
                    "Colunas obrigatórias ausentes: " + ", ".join(sorted(ausentes))
                )
            return list(leitor)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_entrada}") from exc


def calcular_resumo(vendas: Iterable[dict[str, str]]) -> tuple[Decimal, dict[str, int]]:
    """Calcula o faturamento e a quantidade total por produto."""
    faturamento_total = Decimal("0.00")
    vendas_por_produto: dict[str, int] = defaultdict(int)

    for numero_linha, venda in enumerate(vendas, start=2):
        produto = (venda.get("Produto") or "").strip()
        if not produto:
            raise ValueError(f"Produto vazio na linha {numero_linha}.")
        try:
            quantidade = int((venda.get("Quantidade") or "").strip())
        except ValueError as exc:
            raise ValueError(f"Quantidade inválida na linha {numero_linha}.") from exc
        if quantidade < 0:
            raise ValueError(f"Quantidade negativa na linha {numero_linha}.")
        try:
            preco = converter_decimal(venda.get("Preco") or "")
        except ValueError as exc:
            raise ValueError(f"{exc} na linha {numero_linha}.") from exc
        faturamento_total += quantidade * preco
        vendas_por_produto[produto] += quantidade

    return faturamento_total, dict(vendas_por_produto)


def gerar_relatorio(
    arquivo_saida: Path, faturamento_total: Decimal, vendas_por_produto: dict[str, int]
) -> None:
    """Grava o relatório consolidado em arquivo de texto."""
    with arquivo_saida.open("w", encoding="utf-8") as arquivo:
        arquivo.write("=== Relatório de Fechamento de Produção ===\n\n")
        arquivo.write(f"Faturamento Total: R$ {faturamento_total:.2f}\n\n")
        arquivo.write("Resumo de Materiais Vendidos:\n")
        for produto, quantidade in sorted(vendas_por_produto.items()):
            arquivo.write(f"- {produto}: {quantidade} unidades\n")


def processar_vendas(arquivo_entrada: str | Path, arquivo_saida: str | Path) -> tuple[Decimal, dict[str, int]]:
    """Processa um CSV e gera seu relatório consolidado."""
    entrada = Path(arquivo_entrada)
    saida = Path(arquivo_saida)
    faturamento, resumo = calcular_resumo(ler_vendas(entrada))
    gerar_relatorio(saida, faturamento, resumo)
    LOGGER.info("Relatório gerado em %s", saida)
    return faturamento, resumo


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Processa pedidos e gera relatório logístico.")
    parser.add_argument("--entrada", default="pedidos.csv", help="Arquivo CSV de entrada.")
    parser.add_argument("--saida", default="relatorio_final.txt", help="Arquivo TXT de saída.")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = criar_parser().parse_args()
    try:
        processar_vendas(args.entrada, args.saida)
    except (FileNotFoundError, ValueError) as exc:
        LOGGER.error("%s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
