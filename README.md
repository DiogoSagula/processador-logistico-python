# Processador de Dados Logísticos (Python)

Script em Python para automatizar a leitura de pedidos em CSV e gerar um relatório consolidado de faturamento e quantidade vendida por produto.

## Problema resolvido

Operações de vendas e logística frequentemente recebem arquivos CSV exportados de sistemas diferentes. O projeto automatiza a leitura, validação, consolidação e geração do relatório, reduzindo tarefas manuais e erros de cálculo.

## Funcionalidades

- Leitura de CSV com `utf-8-sig` e espaços extras;
- Detecção automática de delimitador por vírgula ou ponto e vírgula;
- Aceita preços com ponto ou vírgula decimal;
- Validação de colunas, quantidades e preços;
- Cálculo financeiro com `Decimal`;
- Agrupamento de produtos com dicionários;
- Geração de relatório `.txt` ordenado;
- Interface de linha de comando com `argparse`;
- Testes automatizados com `unittest`.

## Como executar

Requer Python 3.10 ou superior.

```bash
python processador.py --entrada pedidos.csv --saida relatorio_final.txt
```

Os argumentos são opcionais. Sem argumentos, o programa usa `pedidos.csv` e gera `relatorio_final.txt`.

## Formato de entrada

O CSV deve conter as colunas `Produto`, `Quantidade` e `Preco`:

```csv
Produto,Quantidade,Preco
Caixa,2,10.50
Fita,3,2.00
```

O projeto também aceita ponto e vírgula como delimitador e vírgula como separador decimal.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Exemplo de saída

```text
=== Relatório de Fechamento de Produção ===

Faturamento Total: R$ 26.00

Resumo de Materiais Vendidos:
- Caixa: 2 unidades
- Fita: 3 unidades
```

## Tecnologias

- Python 3
- Biblioteca padrão `csv`
- `Decimal` para valores financeiros
- `argparse` para CLI
- `unittest` para testes
- Manipulação de arquivos e estruturas de dados

## Estrutura

```text
.
├── pedidos.csv
├── processador.py
├── README.md
└── tests/
    └── test_processador.py
```
