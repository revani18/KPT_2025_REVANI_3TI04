# Contoh implementasi basic multiprocessing di Python menggunakan Process dan Pool

#!/usr/bin/env python3
"""
File: kode_implementasi_multiprocessing_process_dan_multiprocessing_pool.py
Tujuan:
  1. Demonstrasi perbedaan multiprocessing.Process vs multiprocessing.Pool
  2. Analisis speedup berdasarkan jumlah worker (diminishing returns)
"""

import multiprocessing
import time
import os
from statistics import median

# --- Fungsi pekerja ---

def worker_function_process(nomor: int) -> None:
    """Fungsi pekerja untuk multiprocessing.Process."""
    pid = os.getpid()
    print(f"[{pid}] [Process] Tugas {nomor} sedang bekerja...")
    time.sleep(1) # Simulasikan beban kerja 1 detik
    print(f"[{pid}] [Process] Tugas {nomor} selesai.")

def worker_function_pool(nomor: int) -> str:
    """Fungsi pekerja untuk multiprocessing.Pool."""
    pid = os.getpid()
    time.sleep(1) # Simulasikan beban kerja 1 detik
    return f"[{pid}] [Pool] Tugas {nomor} selesai setelah 1 detik."

# --- Fungsi Utama untuk Setiap Metode ---

# --- Demo manual Process ---

def run_with_process():
    print("-------------------------------------------------------")
    print("--- 1. DEMO: MENGGUNAKAN multiprocessing.Process ---")
    print("-------------------------------------------------------")

    jumlah_tugas = 4
    proses_list = []

    start = time.perf_counter()
    # Membuat dan memulai proses secara manual
    for i in range(jumlah_tugas):
        p = multiprocessing.Process(target=worker_function_process, args=(i+1,))
        proses_list.append(p)
        p.start() # Memulai eksekusi proses

    # Menunggu semua proses selesai
    for p in proses_list:
        p.join()
    durasi = time.perf_counter() - start

    print(f"\nSemua proses selesai. Total waktu: {durasi:.2f} detik.")
    return durasi

# --- Demo Pool sederhana ---

def run_with_pool():
    print("\n-------------------------------------------------------")
    print("--- 2. DEMO: MENGGUNAKAN multiprocessing.Pool ---")
    print("-------------------------------------------------------")

    data_tugas = list(range(1, 6)) # 5 tugas
    jumlah_worker = 3 # Hanya 3 worker untuk demonstrasi antrian tugas

    start = time.perf_counter()
    # Membuat Pool dengan jumlah proses yang ditentukan (misal: 3)
    with multiprocessing.Pool(processes=jumlah_worker) as pool:
        print(f"Pool dibuat dengan {pool._processes} worker.")

        # Mendistribusikan tugas menggunakan map. Pool menangani start dan join secara otomatis.
        # Karena ada 5 tugas dan 3 worker, tugas akan diantrikan
        hasil = pool.map(worker_function_pool, data_tugas)
    durasi = time.perf_counter() - start

    print("\nSemua proses selesai dieksekusi oleh multiprocessing.Pool.")
    print(f"Total waktu: {durasi:.2f} detik.")
    print("Hasil yang dikumpulkan:")
    for res in hasil:
        print(res)
    print("-------------------------------------------------------")
    return durasi

# --- Eksperimen variasi worker ---

def benchmark_pool():
    print("\n=======================================================")
    print("=== 3. ANALISIS: VARIASI JUMLAH WORKER & SPEEDUP ===")
    print("=======================================================")

    cpu_count = multiprocessing.cpu_count()
    variasi = [1, 2, 4, 8, cpu_count + 1, cpu_count + 2]
    data_tugas = list(range(1, 9))  # 8 tugas
    hasil = {}

    for jumlah_worker in variasi:
        start = time.perf_counter()
        with multiprocessing.Pool(processes=jumlah_worker) as pool:
            _ = pool.map(worker_function_pool, data_tugas)
        waktu = time.perf_counter() - start
        hasil[jumlah_worker] = waktu
        print(f"{jumlah_worker:>2d} worker -> {waktu:.3f} detik")

    print("\n--- Analisis Speedup ---")
    baseline = hasil[variasi[0]]
    for w, t in hasil.items():
        speedup = baseline / t
        print(f"{w:>2d} worker -> {t:.3f}s | speedup {speedup:.2f}x")

    # Deteksi diminishing returns (improvement <5%)
    prev_time = baseline
    for w in variasi[1:]:
        improvement = (prev_time - hasil[w]) / prev_time
        if improvement < 0.05:
            print(f"\n⚠️  Diminishing returns mulai sekitar {w} worker (improvement <5%).")
            break
        prev_time = hasil[w]

# --- Entry point ---
# --- Blok Kontrol Wajib untuk Windows ---
if __name__ == '__main__':
    # Pastikan Python menggunakan metode 'spawn' di Windows secara default.
    # Tidak perlu setting eksplisit, tapi ini adalah tempat yang tepat untuk menjalankannya.

    print(f"CPU logical core terdeteksi: {multiprocessing.cpu_count()}")
    durasi_proc = run_with_process()
    durasi_pool = run_with_pool()
    benchmark_pool()
