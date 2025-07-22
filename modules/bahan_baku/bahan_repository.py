from typing import List, Optional
from sqlalchemy.orm import Session
from . import bahan_models, bahan_schemas

class BahanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[bahan_models.BahanBaku]:
        return self.db.query(bahan_models.BahanBaku).all()

    def get_by_id(self, bahan_id: int) -> Optional[bahan_models.BahanBaku]:
        return self.db.query(bahan_models.BahanBaku).filter(bahan_models.BahanBaku.id == bahan_id).first()

    def create(self, bahan: bahan_schemas.BahanBakuCreate) -> bahan_models.BahanBaku:
        db_bahan = bahan_models.BahanBaku(**bahan.dict())
        self.db.add(db_bahan)
        self.db.commit()
        self.db.refresh(db_bahan)
        return db_bahan

    def update(self, bahan_id: int, bahan: bahan_schemas.BahanBakuUpdate) -> Optional[bahan_models.BahanBaku]:
        db_bahan = self.get_by_id(bahan_id)
        if not db_bahan:
            return None
        for key, value in bahan.dict(exclude_unset=True).items():
            setattr(db_bahan, key, value)
        self.db.commit()
        self.db.refresh(db_bahan)
        return db_bahan

    def delete(self, bahan_id: int) -> bool:
        db_bahan = self.get_by_id(bahan_id)
        if not db_bahan:
            return False
        self.db.delete(db_bahan)
        self.db.commit()
        return True