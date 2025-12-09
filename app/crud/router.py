from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, selectinload
from typing import List, Any

from app.db.deps import get_db
from app.schemas.auto import generate_schemas
from app.repositories.auto import create_repository
from app.services.auto import create_service
from app.utils.filter_engine import apply_filters
from app.docs.filters_doc import FILTERS_DOC

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
    Генератор *_name полей для всех реляций модели.
    Работает умно: ищет человекочитаемое поле или строковое представление.
    """
    result = instance.__dict__.copy()

    def extract_label(obj):
        # 1. Находим обычные поля с именами
        for field in ["name", "title", "full_name"]:
            if hasattr(obj, field):
                val = getattr(obj, field)
                if val:
                    return val

        # 2. Если есть __str__ — используем
        if obj.__class__.__str__ is not object.__str__:
            try:
                return str(obj)
            except:
                pass

        # 3. Если есть __repr__ — используем его
        if obj.__class__.__repr__ is not object.__repr__:
            try:
                return repr(obj)
            except:
                pass

        # 4. Фолбэк — ID (в крайнем случае)
        return getattr(obj, "id", None)

    # Обходим все relationships модели
    for rel in model.__mapper__.relationships:
        rel_obj = getattr(instance, rel.key, None)
        field_name = f"{rel.key}_name"

        if rel_obj is None:
            result[field_name] = None
        else:
            result[field_name] = extract_label(rel_obj)

    return result



# ============================================================
# CRUD ROUTER
# ============================================================
def crud_router(model: Any, prefix: str | None = None, tags: list[str] | None = None) -> APIRouter:

    #print("INIT ROUTER FOR:", model.__name__)

    if prefix is None:
        prefix = "/" + model.__tablename__

    if tags is None:
        tags = [model.__name__]

    router = APIRouter(prefix=prefix, tags=tags)

    # 4 схемы
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
        description=FILTERS_DOC,
        operation_id=f"{model.__name__}_list"
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

        # Подгружаем все связи
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
            data = fill_names(r, model)
            result.append(out_list_schema.model_validate(data))

        return result

    # ---------------------------------------------------------
    # GET DETAIL
    # ---------------------------------------------------------
    @router.get(
        "/{obj_id}",
        response_model=out_detail_schema,
        operation_id=f"{model.__name__}_detail"
    )
    def get_item(obj_id: int, db: Session = Depends(get_db)):
        obj = service.get(db, obj_id)
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    @router.post(
        "/",
        response_model=out_detail_schema,
        operation_id=f"{model.__name__}_create"
    )
    def create_item(data: create_schema, db: Session = Depends(get_db)):
        obj = service.create(db, data.dict())
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # PATCH
    # ---------------------------------------------------------
    @router.patch(
        "/{obj_id}",
        response_model=out_detail_schema,
        operation_id=f"{model.__name__}_patch"
    )
    def patch_item(obj_id: int, data: patch_schema, db: Session = Depends(get_db)):
        obj = service.patch(db, obj_id, data.dict(exclude_unset=True))
        return out_detail_schema.model_validate(obj, from_attributes=True)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    @router.delete(
        "/{obj_id}",
        operation_id=f"{model.__name__}_delete"
    )
    def delete_item(obj_id: int, db: Session = Depends(get_db)):
        return service.delete(db, obj_id)

    # ============ FIX: уникальные имена функций ===============
    list_items.__name__ = f"{model.__name__}_list_items_fn"
    get_item.__name__ = f"{model.__name__}_get_item_fn"
    create_item.__name__ = f"{model.__name__}_create_item_fn"
    patch_item.__name__ = f"{model.__name__}_patch_item_fn"
    delete_item.__name__ = f"{model.__name__}_delete_item_fn"

    return router

