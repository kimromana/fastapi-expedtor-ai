from typing import Type, Dict, Any, Optional, List
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.crud.filters import apply_filters


class BaseCRUD:
    def __init__(self, model: Type):
        self.model = model

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------
    def get_list(
        self,
        db: Session,
        limit: int = 100,
        offset: int = 0,
        filters: Dict[str, Any] = None,
        sort: Optional[str] = None,
        sort_dir: str = "asc",
        joins: List[str] = None,
    ):
        query = db.query(self.model)

        # ---------------- JOIN LOAD -----------------
        if joins:
            for rel in joins:
                attr = getattr(self.model, rel, None)
                if isinstance(attr, InstrumentedAttribute):
                    query = query.options(joinedload(attr))

        # ---------------- FILTERS -----------------
        if filters:
            query = apply_filters(query, self.model, filters)

        # ---------------- SORTING -----------------
        if sort:
            if "." in sort:
                # Example: territory.name
                rel, col = sort.split(".")

                rel_attr = getattr(self.model, rel, None)
                if rel_attr is None:
                    raise ValueError(f"Invalid relation: {rel}")

                related_model = rel_attr.property.mapper.class_

                column = getattr(related_model, col, None)
                if column is None:
                    raise ValueError(f"Invalid related sort field: {sort}")

                query = query.join(rel_attr)
            else:
                # Example: name, code, rate
                column = getattr(self.model, sort, None)
                if column is None:
                    raise ValueError(f"Invalid sort field: {sort}")

            # the key line — use the column
            query = query.order_by(
                desc(column) if sort_dir == "desc" else asc(column)
            )

        return query.offset(offset).limit(limit).all()

    # ---------------------------------------------------------
    # GET ONE
    # ---------------------------------------------------------
    def get(self, db: Session, obj_id: int):
        pk = getattr(self.model, "id", None)
        if pk is None:
            raise Exception(f"Model {self.model.__name__} has no 'id' column")

        obj = db.query(self.model).filter(pk == obj_id).first()
        if not obj:
            raise HTTPException(404, f"{self.model.__name__} not found")

        return obj

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create(self, db: Session, data: dict):
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    # ---------------------------------------------------------
    # PATCH
    # ---------------------------------------------------------
    def patch(self, db: Session, obj_id: int, data: dict):
        obj = self.get(db, obj_id)

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete(self, db: Session, obj_id: int):
        obj = self.get(db, obj_id)
        db.delete(obj)
        db.commit()
        return True
