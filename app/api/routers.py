import pkgutil
import importlib
from fastapi import APIRouter
from sqlalchemy.orm import DeclarativeMeta
from pathlib import Path

from app.crud.router import crud_router


# --------------------------
#   AUTO DETECT SQLALCHEMY MODELS
# --------------------------
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


# --------------------------
#   AUTO DETECT APIRouter IN app/utils
# --------------------------
def include_utils_routers(api: APIRouter, max_depth: int = 2):
    import os

    utils_dir = Path("app/utils").resolve()   # Абсолютный путь к папке utils
    base_package = "app.utils"

    def walk(path: Path, pkg: str, depth: int):
        if depth > max_depth:
            return

        for entry in os.scandir(path):

            # --------------------------
            # 1) Если это python-файл
            # --------------------------
            if entry.is_file() and entry.name.endswith(".py") and entry.name != "__init__.py":
                module_name = entry.name[:-3]
                module_full = f"{pkg}.{module_name}"

                module = importlib.import_module(module_full)

                # Ищем APIRouter
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, APIRouter):
                        api.include_router(attr)

            # --------------------------
            # 2) Если это папка — просто идём внутрь
            #    НЕ пытаться импортировать папку как модуль!
            # --------------------------
            elif entry.is_dir():
                new_pkg = pkg + "." + entry.name  # формируем пакетное имя
                walk(Path(entry.path), new_pkg, depth + 1)

    walk(utils_dir, base_package, 0)

# --------------------------
#   CREATE MAIN ROUTER
# --------------------------
def create_auto_router() -> APIRouter:
    api = APIRouter()

    # 1️⃣ Подключить все APIRouter из app/utils/*
    include_utils_routers(api, max_depth=2)

    # 2️⃣ CRUD-генерация
    for model in load_all_models():
        api.include_router(crud_router(model))

    return api

router = create_auto_router()
