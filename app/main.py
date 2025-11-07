from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from .db import engine, Base, SessionLocal
from .models import Profile
from .schemas import ProfileIn, ProfileOut
from .rabbit import start_consumer_background

app = FastAPI(title="Profiles Service", version="1.0.0")

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    start_consumer_background()

@app.get("/health")
def health():
    return {"status": "UP"}

@app.post("/profiles", response_model=ProfileOut, status_code=201)
def upsert_profile(user_id: str, payload: ProfileIn):
    with SessionLocal() as s:
        obj = s.get(Profile, user_id)
        if not obj:
            obj = Profile(user_id=user_id)
            s.add(obj)
        # Actualizar campos
        for field, value in payload.model_dump(exclude_unset=True).items():
            if field == "social_links" and value is not None:
                # Guardar como JSON string
                import json
                setattr(obj, field, json.dumps(value))
            else:
                setattr(obj, field, value)
        s.commit()
        s.refresh(obj)
        # Convertir social_links a dict si aplica
        import json
        sl = None
        if obj.social_links:
            try:
                sl = json.loads(obj.social_links)
            except Exception:
                sl = None
        return ProfileOut(
            user_id=obj.user_id,
            nickname=obj.nickname,
            homepage_url=obj.homepage_url,
            public_contact=obj.public_contact,
            address=obj.address,
            bio=obj.bio,
            organization=obj.organization,
            country=obj.country,
            social_links=sl
        )

@app.get("/profiles/{user_id}", response_model=ProfileOut)
def get_profile(user_id: str):
    with SessionLocal() as s:
        obj = s.get(Profile, user_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Profile not found")
        import json
        sl = None
        if obj.social_links:
            try:
                sl = json.loads(obj.social_links)
            except Exception:
                sl = None
        return ProfileOut(
            user_id=obj.user_id,
            nickname=obj.nickname,
            homepage_url=obj.homepage_url,
            public_contact=obj.public_contact,
            address=obj.address,
            bio=obj.bio,
            organization=obj.organization,
            country=obj.country,
            social_links=sl
        )

@app.put("/profiles/{user_id}", response_model=ProfileOut)
def update_profile(user_id: str, payload: ProfileIn):
    return upsert_profile(user_id=user_id, payload=payload)

@app.delete("/profiles/{user_id}", status_code=204)
def delete_profile(user_id: str):
    with SessionLocal() as s:
        obj = s.get(Profile, user_id)
        if not obj:
            return JSONResponse(status_code=204, content=None)
        s.delete(obj)
        s.commit()
        return JSONResponse(status_code=204, content=None)
