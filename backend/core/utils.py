from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def get_or_create(db, model, defaults=None, **filters):
    instance = db.query(model).filter_by(**filters).first()
    if instance:
        return instance, False

    params = {**filters, **(defaults or {})}
    instance = model(**params)
    db.add(instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        instance = db.query(model).filter_by(**filters).first()
        return instance, False

    db.refresh(instance)
    return instance, True

def check_users_limit(client):
    if client.users_limit and client.users_count >= client.users_limit:
        raise HTTPException(403, "User limit reached")

def check_portfolios_limit(client, user):
    if client.user_portfolios_limit and user.portfolios_count >= client.user_portfolios_limit:
        raise HTTPException(403, f"Portfolio limit reached for user {user.external_id}")

def consume_api_request(client, db):
    if client.api_requests_limit is None:
        return
    if client.api_requests_remaining is None:
        client.api_requests_remaining = client.api_requests_limit
    if client.api_requests_remaining <= 0:
        raise HTTPException(429, "Daily API request limit reached")
    client.api_requests_remaining -= 1
    db.commit()