# Maze Adventure Generator Game Scratch (.sb3)

Generator project Scratch otomatis yang ditulis murni pakai Python tanpa perlu buka editor Scratch dan susun blok satu-satu. Jalankan skripnya, dapat file `.sb3` siap upload dan langsung dimainkan.

## Apa yang Dihasilkan

Game labirin (maze) sederhana:
- Kontrol karakter pakai tombol panah (⬆️⬇️⬅️➡️)
- Tabrak tembok → posisi otomatis dibatalkan (tidak bisa tembus)
- Kena Monster → Game Over, skor & timer reset, balik ke titik start
- Sentuh Bintang → Menang, game berhenti
- Skor bertambah otomatis seiring waktu (dihitung lewat Timer)

## Cara Pakai

1. Pastikan Python 3 terpasang (tidak butuh library tambahan, semua pakai standard library: `json`, `zipfile`, `os`, `struct`, `math`, `io`)
2. Jalankan skrip:
   ```bash
   python3 maze_adventure.py
   ```
3. File `maze_adventure_v2.sb3` akan muncul di folder yang sama
4. Upload ke Scratch:
   - Buka [scratch.mit.edu](https://scratch.mit.edu) dan login
   - Klik **Create**
   - **File > Load from your computer**
   - Pilih `maze_adventure_v2.sb3`
   - Klik ▶️ dan mainkan

## Cara Kerja

File `.sb3` sebenarnya cuma arsip ZIP berisi `project.json` (definisi seluruh blok kode Scratch) plus aset gambar dan suara. Skrip ini membangun semuanya secara terprogram, tanpa file eksternal apapun:

| Bagian | Isi |
|---|---|
| **Aset visual** | SVG buatan sendiri: 2 kostum Hero, Monster, Bintang, pola Tembok labirin, dan Backdrop panggung |
| **Aset suara** | WAV disintesis manual pakai gelombang sinus (fungsi `make_beep_wav`) suara "Oops" saat kalah dan "Win" saat menang |
| **project.json** | 5 target: Stage (variabel & timer), Tembok, Hero, Monster, Bintang masing-masing dengan logika blok Scratch (`event`, `motion`, `control`, `sensing`) |

## Struktur Target

| Target | Peran |
|---|---|
| **Stage** | Simpan variabel Skor & Timer, tambah skor tiap detik |
| **Tembok** | Tampilkan pola labirin, jadi rintangan |
| **Hero** | Sprite pemain gerak dengan tombol panah, deteksi tabrakan tembok/monster/bintang |
| **Monster** | Bergerak otomatis, memantul & berbelok saat kena tembok |
| **Bintang** | Target kemenangan, berputar terus sebagai animasi idle |

## Kustomisasi

Beberapa hal yang gampang diubah langsung di skrip:
- **Bentuk labirin**: edit koordinat `rect` di dalam `wall_svg`
- **Posisi start/finish**: ubah `x`, `y` pada target Hero dan Bintang
- **Kecepatan gerak**: ubah nilai `DX`/`DY` (default `5`) di blok `mvR`, `mvL`, `mvU`, `mvD`
- **Kecepatan/pola musuh**: ubah `STEPS` di blok `mm1` (kecepatan) atau posisi awal di `mg1`
- **Warna tembok**: ubah `WALL_COLOR`, harus konsisten dengan warna `fill` di `wall_svg`

## Catatan

Skrip ini murni untuk membuat *project file* Scratch belum melakukan playtesting otomatis. Setelah upload, coba mainkan dulu di Scratch untuk memastikan jalur labirin bisa dilewati sebelum dipakai untuk keperluan lain (misalnya tugas/kompetisi).
