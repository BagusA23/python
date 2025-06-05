import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
from typing import List, Optional, Dict


class Ayat:
    def __init__(self, nomor: int, teks_arab: str, teks_latin: str = "", arti: str = ""):
        self.nomor = nomor
        self.teks_arab = teks_arab
        self.teks_latin = teks_latin
        self.arti = arti


class Surah:
    def __init__(self, nomor: int, nama: str, nama_latin: str, jumlah_ayat: int,
                 tempat_turun: str, arti: str):
        self.nomor = nomor
        self.nama = nama
        self.nama_latin = nama_latin
        self.jumlah_ayat = jumlah_ayat
        self.tempat_turun = tempat_turun
        self.arti = arti
        self.ayat_list: List[Ayat] = []  # Daftar ayat dalam surah

    def get_info_string(self) -> str:
        # Safe formatting untuk nomor
        try:
            nomor_str = f"{self.nomor:3d}" if isinstance(
                self.nomor, int) else f"{self.nomor:>3}"
        except (ValueError, TypeError):
            nomor_str = f"{str(self.nomor):>3}"

        return (f"{nomor_str}. {self.nama} ({self.nama_latin})\n"
                f"       Arti        : {self.arti}\n"
                f"       Jumlah Ayat : {self.jumlah_ayat}\n"
                f"       Tempat Turun: {self.tempat_turun}\n"
                f"       {'-' * 50}\n")

    def __str__(self) -> str:
        return f"{self.nomor}. {self.nama_latin} - {self.nama}"


class QuranAPI:
    def __init__(self, url: str):
        self.url = url
        self.surah_list: List[Surah] = []
        self.ayat_cache: Dict[int, List[Ayat]] = {}  # Cache untuk ayat-ayat

    def fetch_data(self) -> bool:
        """Mengambil data dari API dengan error handling yang lebih baik"""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.surah_list.clear()

            for item in data:
                # Konversi ke integer dengan safe handling
                try:
                    nomor = int(item.get('nomor', 0))
                except (ValueError, TypeError):
                    nomor = 0

                try:
                    jumlah_ayat = int(
                        item.get('ayat', item.get('jumlah_ayat', 0)))
                except (ValueError, TypeError):
                    jumlah_ayat = 0

                surah = Surah(
                    nomor=nomor,
                    nama=item.get('nama', ''),
                    nama_latin=item.get(
                        'namaLatin', item.get('nama_latin', '')),
                    jumlah_ayat=jumlah_ayat,
                    tempat_turun=item.get(
                        'type', item.get('tempat_turun', '')),
                    arti=item.get('arti', '')
                )
                self.surah_list.append(surah)

            return True

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return False
        except Exception as e:
            print(f"Error parsing data: {e}")
            return False

    def fetch_ayat(self, nomor_surah: int) -> bool:
        """Mengambil ayat-ayat untuk surah tertentu dengan multiple API fallback"""
        if nomor_surah in self.ayat_cache:
            return True

        # Coba beberapa API secara berurutan
        apis_to_try = [
            self._fetch_from_equran_api,
            self._fetch_from_quran_api,
            self._fetch_from_alquran_cloud_api
        ]

        for api_method in apis_to_try:
            try:
                if api_method(nomor_surah):
                    return True
            except Exception as e:
                print(f"API method failed: {e}")
                continue

        return False

    def _fetch_from_equran_api(self, nomor_surah: int) -> bool:
        """API equran.id - biasanya paling reliable"""
        try:
            api_url = f"https://equran.id/api/surat/{nomor_surah}"

            response = requests.get(api_url, timeout=15)
            response.raise_for_status()

            data = response.json()
            ayat_list = []

            if 'ayat' in data:
                for verse in data['ayat']:
                    ayat = Ayat(
                        nomor=verse.get('nomor', 0),
                        teks_arab=verse.get('ar', ''),
                        teks_latin=verse.get('tr', ''),
                        arti=verse.get('idn', '')
                    )
                    ayat_list.append(ayat)

            if ayat_list:
                self.ayat_cache[nomor_surah] = ayat_list

                # Update surah dengan ayat-ayatnya
                surah = self.get_surah_by_number(nomor_surah)
                if surah:
                    surah.ayat_list = ayat_list

                print(
                    f"Successfully loaded {len(ayat_list)} ayat from equran.id")
                return True

            return False

        except Exception as e:
            print(f"Equran API error: {e}")
            raise

    def _fetch_from_quran_api(self, nomor_surah: int) -> bool:
        """API quran.com"""
        try:
            api_url = f"https://api.quran.com/api/v4/verses/by_chapter/{nomor_surah}?language=id&words=true&translations=33"

            response = requests.get(api_url, timeout=15)
            response.raise_for_status()

            data = response.json()
            ayat_list = []

            if 'verses' in data:
                for verse in data['verses']:
                    ayat = Ayat(
                        nomor=verse.get('verse_number', 0),
                        teks_arab=verse.get('text_uthmani', ''),
                        teks_latin=self._get_transliteration(verse),
                        arti=self._get_translation(verse)
                    )
                    ayat_list.append(ayat)

            if ayat_list:
                self.ayat_cache[nomor_surah] = ayat_list

                # Update surah dengan ayat-ayatnya
                surah = self.get_surah_by_number(nomor_surah)
                if surah:
                    surah.ayat_list = ayat_list

                print(
                    f"Successfully loaded {len(ayat_list)} ayat from quran.com")
                return True

            return False

        except Exception as e:
            print(f"Quran.com API error: {e}")
            raise

    def _fetch_from_alquran_cloud_api(self, nomor_surah: int) -> bool:
        """API alquran.cloud - backup API"""
        try:
            # API untuk teks Arab
            arabic_url = f"https://api.alquran.cloud/v1/surah/{nomor_surah}/ar.alafasy"
            # API untuk terjemahan Indonesia
            indo_url = f"https://api.alquran.cloud/v1/surah/{nomor_surah}/id.indonesian"

            # Ambil data Arab
            arabic_response = requests.get(arabic_url, timeout=10)
            arabic_response.raise_for_status()
            arabic_data = arabic_response.json()

            # Ambil data terjemahan
            indo_response = requests.get(indo_url, timeout=10)
            indo_response.raise_for_status()
            indo_data = indo_response.json()

            ayat_list = []

            if ('data' in arabic_data and 'ayahs' in arabic_data['data'] and
                    'data' in indo_data and 'ayahs' in indo_data['data']):

                arabic_ayahs = arabic_data['data']['ayahs']
                indo_ayahs = indo_data['data']['ayahs']

                for i, arabic_ayah in enumerate(arabic_ayahs):
                    indo_ayah = indo_ayahs[i] if i < len(indo_ayahs) else {}

                    ayat = Ayat(
                        nomor=arabic_ayah.get('numberInSurah', i + 1),
                        teks_arab=arabic_ayah.get('text', ''),
                        teks_latin='',  # API ini tidak menyediakan transliterasi
                        arti=indo_ayah.get('text', '')
                    )
                    ayat_list.append(ayat)

            if ayat_list:
                self.ayat_cache[nomor_surah] = ayat_list

                # Update surah dengan ayat-ayatnya
                surah = self.get_surah_by_number(nomor_surah)
                if surah:
                    surah.ayat_list = ayat_list

                print(
                    f"Successfully loaded {len(ayat_list)} ayat from alquran.cloud")
                return True

            return False

        except Exception as e:
            print(f"AlQuran.cloud API error: {e}")
            raise

    def _get_transliteration(self, verse: dict) -> str:
        """Ekstrak transliterasi dari data verse"""
        try:
            if 'words' in verse:
                words = []
                for word in verse['words']:
                    if 'transliteration' in word and 'text' in word['transliteration']:
                        words.append(word['transliteration']['text'])
                return ' '.join(words)
        except:
            pass
        return ""

    def _get_translation(self, verse: dict) -> str:
        """Ekstrak terjemahan dari data verse"""
        try:
            if 'translations' in verse and len(verse['translations']) > 0:
                return verse['translations'][0].get('text', '')
        except:
            pass
        return ""

    def get_surah_by_number(self, nomor: int) -> Optional[Surah]:
        """Mencari surah berdasarkan nomor"""
        for surah in self.surah_list:
            if surah.nomor == nomor:
                return surah
        return None

    def search_surah(self, query: str) -> List[Surah]:
        """Mencari surah berdasarkan nama atau nama latin"""
        query = query.lower()
        results = []
        for surah in self.surah_list:
            if (query in surah.nama.lower() or
                query in surah.nama_latin.lower() or
                    query in surah.arti.lower()):
                results.append(surah)
        return results


class QuranGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📖 Aplikasi Al-Qur'an")
        self.root.geometry("900x700")
        self.root.configure(bg='#f8f9fa')

        # API instance
        self.api = QuranAPI("https://api.npoint.io/99c279bb173a6e28359c/data")

        # Variables
        self.current_surah_list = []
        self.selected_surah = None  # Menyimpan surah yang sedang dipilih

        self.setup_styles()
        self.create_widgets()
        self.load_data()

    def setup_styles(self):
        """Setup tema dan style untuk aplikasi"""
        style = ttk.Style()
        style.theme_use('clam')

        # Custom colors
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'),
                        foreground='#2c3e50', background='#f8f9fa')
        style.configure('Custom.TButton', font=('Arial', 10))
        style.configure('Success.TLabel', foreground='#27ae60',
                        background='#f8f9fa')
        style.configure('Error.TLabel', foreground='#e74c3c',
                        background='#f8f9fa')

    def create_widgets(self):
        """Membuat semua widget GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(title_frame, text="📖 Aplikasi Al-Qur'an",
                                style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(title_frame, text="Daftar 114 Surah dalam Al-Qur'an",
                                   font=('Arial', 11), foreground='#7f8c8d')
        subtitle_label.pack()

        # Status label
        self.status_label = ttk.Label(title_frame, text="Memuat data...",
                                      font=('Arial', 9))
        self.status_label.pack(pady=(5, 0))

        # Search frame
        search_frame = ttk.LabelFrame(
            main_frame, text="🔍 Pencarian Surah", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 15))

        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X)

        ttk.Label(search_input_frame,
                  text="Cari berdasarkan nama, nama latin, atau arti:").pack(anchor=tk.W)

        entry_frame = ttk.Frame(search_input_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(entry_frame, textvariable=self.search_var,
                                      font=('Arial', 11))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X,
                               expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)

        self.search_button = ttk.Button(entry_frame, text="🔍 Cari",
                                        command=self.search_surah, style='Custom.TButton')
        self.search_button.pack(side=tk.RIGHT)

        self.reset_button = ttk.Button(entry_frame, text="🔄 Reset",
                                       command=self.reset_search, style='Custom.TButton')
        self.reset_button.pack(side=tk.RIGHT, padx=(0, 5))

        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Daftar Surah
        left_frame = ttk.LabelFrame(
            content_frame, text="📋 Daftar Surah", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Listbox dengan scrollbar
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.surah_listbox = tk.Listbox(listbox_frame, font=('Arial', 10),
                                        selectmode=tk.SINGLE, height=20,
                                        bg='white', selectbackground='#3498db',
                                        selectforeground='white')
        scrollbar_list = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL,
                                       command=self.surah_listbox.yview)

        self.surah_listbox.configure(yscrollcommand=scrollbar_list.set)
        self.surah_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)

        self.surah_listbox.bind('<<ListboxSelect>>', self.on_surah_select)

        # Right panel - Detail Surah
        right_frame = ttk.LabelFrame(
            content_frame, text="📄 Detail Surah", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Notebook untuk tab detail dan ayat
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab Detail Surah
        detail_frame = ttk.Frame(self.notebook)
        self.notebook.add(detail_frame, text="📋 Info Surah")

        self.detail_text = scrolledtext.ScrolledText(detail_frame,
                                                     font=('Arial', 11),
                                                     wrap=tk.WORD,
                                                     height=25,
                                                     bg='#ffffff',
                                                     relief=tk.FLAT,
                                                     borderwidth=1)
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        # Tab Bacaan Ayat
        ayat_frame = ttk.Frame(self.notebook)
        self.notebook.add(ayat_frame, text="📖 Bacaan Ayat")

        # Control frame untuk ayat
        ayat_control_frame = ttk.Frame(ayat_frame)
        ayat_control_frame.pack(fill=tk.X, padx=5, pady=5)

        self.load_ayat_button = ttk.Button(ayat_control_frame, text="📖 Muat Ayat",
                                           command=self.load_ayat_for_selected_surah,
                                           style='Custom.TButton')
        self.load_ayat_button.pack(side=tk.LEFT, padx=(0, 10))

        self.ayat_status_label = ttk.Label(
            ayat_control_frame, text="Pilih surah untuk melihat ayat")
        self.ayat_status_label.pack(side=tk.LEFT)

        # Text widget untuk menampilkan ayat
        self.ayat_text = scrolledtext.ScrolledText(ayat_frame,
                                                   font=('Arial', 10),
                                                   wrap=tk.WORD,
                                                   bg='#ffffff',
                                                   relief=tk.FLAT,
                                                   borderwidth=1)
        self.ayat_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # Default text untuk detail
        self.detail_text.insert(tk.END,
                                "Selamat datang di Aplikasi Al-Qur'an! 🌟\n\n"
                                "Pilih salah satu surah dari daftar di sebelah kiri "
                                "untuk melihat informasi detail tentang surah tersebut.\n\n"
                                "Anda juga dapat menggunakan fitur pencarian untuk "
                                "menemukan surah berdasarkan nama, nama latin, atau arti.\n\n"
                                "📖 Tab 'Bacaan Ayat' akan menampilkan teks lengkap ayat-ayat "
                                "dalam surah yang dipilih beserta terjemahannya.")
        self.detail_text.configure(state=tk.DISABLED)

        # Default text untuk ayat
        self.ayat_text.insert(tk.END,
                              "📖 Bacaan Ayat Al-Qur'an\n\n"
                              "Pilih surah dari daftar di sebelah kiri, lalu klik tombol "
                              "'Muat Ayat' untuk menampilkan bacaan ayat lengkap.\n\n"
                              "Setiap ayat akan ditampilkan dengan:\n"
                              "• Teks Arab asli\n"
                              "• Transliterasi (bacaan latin)\n"
                              "• Terjemahan dalam bahasa Indonesia")
        self.ayat_text.configure(state=tk.DISABLED)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))

        self.refresh_button = ttk.Button(button_frame, text="🔄 Refresh Data",
                                         command=self.load_data, style='Custom.TButton')
        self.refresh_button.pack(side=tk.LEFT)

        self.about_button = ttk.Button(button_frame, text="ℹ️ Tentang",
                                       command=self.show_about, style='Custom.TButton')
        self.about_button.pack(side=tk.RIGHT)

    def load_data(self):
        """Memuat data dari API dalam thread terpisah"""
        self.status_label.configure(text="Memuat data dari server...",
                                    style='')
        self.refresh_button.configure(state=tk.DISABLED)

        def fetch_in_thread():
            success = self.api.fetch_data()
            self.root.after(0, lambda: self.on_data_loaded(success))

        thread = threading.Thread(target=fetch_in_thread, daemon=True)
        thread.start()

    def on_data_loaded(self, success: bool):
        """Callback setelah data selesai dimuat"""
        self.refresh_button.configure(state=tk.NORMAL)

        if success:
            self.populate_listbox(self.api.surah_list)
            self.status_label.configure(
                text=f"✅ Berhasil memuat {len(self.api.surah_list)} surah",
                style='Success.TLabel')
        else:
            self.status_label.configure(
                text="❌ Gagal memuat data. Periksa koneksi internet.",
                style='Error.TLabel')
            messagebox.showerror("Error",
                                 "Gagal memuat data dari server.\n"
                                 "Pastikan koneksi internet Anda stabil.")

    def populate_listbox(self, surah_list: List[Surah]):
        """Mengisi listbox dengan daftar surah"""
        self.surah_listbox.delete(0, tk.END)
        self.current_surah_list = surah_list

        for surah in surah_list:
            # Safe formatting untuk nomor
            try:
                nomor_str = f"{surah.nomor:3d}" if isinstance(
                    surah.nomor, int) else f"{surah.nomor:>3}"
            except (ValueError, TypeError):
                nomor_str = f"{str(surah.nomor):>3}"

            display_text = f"{nomor_str}. {surah.nama_latin} - {surah.nama}"
            self.surah_listbox.insert(tk.END, display_text)

    def on_surah_select(self, event):
        """Handler ketika surah dipilih dari listbox"""
        selection = self.surah_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.current_surah_list):
                surah = self.current_surah_list[index]
                self.selected_surah = surah
                self.show_surah_detail(surah)

                # Update status ayat
                if surah.ayat_list:
                    self.ayat_status_label.configure(
                        text=f"✅ Ayat untuk {surah.nama_latin} sudah dimuat")
                    self.display_ayat(surah)
                else:
                    self.ayat_status_label.configure(
                        text=f"Klik 'Muat Ayat' untuk {surah.nama_latin}")
                    self.clear_ayat_display()

    def show_surah_detail(self, surah: Surah):
        """Menampilkan detail surah di panel kanan"""
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)

        # Safe formatting untuk nomor dan jumlah ayat
        nomor_display = str(surah.nomor)
        ayat_display = str(surah.jumlah_ayat)

        detail_info = (
            f"🕌 {surah.nama} ({surah.nama_latin})\n"
            f"{'=' * 50}\n\n"
            f"📍 Nomor Surah    : {nomor_display}\n"
            f"📖 Nama Arab      : {surah.nama}\n"
            f"🌐 Nama Latin     : {surah.nama_latin}\n"
            f"💭 Arti           : {surah.arti}\n"
            f"📊 Jumlah Ayat    : {ayat_display}\n"
            f"🏛️  Tempat Turun   : {surah.tempat_turun}\n\n"
            f"{'=' * 50}\n\n"
            f"Surah {surah.nama_latin} adalah surah ke-{nomor_display} "
            f"dalam Al-Qur'an yang memiliki {ayat_display} ayat "
            f"dan diturunkan di {surah.tempat_turun}. "
            f"Arti dari surah ini adalah '{surah.arti}'."
        )

        self.detail_text.insert(tk.END, detail_info)
        self.detail_text.configure(state=tk.DISABLED)

    def load_ayat_for_selected_surah(self):
        """Memuat ayat untuk surah yang sedang dipilih"""
        if not self.selected_surah:
            messagebox.showwarning(
                "Peringatan", "Silakan pilih surah terlebih dahulu!")
            return

        if self.selected_surah.ayat_list:
            # Ayat sudah dimuat, tampilkan langsung
            self.display_ayat(self.selected_surah)
            return

        # Muat ayat dari API
        self.ayat_status_label.configure(text="⏳ Memuat ayat...")
        self.load_ayat_button.configure(state=tk.DISABLED)

        def fetch_ayat_thread():
            success = self.api.fetch_ayat(self.selected_surah.nomor)
            self.root.after(0, lambda: self.on_ayat_loaded(success))

        thread = threading.Thread(target=fetch_ayat_thread, daemon=True)
        thread.start()

    def on_ayat_loaded(self, success: bool):
        """Callback setelah ayat selesai dimuat"""
        self.load_ayat_button.configure(state=tk.NORMAL)

        if success and self.selected_surah:
            self.display_ayat(self.selected_surah)
            self.ayat_status_label.configure(
                text=f"✅ {len(self.selected_surah.ayat_list)} ayat berhasil dimuat")
        else:
            self.ayat_status_label.configure(
                text="❌ Gagal memuat ayat. Coba lagi.")
            messagebox.showerror("Error",
                                 "Gagal memuat ayat dari server.\n"
                                 "Periksa koneksi internet Anda.")

    def display_ayat(self, surah: Surah):
        """Menampilkan ayat-ayat di tab bacaan"""
        self.ayat_text.configure(state=tk.NORMAL)
        self.ayat_text.delete(1.0, tk.END)

        if not surah.ayat_list:
            self.ayat_text.insert(tk.END, "Tidak ada ayat yang tersedia.")
            self.ayat_text.configure(state=tk.DISABLED)
            return

        # Header
        header = (f"📖 {surah.nama} ({surah.nama_latin})\n"
                  f"{'=' * 60}\n"
                  f"Jumlah Ayat: {len(surah.ayat_list)}\n\n")

        self.ayat_text.insert(tk.END, header)

        # Tampilkan setiap ayat
        for ayat in surah.ayat_list:
            ayat_text = f"Ayat {ayat.nomor}\n"
            ayat_text += f"{'─' * 40}\n"

            # Teks Arab
            if ayat.teks_arab:
                ayat_text += f"🔸 Arab: {ayat.teks_arab}\n\n"

            # Transliterasi
            if ayat.teks_latin:
                ayat_text += f"🔸 Latin: {ayat.teks_latin}\n\n"

            # Terjemahan
            if ayat.arti:
                ayat_text += f"🔸 Arti: {ayat.arti}\n"

            ayat_text += f"\n{'═' * 60}\n\n"

            self.ayat_text.insert(tk.END, ayat_text)

        self.ayat_text.configure(state=tk.DISABLED)

        # Pindah ke tab ayat
        self.notebook.select(1)

    def clear_ayat_display(self):
        """Membersihkan tampilan ayat"""
        self.ayat_text.configure(state=tk.NORMAL)
        self.ayat_text.delete(1.0, tk.END)
        self.ayat_text.insert(tk.END,
                              "📖 Bacaan Ayat Al-Qur'an\n\n"
                              "Klik tombol 'Muat Ayat' untuk menampilkan bacaan ayat lengkap.\n\n"
                              "Setiap ayat akan ditampilkan dengan:\n"
                              "• Teks Arab asli\n"
                              "• Transliterasi (bacaan latin)\n"
                              "• Terjemahan dalam bahasa Indonesia")
        self.ayat_text.configure(state=tk.DISABLED)

    def on_search(self, event):
        """Handler untuk pencarian real-time"""
        if len(self.search_var.get()) >= 2:
            self.search_surah()
        elif len(self.search_var.get()) == 0:
            self.reset_search()

    def search_surah(self):
        """Melakukan pencarian surah"""
        query = self.search_var.get().strip()
        if not query:
            self.reset_search()
            return

        results = self.api.search_surah(query)
        self.populate_listbox(results)

        if results:
            self.status_label.configure(
                text=f"🔍 Ditemukan {len(results)} surah yang cocok dengan '{query}'",
                style='Success.TLabel')
        else:
            self.status_label.configure(
                text=f"❌ Tidak ada surah yang cocok dengan '{query}'",
                style='Error.TLabel')

    def reset_search(self):
        """Reset pencarian dan tampilkan semua surah"""
        self.search_var.set("")
        self.populate_listbox(self.api.surah_list)
        self.status_label.configure(
            text=f"✅ Menampilkan semua {len(self.api.surah_list)} surah",
            style='Success.TLabel')

    def show_about(self):
        """Menampilkan dialog tentang aplikasi"""
        about_text = (
            "📖 Aplikasi Al-Qur'an v2.0\n\n"
            "Aplikasi ini menampilkan daftar 114 surah dalam Al-Qur'an "
            "beserta informasi detail dan bacaan ayat lengkap.\n\n"
            "Fitur:\n"
            "• Daftar lengkap 114 surah\n"
            "• Pencarian berdasarkan nama, nama latin, atau arti\n"
            "• Informasi detail setiap surah\n"
            "• Bacaan ayat lengkap dengan teks Arab, transliterasi, dan terjemahan\n"
            "• Interface yang user-friendly dengan tab system\n\n"
            "Data diambil dari API Al-Qur'an online yang terpercaya.\n\n"
            "Semoga bermanfaat untuk pembelajaran dan ibadah! 🤲"
        )
        messagebox.showinfo("Tentang Aplikasi", about_text)


def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()

    # Set icon jika ada
    try:
        root.iconbitmap('icon.ico')  # Opsional: tambahkan icon
    except:
        pass

    app = QuranGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
