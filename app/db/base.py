import os
import pkgutil
import importlib
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ==========================================
# Авто-импорт всех моделей из папки app/models
# ==========================================
models_package = "app.models"
models_path = os.path.join(os.path.dirname(__file__), "..", "models")

for module_info in pkgutil.iter_modules([models_path]):
    module_name = f"{models_package}.{module_info.name}"
    importlib.import_module(module_name)
