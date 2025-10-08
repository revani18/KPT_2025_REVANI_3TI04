import math
import time
import multiprocessing

def hitung_akar_kuadrat_paralel_batch(batch):
    """Fungsi untuk memproses sebuah batch angka."""
    hasil_batch = [math.sqrt(angka) for angka in batch]
    return hasil_batch

def buat_batch(data, ukuran_batch):
    """Generator untuk memecah data menjadi batch."""
    for i in range(0, len(data), ukuran_batch):
        yield data[i:i + ukuran_batch]

if __name__ == '__main__':
    daftar_angka = list(range(1, 5000001))
    jumlah_proses = multiprocessing.cpu_count()
    ukuran_batch = 100000  # Ukuran batch yang ideal dapat bervariasi

    print("\nMemulai pemrosesan paralel dengan batching...")
    start_time = time.time()

    # Membuat batch dari data
    daftar_batch = list(buat_batch(daftar_angka, ukuran_batch))

    # Menggunakan Pool untuk memproses batch
    with multiprocessing.Pool(processes=jumlah_proses) as pool:
        hasil_nested = pool.map(hitung_akar_kuadrat_paralel_batch, daftar_batch)

    # Menggabungkan hasil dari semua batch
    hasil_paralel = []
    for sublist in hasil_nested:
        hasil_paralel.extend(sublist)

    end_time = time.time()
    durasi_paralel = end_time - start_time
    print(f"Pemrosesan paralel dengan batching selesai dalam: {durasi_paralel:.4f} detik")

    # Perbandingan
    # Catatan: Variabel durasi_serial diasumsikan sudah ada dari eksekusi Tugas 1
    # Jika tidak, Anda bisa menggabungkan kedua kode ke dalam satu file untuk perbandingan langsung.
    try:
        print(f"\nPerbandingan:")
        print(f"Waktu Serial: {durasi_serial:.4f} detik")
        print(f"Waktu Paralel (dengan batching): {durasi_paralel:.4f} detik")
        print(f"Percepatan: {durasi_serial / durasi_paralel:.2f}x")
    except NameError:
        print("\nUntuk perbandingan, jalankan kode Tugas 1 terlebih dahulu.")