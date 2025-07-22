# File: modules/bahan_baku/bahan_service.py
from typing import List, Optional
from .bahan_model import BahanBaku
from .bahan_repository import BahanRepository

class BahanService:
    def __init__(self, repository: BahanRepository):
        self.repository = repository

    def get_all_bahan(self) -> List[BahanBaku]:
        return self.repository.get_all()

    def get_bahan_by_id(self, bahan_id: int) -> Optional[BahanBaku]:
        return self.repository.get_by_id(bahan_id)

    def create_bahan(self, nama: str, stok: int, satuan: str) -> BahanBaku:
        bahan = BahanBaku(nama=nama, stok=stok, satuan=satuan)
        return self.repository.create(bahan)

    def update_bahan(self, bahan_id: int, nama: Optional[str] = None, stok: Optional[int] = None, satuan: Optional[str] = None) -> Optional[BahanBaku]:
        bahan = self.repository.get_by_id(bahan_id)
        if not bahan:
            return None
        if nama is not None:
            bahan.nama = nama
        if stok is not None:
            bahan.stok = stok
        if satuan is not None:
            bahan.satuan = satuan
        return self.repository.update(bahan)

    def delete_bahan(self, bahan_id: int) -> bool:
        return self.repository.delete(bahan_id)