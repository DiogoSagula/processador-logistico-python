import csv

def processar_vendas(arquivo_entrada, arquivo_saida):
    faturamento_total = 0.0
    vendas_por_produto = {}

    try:
        # utf-8-sig remove caracteres invisíveis (BOM) do começo do arquivo
        with open(arquivo_entrada, mode='r', encoding='utf-8-sig') as file:
            # Lemos a primeira linha para descobrir se o separador é vírgula ou ponto-e-vírgula
            primeira_linha = file.readline()
            separador = ';' if ';' in primeira_linha else ','
            
            # Voltamos para o começo do arquivo para ler os dados
            file.seek(0)
            
            leitor = csv.DictReader(file, delimiter=separador, skipinitialspace=True)
            
            for linha in leitor:
                # O skipinitialspace=True já remove os espaços antes das palavras
                produto = linha['Produto']
                quantidade = int(linha['Quantidade'])
                preco = float(linha['Preco'])
                
                total_item = quantidade * preco
                faturamento_total += total_item
                
                if produto in vendas_por_produto:
                    vendas_por_produto[produto] += quantidade
                else:
                    vendas_por_produto[produto] = quantidade

        with open(arquivo_saida, mode='w', encoding='utf-8') as file:
            file.write("=== Relatório de Fechamento de Produção ===\n\n")
            file.write(f"Faturamento Total: R$ {faturamento_total:.2f}\n\n")
            file.write("Resumo de Materiais Vendidos:\n")
            
            for prod, qtd in vendas_por_produto.items():
                file.write(f"- {prod}: {qtd} unidades\n")

        print(f"Sucesso! Relatório gerado em: {arquivo_saida}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    processar_vendas('pedidos.csv', 'relatorio_final.txt')