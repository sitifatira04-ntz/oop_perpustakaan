from abc import ABC, abstractmethod
from datetime import date, timedelta


class PerpustakaanError(Exception):
    """Exception khusus untuk error di aplikasi perpustakaan."""


# =====================================================
# ABSTRACT CLASS
# =====================================================
class Item(ABC):
    """Induk semua koleksi. Tidak boleh dibuat objeknya langsung."""

    total_items = 0  # class variable (dipakai bersama semua objek)

    def __init__(self, kode, judul, tahun):
        if not Item.validasi_kode(kode):
            raise PerpustakaanError(f"Kode '{kode}' tidak valid (min. 3 karakter)")
        self.kode = kode
        self.judul = judul
        self.tahun = tahun
        self.__tersedia = True      # private attribute (encapsulation)
        Item.total_items += 1

    # ----- Property (getter & setter) -----
    @property
    def tersedia(self):
        return self.__tersedia

    @tersedia.setter
    def tersedia(self, nilai):
        if not isinstance(nilai, bool):
            raise ValueError("Status harus bertipe bool (True/False)")
        self.__tersedia = nilai

    # ----- Abstract method: WAJIB di-override child class -----
    @abstractmethod
    def durasi_pinjam(self):
        """Lama peminjaman (hari)."""

    @abstractmethod
    def denda_per_hari(self):
        """Denda keterlambatan per hari (rupiah)."""

    @abstractmethod
    def info_tambahan(self):
        """Keterangan khusus tiap jenis koleksi."""

    # ----- Method biasa -----
    def hitung_denda(self, hari_telat):
        if hari_telat <= 0:
            return 0
        return hari_telat * self.denda_per_hari()

    # ----- Static method -----
    @staticmethod
    def validasi_kode(kode):
        return isinstance(kode, str) and len(kode.strip()) >= 3

    # ----- Class method -----
    @classmethod
    def get_total_items(cls):
        return Item.total_items

    # ----- Magic method -----
    def __str__(self):
        status = "Tersedia" if self.tersedia else "Dipinjam"
        return f"[{self.kode}] {self.judul} ({self.tahun}) | {self.info_tambahan()} | {status}"

    def __eq__(self, other):
        return isinstance(other, Item) and self.kode == other.kode

    def __hash__(self):
        return hash(self.kode)


# =====================================================
# INHERITANCE
# =====================================================
class Buku(Item):
    def __init__(self, kode, judul, tahun, penulis):
        super().__init__(kode, judul, tahun)
        self.penulis = penulis

    def durasi_pinjam(self):            # overriding
        return 7

    def denda_per_hari(self):           # overriding
        return 1000

    def info_tambahan(self):            # overriding
        return f"Buku oleh {self.penulis}"

    @classmethod
    def dari_string(cls, teks):
        """Alternative constructor. Format: kode;judul;tahun;penulis"""
        kode, judul, tahun, penulis = teks.split(";")
        return cls(kode, judul, int(tahun), penulis)


class Majalah(Item):
    def __init__(self, kode, judul, tahun, edisi):
        super().__init__(kode, judul, tahun)
        self.edisi = edisi

    def durasi_pinjam(self):
        return 3

    def denda_per_hari(self):
        return 500

    def info_tambahan(self):
        return f"Majalah edisi {self.edisi}"


class Dvd(Item):
    def __init__(self, kode, judul, tahun, durasi_menit):
        super().__init__(kode, judul, tahun)
        self.durasi_menit = durasi_menit

    def durasi_pinjam(self):
        return 2

    def denda_per_hari(self):
        return 2000

    def info_tambahan(self):
        return f"DVD {self.durasi_menit} menit"


# =====================================================
# COMPOSITION
# =====================================================
class Peminjaman:
    """Satu transaksi pinjam. Peminjaman 'memiliki' sebuah Item."""

    def __init__(self, item, tanggal_pinjam=None):
        self.item = item
        self.tanggal_pinjam = tanggal_pinjam or date.today()
        self.jatuh_tempo = self.tanggal_pinjam + timedelta(days=item.durasi_pinjam())

    def hari_telat(self, tanggal_kembali=None):
        tanggal_kembali = tanggal_kembali or date.today()
        return max(0, (tanggal_kembali - self.jatuh_tempo).days)

    def __str__(self):
        return f"{self.item.judul} (jatuh tempo: {self.jatuh_tempo})"


class Anggota:
    """Anggota 'memiliki' daftar Peminjaman."""

    MAKS_PINJAM = 3      # class variable
    total_anggota = 0    # class variable

    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self.daftar_pinjam = []
        self.__total_denda = 0   # private
        Anggota.total_anggota += 1

    @property
    def total_denda(self):
        return self.__total_denda

    def tambah_denda(self, jumlah):
        if jumlah < 0:
            raise ValueError("Denda tidak boleh negatif")
        self.__total_denda += jumlah

    def bisa_pinjam(self):
        return len(self.daftar_pinjam) < Anggota.MAKS_PINJAM

    def __str__(self):
        return f"{self.nama} ({self.nim}) | Sedang pinjam: {len(self.daftar_pinjam)} | Denda: {self.total_denda}"