# Processador de Dados Logísticos (Python)
Script em Python desenvolvido para automatizar a leitura de dados brutos de vendas e gerar relatórios consolidados de faturação.

## O problema que resolve
Em operações logísticas e de vendas, é comum receber dados em planilhas mal formatadas ou exportadas de sistemas antigos (CSV). Fazer o cálculo manual de totais e o agrupamento de materiais consumidos consome tempo e gera erros. Este script resolve o problema ao ler ficheiros CSV de forma resiliente (ignorando marcações invisíveis e aspas indesejadas), calculando o faturamento total e agrupando a quantidade vendida de cada produto num relatório limpo de texto.

## Funcionalidades
- Leitura de ficheiros `.csv` com tratamento de encoding (`utf-8-sig`) e espaços em branco.
- Deteção automática do delimitador (vírgula ou ponto-e-vírgula).
- Cálculo financeiro iterativo linha a linha.
- Agrupamento de itens por chave usando dicionários.
- Exportação automatizada para `.txt`.

## Como executar
1. Certifique-se de ter o Python instalado.
2. Coloque o ficheiro de base de dados no formato CSV (ex: `pedidos.csv`) na mesma pasta do script.
3. Execute o comando no terminal:
   `python processador.py`
4. O resultado será gerado no ficheiro `relatorio_final.txt`.

## Tecnologias
Python 3 · I/O de Ficheiros · Manipulação de Dicionários · Biblioteca `csv`