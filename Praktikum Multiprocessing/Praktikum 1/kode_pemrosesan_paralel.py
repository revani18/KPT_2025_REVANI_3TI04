import math
import time
import multiprocessing

def hitung_akar_kuadrat_paralel(angka):
    """Fungsi untuk menghitung akar kuadrat dari sebuah angka."""
    return math.sqrt(angka)

if __name__ == '__main__':
    daftar_angka = list(range(1, 5000001))

    print("\nMemulai pemrosesan paralel...")
    start_time = time.time()

    # Membuat Pool dengan jumlah proses yang sesuai dengan inti CPU
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        hasil_paralel = pool.map(hitung_akar_kuadrat_paralel, daftar_angka)

    end_time = time.time()
    durasi_paralel = end_time - start_time
    print(f"Pemrosesan paralel selesai dalam: {durasi_paralel:.4f} detik")
    # print(f"Contoh hasil: {hasil_paralel[:5]}...") # Opsional: uncomment untuk melihat hasilnya