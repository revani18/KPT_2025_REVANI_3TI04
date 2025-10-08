import multiprocessing
import time
import os

# --- Fungsi Pekerja ---

def worker_function_process(nomor):
    """Fungsi pekerja untuk multiprocessing.Process."""
    pid = os.getpid()
    print(f"[{pid}] [Process] Tugas {nomor} sedang bekerja...")
    time.sleep(1) # Simulasikan beban kerja 1 detik
    print(f"[{pid}] [Process] Tugas {nomor} selesai.")

def worker_function_pool(nomor):
    """Fungsi pekerja untuk multiprocessing.Pool."""
    pid = os.getpid()
    time.sleep(1) # Simulasikan beban kerja 1 detik
    return f"[{pid}] [Pool] Tugas {nomor} selesai setelah 1 detik."

# --- Fungsi Utama untuk Setiap Metode ---

def run_with_process():
    print("-------------------------------------------------------")
    print("--- 1. DEMO: MENGGUNAKAN multiprocessing.Process ---")
    print("-------------------------------------------------------")

    jumlah_tugas = 4
    proses_list = []

    # Membuat dan memulai proses secara manual
    for i in range(jumlah_tugas):
        p = multiprocessing.Process(target=worker_function_process, args=(i+1,))
        proses_list.append(p)
        p.start()  # Memulai eksekusi proses

    # Menunggu semua proses selesai
    for p in proses_list:
        p.join()

    print("\nSemua proses selesai dieksekusi oleh multiprocessing.Process.")

def run_with_pool():
    print("\n-------------------------------------------------------")
    print("--- 2. DEMO: MENGGUNAKAN multiprocessing.Pool ---")
    print("-------------------------------------------------------")

    data_tugas = list(range(1, 6)) # 5 tugas
    jumlah_worker = 3 # Hanya 3 worker untuk demonstrasi antrian tugas

    # Membuat Pool dengan jumlah proses yang ditentukan (misal: 3)
    with multiprocessing.Pool(processes=jumlah_worker) as pool:
        print(f"Pool dibuat dengan {pool._processes} worker.")

        # Mendistribusikan tugas menggunakan map. Pool menangani start dan join secara otomatis.
        # Karena ada 5 tugas dan 3 worker, tugas akan diantrikan.
        hasil = pool.map(worker_function_pool, data_tugas)

    print("\nSemua proses selesai dieksekusi oleh multiprocessing.Pool.")
    print("Hasil yang dikumpulkan:")
    for res in hasil:
        print(res)
    print("-------------------------------------------------------")

# --- Blok Kontrol Wajib untuk Windows ---
if __name__ == '__main__':
    # Pastikan Python menggunakan metode 'spawn' di Windows secara default.
    # Tidak perlu setting eksplisit, tapi ini adalah tempat yang tepat untuk menjalankannya.

    run_with_process()
    run_with_pool()