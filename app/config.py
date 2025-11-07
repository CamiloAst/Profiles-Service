from pydantic import BaseModel
import os

class Settings(BaseModel):
    db_host: str = os.getenv("DB_HOST", "profiles-db")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_user: str = os.getenv("DB_USER", "profiles_user")
    db_pass: str = os.getenv("DB_PASS", "profiles_pass")
    db_name: str = os.getenv("DB_NAME", "profiles")

    rabbitmq_enabled: bool = os.getenv("RABBITMQ_ENABLED", "true").lower() == "true"
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbitmq_user: str = os.getenv("RABBITMQ_USER", "guest")
    rabbitmq_pass: str = os.getenv("RABBITMQ_PASS", "guest")
    rabbitmq_exchange: str = os.getenv("RABBITMQ_EXCHANGE", "auth.events")
    rabbitmq_queue: str = os.getenv("RABBITMQ_QUEUE", "profiles.events")
    rabbitmq_rk_created: str = os.getenv("RABBITMQ_ROUTING_KEY_CREATED", "user.created")
    rabbitmq_rk_deleted: str = os.getenv("RABBITMQ_ROUTING_KEY_DELETED", "user.deleted")

settings = Settings()
