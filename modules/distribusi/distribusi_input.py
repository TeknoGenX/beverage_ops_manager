from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# modules/distribusi/distribusi_input.py


@dataclass
class DistribusiInput:
    tanggal: datetime
    kode_distribusi: str
    kode_produk: str
    jumlah: int
    tujuan: str
    keterangan: Optional[str] = None

class DistribusiInputManager:
    def __init__(self):
        self.inputs: List[DistribusiInput] = []

    def tambah_input(self, distribusi_input: DistribusiInput):
        self.inputs.append(distribusi_input)

    def get_all_inputs(self) -> List[DistribusiInput]:
        return self.inputs

    def cari_berdasarkan_kode(self, kode_distribusi: str) -> Optional[DistribusiInput]:
        for inp in self.inputs:
            if inp.kode_distribusi == kode_distribusi:
                return inp
        return None

    def hapus_input(self, kode_distribusi: str) -> bool:
        for i, inp in enumerate(self.inputs):
            if inp.kode_distribusi == kode_distribusi:
                del self.inputs[i]
                return True
        return False

# Contoh penggunaan
if __name__ == "__main__":
    manager = DistribusiInputManager()
    input1 = DistribusiInput(
        tanggal=datetime.now(),
        kode_distribusi="D001",
        kode_produk="P001",
        jumlah=100,
        tujuan="Gudang A",
        keterangan="Pengiriman awal"
    )
    manager.tambah_input(input1)
    print(manager.get_all_inputs())