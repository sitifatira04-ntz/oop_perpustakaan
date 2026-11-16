from models import Peminjaman, PerpustakaanError


class Perpustakaan:
    def __init__(self, nama):
        self.nama = nama
        self.koleksi = []
        self.anggota = []

    # ----- Static method -----
    @staticmethod
    def format_rupiah(angka):
        return "Rp" + f"{angka:,}".replace(",", ".")

    # ----- Magic method -----
    def __len__(self):
        return len(self.koleksi)

    # ----- Tambah data -----
    def tambah_item(self, item):
        if item in self.koleksi:            # memakai __eq__
            raise PerpustakaanError(f"Kode {item.kode} sudah terdaftar")
        self.koleksi.append(item)

    def tambah_anggota(self, anggota):
        self.anggota.append(anggota)

    # ----- Pencarian -----
    def cari_item(self, kode):
        for item in self.koleksi:
            if item.kode == kode:
                return item
        raise PerpustakaanError(f"Koleksi dengan kode {kode} tidak ditemukan")

    def cari_anggota(self, nim):
        for a in self.anggota:
            if a.nim == nim:
                return a
        raise PerpustakaanError(f"Anggota dengan NIM {nim} tidak ditemukan")

    # ----- Transaksi -----
    def pinjam(self, nim, kode):
        anggota = self.cari_anggota(nim)
        item = self.cari_item(kode)

        if not item.tersedia:
            raise PerpustakaanError(f"'{item.judul}' sedang dipinjam orang lain")
        if not anggota.bisa_pinjam():
            raise PerpustakaanError(f"{anggota.nama} sudah mencapai batas pinjam")

        item.tersedia = False
        transaksi = Peminjaman(item)
        anggota.daftar_pinjam.append(transaksi)
        print(f"✅ {anggota.nama} meminjam '{item.judul}'. Jatuh tempo: {transaksi.jatuh_tempo}")
        return transaksi

    def kembalikan(self, nim, kode, tanggal_kembali=None):
        anggota = self.cari_anggota(nim)
        item = self.cari_item(kode)

        for transaksi in anggota.daftar_pinjam:
            if transaksi.item == item:
                telat = transaksi.hari_telat(tanggal_kembali)
                denda = item.hitung_denda(telat)     # polymorphism
                anggota.tambah_denda(denda)
                anggota.daftar_pinjam.remove(transaksi)
                item.tersedia = True

                print(f"📚 {anggota.nama} mengembalikan '{item.judul}'.")
                if telat > 0:
                    print(f"⚠️  Terlambat {telat} hari, denda {Perpustakaan.format_rupiah(denda)}")
                else:
                    print("👍 Tepat waktu, tidak ada denda.")
                return denda

        raise PerpustakaanError(f"{anggota.nama} tidak meminjam '{item.judul}'")

    def tampilkan_koleksi(self):
        for item in self.koleksi:
            print(item)