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
