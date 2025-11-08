# Profiles-Service (Python / FastAPI)

Servicio de gestión de **perfiles de usuario** para el proyecto de microservicios.
- Lenguaje: Python 3.12 + FastAPI
- DB: PostgreSQL
- Mensajería: RabbitMQ (escucha eventos `user.created` y `user.deleted`)
- Exposición: puerto 8086
- Healthcheck: `GET /health`
- OpenAPI: `GET /docs` y `GET /openapi.json`

## Variables de entorno

| Variable | Ejemplo | Descripción |
|---|---|---|---|
| `DB_HOST` | `profiles-db` | Host de Postgres |
| `DB_PORT` | `5432` | Puerto de Postgres |
| `DB_USER` | `profiles_user` | Usuario DB |
| `DB_PASS` | `profiles_pass` | Password DB |
| `DB_NAME` | `profiles` | Nombre de la base |
| `RABBITMQ_HOST` | `rabbitmq` | Host |
| `RABBITMQ_PORT` | `5672` | Puerto |
| `RABBITMQ_USER` | `guest` | Usuario |
| `RABBITMQ_PASS` | `guest` | Password |
| `RABBITMQ_ENABLED` | `true` | Habilita consumer |
| `RABBITMQ_EXCHANGE` | `auth.events` | Exchange fanout/topic de eventos |
| `RABBITMQ_QUEUE` | `profiles.events` | Cola de perfiles |
| `RABBITMQ_ROUTING_KEY_CREATED` | `user.created` | Routing key para usuario creado |
| `RABBITMQ_ROUTING_KEY_DELETED` | `user.deleted` | Routing key para usuario eliminado |

## Endpoints principales

- `GET /health`
- `POST /profiles` (crea o actualiza por `user_id`)
- `GET /profiles/{user_id}`
- `PUT /profiles/{user_id}`
- `DELETE /profiles/{user_id}`

## Ejecutar local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DB_HOST=localhost DB_PORT=5432 DB_USER=postgres DB_PASS=postgres DB_NAME=profiles
uvicorn app.main:app --reload --port 8082
```

## Tests (happy path)
```bash
pytest -q
```

## OpenAPI
FastAPI expone `GET /openapi.json`. Para exportarlo a archivo:
```bash
curl -s http://localhost:8082/openapi.json > docs/openapi.json
```

