# ETL FastAPI ↔ PostgreSQL + Dagster

Pipeline prático que demonstra:

1. **Fonte** `source_db` – PostgreSQL com tabela **data** (10 dias de séries 1-minuto).  
2. **API**  FastAPI (`/data/`) isolando o acesso ao banco fonte.  
3. **ETL**  Script Python que consulta a API com **httpx**, agrega em 10 min (pandas) e grava em **target_db** via SQLAlchemy.  
4. **Orquestração (bônus)** Dagster com asset particionado diário, job e schedule (02:00 UTC).

> Testado em Docker ≥ 24 e Docker Compose v2.

---

## Subindo tudo em 3 passos

```bash
# 1 – clone o repositório
git clone https://github.com/FelipeDeMoraes19/etl-fastapi-postgres.git
cd etl-fastapi-postgres    #todos os comandos seguintes partem daqui

# 2 – build & start
docker compose up --build -d

# 3 – acompanhar logs
docker logs -f dagster    
docker logs -f api        
```

## Serviços expostos

| Serviço        | Porta | URL / Acesso                                             | Função                                        |
|----------------|-------|----------------------------------------------------------|------------------------------------------------|
| **FastAPI**    | 8000  | `http://localhost:8000/data/`                            | Exposição da tabela **data** do banco fonte    |
| **Dagster UI** | 3000  | `http://localhost:3000`                                  | Orquestração, assets, jobs, schedules          |
| **source_db**  | 5432  | `postgresql://user:password@localhost:5432/source_db`    | Banco PostgreSQL de origem                     |
| **target_db**  | 5433  | `postgresql://user:password@localhost:5433/target_db`    | Banco PostgreSQL de destino                    |

> Usuário e senha são **`user / password`** para ambos os bancos.

## Populando e criando tabelas

### Banco fonte (`source_db`)
* A tabela **data** é criada e, na primeira vez que o container sobe, recebe
  10 dias de amostras minutas via `db/source.sql`.
* Para repopular manualmente:

```bash
docker exec -it source_db python /app/db/populate_source_db.py
```

### Banco alvo (target_db)
* A tabela signal é criada on-demand pela asset Dagster ou pelo script ETL.

* Para criar manualmente:

```bash
docker exec -it etl python etl/create_tables.py
```

## Executando o ETL

1. Linha de comando

### executa o ETL para um dia específico (YYYY-MM-DD)

```bash
docker exec -it etl python etl/etl_script.py 2024-04-05
```

2. Via Dagster

* Abra `http://localhost:3000.`

* Vá em Assets -> `aggregated_signals` e clique `Materialize`.

* Escolha a partição (`data`) desejada e Launch.

* Acompanhe os logs em `tempo real.`

* A execução agendada (`daily_schedule`) dispara automaticamente às 02:00 UTC todos os dias.

### Verificando dados no destino

```bash
docker exec -it target_db psql -U user -d target_db -c \
"SELECT name, COUNT(*) FROM signal GROUP BY name ORDER BY 1;"
```


## Parar e limpar tudo

```bash
docker compose down   
docker compose down -v       
```