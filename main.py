from datetime import date, timedelta
from models import Buku, Majalah, Dvd, Item, Anggota, PerpustakaanError
from perpustakaan import Perpustakaan


def garis(judul):
    print("\n" + "=" * 56)
    print(judul.center(56))
    print("=" * 56)


def main():
    perpus = Perpustakaan("Perpustakaan Kampus")

    # --- Isi data awal ---
    perpus.tambah_item(Buku("B001", "Pemrograman Python", 2022, "Budi Santoso"))
    perpus.tambah_item(Buku.dari_string("B002;Struktur Data;2021;Siti Aminah"))
    perpus.tambah_item(Majalah("M001", "Tekno Masa Kini", 2026, 45))
    perpus.tambah_item(Dvd("D001", "Dokumenter Teknologi", 2020, 120))

    perpus.tambah_anggota(Anggota("2024001", "Tira"))
    perpus.tambah_anggota(Anggota("2024002", "Tari"))

    garis("DAFTAR KOLEKSI")
    perpus.tampilkan_koleksi()

    # --- Polymorphism: method sama, hasil beda ---
    garis("ATURAN PINJAM (POLYMORPHISM)")
    for item in perpus.koleksi:
        print(f"{item.judul:<24} -> {item.durasi_pinjam()} hari, "
              f"denda {Perpustakaan.format_rupiah(item.denda_per_hari())}/hari")

    # --- Abstract class tidak bisa dibuat objeknya ---
    garis("TES ABSTRACT CLASS")
    try:
        Item("X001", "Tes", 2020)
    except TypeError as e:
        print("❌ Gagal membuat objek Item:", e)

    # --- Transaksi ---
    garis("TRANSAKSI PEMINJAMAN")
    perpus.pinjam("2024001", "B001")
    perpus.pinjam("2024001", "M001")

    # --- Tes error (custom exception) ---
    garis("TES ERROR HANDLING")
    try:
        perpus.pinjam("2024002", "B001")      # sudah dipinjam Andi
    except PerpustakaanError as e:
        print("❌", e)

    try:
        perpus.pinjam("9999999", "B002")      # NIM tidak ada
    except PerpustakaanError as e:
        print("❌", e)

    try:
        Buku("A", "Kode Pendek", 2020, "Anonim")
    except PerpustakaanError as e:
        print("❌", e)

    # --- Pengembalian (simulasi telat 10 hari) ---
    garis("PENGEMBALIAN")
    telat_10_hari = date.today() + timedelta(days=10)
    perpus.kembalikan("2024001", "B001", telat_10_hari)
    perpus.kembalikan("2024001", "M001", telat_10_hari)

    garis("STATUS ANGGOTA")
    for a in perpus.anggota:
        print(a)

    garis("STATISTIK GLOBAL")
    print(f"Total koleksi          : {Item.get_total_items()}")
    print(f"Jumlah koleksi         : {len(perpus)}")
    print(f"Total anggota          : {Anggota.total_anggota}")


if __name__ == "__main__":
    main()