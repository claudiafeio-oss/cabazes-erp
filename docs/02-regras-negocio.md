# Regras de Negócio

## Regras confirmadas

1. O cabaz final existe em stock como produto acabado.
2. A produção pode ser parcial.
3. A substituição de componentes é permitida.
4. Há controlo por lote e validade.
5. Há múltiplas localizações físicas.
6. Existem mínimos de stock.

## Regras operacionais

- O stock é derivado de movimentos, nunca de edição direta de saldo.
- Se um produto exigir lote, não pode entrar nem ser consumido sem lote.
- Se um produto exigir validade, não pode entrar sem validade.
- Alterações à BOM não afetam ordens de montagem já criadas.
- Substituições devem ficar registadas com produto planeado e produto real usado.
- O consumo sugerido de lotes deve seguir FEFO.
