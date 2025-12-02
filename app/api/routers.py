import pkgutil
import importlib
from fastapi import APIRouter
from sqlalchemy.orm import DeclarativeMeta

from app.crud.router import crud_router
from .dirs import router as dirs_router


def is_model(obj) -> bool:
    return (
        isinstance(obj, DeclarativeMeta)
        and hasattr(obj, "__tablename__")
        and obj.__dict__.get("__abstract__", False) is False
    )


def load_all_models():
    import app.models as models_pkg
    models = []

    for _, module_name, _ in pkgutil.iter_modules(models_pkg.__path__):
        module = importlib.import_module(f"{models_pkg.__name__}.{module_name}")

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if is_model(attr):
                models.append(attr)

    return models


def create_auto_router() -> APIRouter:
    api = APIRouter()

    api.include_router(dirs_router)

    for model in load_all_models():
        api.include_router(crud_router(model))

    return api


router = create_auto_router()
