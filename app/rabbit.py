import json
import threading
import time
import pika
from sqlalchemy.orm import Session
from .config import settings
from .models import Profile
from .db import SessionLocal

def _ensure_profile(session: Session, user_id: str):
    prof = session.get(Profile, user_id)
    if not prof:
        prof = Profile(user_id=user_id)
        session.add(prof)
    return prof

def handle_user_created(payload: dict):
    user_id = str(payload.get("user_id"))
    if not user_id:
        return
    with SessionLocal() as s:
        _ensure_profile(s, user_id)
        s.commit()

def handle_user_deleted(payload: dict):
    user_id = str(payload.get("user_id"))
    if not user_id:
        return
    with SessionLocal() as s:
        obj = s.get(Profile, user_id)
        if obj:
            s.delete(obj)
            s.commit()

def consumer_loop():
    while True:
        try:
            creds = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_pass)
            params = pika.ConnectionParameters(host=settings.rabbitmq_host, port=settings.rabbitmq_port, credentials=creds, heartbeat=30)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
            channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
            channel.queue_bind(queue=settings.rabbitmq_queue, exchange=settings.rabbitmq_exchange, routing_key="#")

            def callback(ch, method, properties, body):
                try:
                    msg = json.loads(body.decode("utf-8"))
                except Exception:
                    msg = {}
                rk = method.routing_key or ""
                if rk == settings.rabbitmq_rk_created:
                    handle_user_created(msg)
                elif rk == settings.rabbitmq_rk_deleted:
                    handle_user_deleted(msg)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=10)
            channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback)
            channel.start_consuming()
        except Exception as e:
            # Retry after short delay
            time.sleep(5)

def start_consumer_background():
    if not settings.rabbitmq_enabled:
        return
    t = threading.Thread(target=consumer_loop, daemon=True, name="rabbit-consumer")
    t.start()
