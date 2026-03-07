# Cabazes ERP

Aplicação web interna para gestão operacional de cabazes, acessível por browser, focada em:

- produtos e embalagens
- fornecedores e compras
- lotes e validade
- stock por localização
- ordens de montagem de cabazes
- substituição controlada de componentes
- inventários, ajustes e rastreabilidade

## Stack prevista

- Backend: FastAPI + SQLAlchemy + Alembic + PostgreSQL
- Frontend: Next.js + TypeScript
- Infra: Docker Compose + Nginx (mais tarde)

## Estrutura do projeto

- `backend/` API e regras de negócio
- `frontend/` interface interna por browser
- `docs/` documentação funcional e técnica
- `database/` esquema, seeds e diagramas
- `scripts/` utilitários de desenvolvimento

## Roadmap inicial

1. Fundação do projeto
2. Core de stock
3. Compras e receções
4. BOM de cabazes
5. Ordens de montagem
6. Inventário e ajustes
7. Dashboards e alertas

## Arranque local

```bash
cp .env.example .env
docker compose up --build
```

## Notas

Este repositório nasce como monorepo. Sim, porque separar tudo logo de início é uma daquelas ideias que parecem sofisticadas até começarem a atrapalhar o trabalho real.
