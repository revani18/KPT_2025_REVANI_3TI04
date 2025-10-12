import threading
import time
import random

# 1. Definisikan fungsi (tugas) yang akan dijalankan oleh thread
def tugas_koki(nama_tugas, durasi_langkah):
    """
    Fungsi ini mensimulasikan pekerjaan yang memakan waktu.
    """
    print(f">>> {nama_tugas} dimulai.")
    
    # Simulasikan beberapa langkah kerja
    for i in range(1, 4):
        print(f"    {nama_tugas}: Langkah ke-{i}")
        # Jeda sejenak untuk mensimulasikan waktu tunggu (misalnya, I/O)
        time.sleep(durasi_langkah) 
        
    print(f"<<< {nama_tugas} selesai.")

# 2. Program Utama
if __name__ == "__main__":
    start=time.time()
    print("Program Utama dimulai. Chef mulai bekerja! 🧑‍🍳")
    
    # Mendefinisikan tugas dan argumennya
    # Tugas 1: Membuat Kopi (durasi langkah 0.5 detik)
    thread_kopi = threading.Thread(
        target=tugas_koki, 
        args=("Tugas Kopi ☕", 0.5)
    )
    
    # Tugas 2: Memanggang Roti (durasi langkah 1.0 detik, lebih lama)
    thread_roti = threading.Thread(
        target=tugas_koki, 
        args=("Tugas Roti 🍞", 1.0)
    )
    
    # Memulai eksekusi thread
    thread_kopi.start()
    thread_roti.start()
    
    # Perintah join() memastikan program utama menunggu kedua thread selesai
    # sebelum mencetak "Program Utama selesai."
    thread_kopi.join()
    thread_roti.join()

    end = time.time()
    print(f"Total waktu dengan multithread: {end-start} s")

    print(f"Ini cara serial tanpa multithread")

    start=time.time()
    print(f"Total waktu: {end-start} s")
    tugas_koki("Task kopi", 0.5)
    tugas_koki("Taskroti", 1)
    end = time.time()
    print(f"Total waktu dengan tanpa multithread/serial: {end-start} s")
    
    print("Program Utama selesai. (Semua pesanan terkirim!)")