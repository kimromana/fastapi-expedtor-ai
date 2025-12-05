from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, selectinload
from typing import List, Any

from app.db.deps import get_db
from app.schemas.auto import generate_schemas
from app.repositories.auto import create_repository
from app.services.auto import create_service
from app.utils.filter_engine import apply_filters


FILTERS_DOC = """
### 🔍 Универсальная система фильтров (Frontend Guide)

Все фильтры передаются через query-параметры.

---

## 1. Равенство (eq)
Простое сравнение по полю.
Примеры:
- `?name=Алматы`
- `?code=270009`

## 2. Частичный поиск (ILIKE)
Поиск подстроки, регистр не важен.
Примеры:
- `?name=алма`
- `?territory.name=каз`

## 3. Диапазоны (min/max)
Примеры:
- `?id_min=10`
- `?id_max=100`

## 4. Операторы сравнения (__gt, __lt, ...)
- `field__gt=100`
- `field__gte=100`
- `field__lt=500`
- `field__lte=500`
- `field__ne=10`
- `field__in=100,200,300`

## 5. OR-фильтры
Через |
- `?name|code=2700`

## 6. Фильтры по связям
Используется syntax:
- `territory.name=Казахстан`

---

⚙ **Пример**
/station?name=Алма&code__gte=200000&territory.name=Казахстан&id_min=10&id_max=100
"""

# ============================================================
# CLEANER — убираем '' → None
# ============================================================
def clean_instance(obj):
    mapper = obj.__mapper__
    for column in mapper.columns:
        val = getattr(obj, column.key)
        if val == "":
            setattr(obj, column.key, None)
    return obj


# ============================================================
# Генератор *_name полей
# ============================================================
def fill_names(instance, model):
    """
    Добавляет поля вида organization_name, author_name, currency_name и т.д.
    """
    result = instance.__dict__.copy()

    for rel in model.__mapper__.relationships:
        rel_obj = getattr(instance, rel.key, None)
        field_name = f"{rel.key}_name"

        if rel_obj is None:
            result[field_name] = None
            continue

        # если __repr__ переопределён — используем
        if rel_obj.__class__.__repr__ is not object.__repr__:
            result[field_name] = repr(rel_obj)
        else:
            # иначе id объекта
            result[field_name] = getattr(rel_obj, "id", None)

    return result


# ============================================================
# CRUD ROUTER
# ============================================================
def crud_router(model: Any, prefix: str | None = None, tags: list[str] | None = None) -> APIRouter:

    if prefix is None:
        prefix = "/" + model.__tablename__

    if tags is None:
        tags = [model.__name__]

    router = APIRouter(prefix=prefix, tags=tags)

    # 4 схемы: Create, Patch, ListOut, DetailOut
    create_schema, patch_schema, out_list_schema, out_detail_schema = generate_schemas(model)

    repository = create_repository(model)
    service = create_service(repository)

    # ---------------------------------------------------------
    # GET LIST
    # ---------------------------------------------------------
    @router.get(
        "/",
        response_model=List[out_list_schema],
        summary="List items with universal filters",
        description=FILTERS_DOC
    )
    def list_items(
        request: Request,
        db: Session = Depends(get_db),
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
        sort_dir: str = "asc",
    ):
        params = dict(request.query_params)
        reserved = {"limit", "offset", "sort", "sort_dir"}

        filters = {k: v for k, v in params.items() if k not in reserved}

        query = db.query(model)
        query = apply_filters(query, model, filters)

        # Подгружаем ВСЕ отношения — корректно!
        for rel in model.__mapper__.relationships:
            query = query.options(selectinload(getattr(model, rel.key)))

        # Сортировка
        if sort:
            col = getattr(model, sort, None)
            if col is not None:
                query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        rows = query.offset(offset).limit(limit).all()

        result = []
        for r in rows:
            clean_instance(r)
            data = fill_names(r, model)   # ← добавляем *_name
            result.append(out_list_schema.model_validate(data))

        return result

    # ---------------------------------------------------------
    # GET DETAIL
    # ---------------------------------------------------------
    @router.get("/{obj_id}", response_model=out_detail_schema)
    def get_item(obj_id: int, db: Session = Depends(get_db)):
        obj = service.get(db, obj_id)
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    @router.post("/", response_model=out_detail_schema)
    def create_item(data: create_schema, db: Session = Depends(get_db)):
        obj = service.create(db, data.dict())
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # PATCH
    # ---------------------------------------------------------
    @router.patch("/{obj_id}", response_model=out_detail_schema)
    def patch_item(obj_id: int, data: patch_schema, db: Session = Depends(get_db)):
        obj = service.patch(db, obj_id, data.dict(exclude_unset=True))
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    @router.delete("/{obj_id}")
    def delete_item(obj_id: int, db: Session = Depends(get_db)):
        return service.delete(db, obj_id)

    return router
