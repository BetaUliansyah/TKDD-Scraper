# Info Terbaru
Website DJPK akan otomatis berubah menjadi mode maintenance jika kita melakukan requests terlalu banyak dalam rentang waktu yang singkat. Solusinya, ambil data dari web Jaga.id yagn tidak membatasi requests. Selain itu, response sudah dalam bentuk json. Silakan gunakan [jaga-apbd-scraper](https://github.com/BetaUliansyah/jaga-apbd-scraper) atau jaga-tkdd-scraper (under development).

# Usage
1. Jalankan dulu get_kode_provinsi.py untuk membentuk file kode_provinsi.csv
2. Kemudian jalankan get_kode_pemda.py untuk membentuk file kode_pemda.csv
3. Selanjutnya jalankan get_akun_tkdd.py untuk membentuk file akun-tkdd-{tahun}.csv
4. Jalankan scraper
