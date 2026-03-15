# Fluxos Operacionais

## 1. Compra e receção

1. Criar encomenda a fornecedor
2. Confirmar encomenda
3. Receber parcial ou total
4. Registar lote, validade e localização
5. Validar receção (lote/validade obrigatórios quando aplicável)
6. Gerar movimentos de stock

## 2. Montagem de cabazes

1. Criar ordem de montagem
2. Copiar BOM ativa para snapshot da ordem
3. Validar disponibilidade
4. Registar lotes consumidos e eventuais substituições (FEFO quando há validade)
5. Registar quantidade efetivamente produzida
6. Calcular validade do cabaz final (mínimo das validades consumidas)
7. Gerar movimentos de consumo e produção

## 3. Inventário e ajuste

1. Selecionar localização
2. Introduzir contagem real por produto/lote
3. Comparar com saldo do sistema
4. Validar diferenças
5. Gerar movimentos de ajuste
