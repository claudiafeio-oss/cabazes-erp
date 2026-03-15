# Decisoes Operacionais

Este documento fecha decisoes criticas do dominio para permitir modelacao,
migrations e implementacao consistente dos servicos.

## Regras de consumo e validade

1. FEFO e **obrigatorio** para sugestao e consumo quando existe validade.
2. O cabaz final **tem lote proprio** (gerado na ordem de montagem).
3. A validade do cabaz final e **o minimo** das validades dos componentes
   consumidos na montagem.

## Substituicoes

1. Substituicao **apenas por grupo** (substitution_groups).
2. Substituicao livre nao e permitida.
3. O consumo real regista sempre produto planeado e produto real.

## Custos e valorizacao

1. Politica de custo inicial: **custo medio ponderado** por movimentos.
2. Ajustes de inventario devem criar movimentos com custo explicito.

## Cancelamentos e estornos

1. Documentos validados (rececoes, montagens, ajustes) **nao podem ser
   apagados**.
2. O cancelamento e feito por **movimentos de estorno** (reverse moves),
   mantendo a rastreabilidade total.
3. Ordens de montagem confirmadas so podem ser canceladas se **nenhum consumo
   real** tiver sido registado.

## Notas

- Estas decisoes sao a base para o modelo SQLAlchemy, migrations Alembic e
  servicos de dominio.
