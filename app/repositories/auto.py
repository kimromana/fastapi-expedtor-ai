from app.crud.base import BaseCRUD

def create_repository(model):
    return BaseCRUD(model)
